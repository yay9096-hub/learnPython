"""SQLite 持久化层。单用户场景，不做鉴权。"""
import json
import os
import shutil
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime, timezone

DATA_DIR = os.environ.get("DATA_DIR", "/app/data")
DB_PATH = os.path.join(DATA_DIR, "progress.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS progress (
    day            INTEGER PRIMARY KEY,
    status         TEXT    NOT NULL DEFAULT 'locked',   -- locked / opened / done
    code           TEXT    NOT NULL DEFAULT '',
    hints_used     INTEGER NOT NULL DEFAULT 0,
    solution_seen  INTEGER NOT NULL DEFAULT 0,
    run_count      INTEGER NOT NULL DEFAULT 0,
    error_count    INTEGER NOT NULL DEFAULT 0,
    seconds_spent  INTEGER NOT NULL DEFAULT 0,
    checks_passed  TEXT    NOT NULL DEFAULT '[]',
    exercises_done TEXT    NOT NULL DEFAULT '[]',
    first_opened   TEXT,
    completed_at   TEXT,
    updated_at     TEXT
);

CREATE TABLE IF NOT EXISTS works (
    day        INTEGER PRIMARY KEY,
    title      TEXT NOT NULL,
    snippet    TEXT NOT NULL DEFAULT '',
    image      TEXT,                    -- dataURL（turtle 画布截图）
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    day        INTEGER,
    kind       TEXT NOT NULL,
    payload    TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS kv (
    k TEXT PRIMARY KEY,
    v TEXT NOT NULL
);
"""


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


BACKUP_DIR = os.path.join(DATA_DIR, "backups")
KEEP_BACKUPS = 30


def auto_backup() -> str | None:
    """每次启动先备份一份。

    这不是洁癖 —— 真出过事：有人把 progress.db 当测试残留删掉了，
    她好几天的学习记录一次性没了，而且没有任何备份可以找回。
    一个 30KB 的文件，留 30 份也才 1MB，没有不备份的理由。
    """
    if not os.path.exists(DB_PATH) or os.path.getsize(DB_PATH) == 0:
        return None
    os.makedirs(BACKUP_DIR, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = os.path.join(BACKUP_DIR, f"progress-{stamp}.db")
    if not os.path.exists(dest):
        shutil.copy2(DB_PATH, dest)

    # 只留最近 N 份，多的删掉
    backups = sorted(
        f for f in os.listdir(BACKUP_DIR)
        if f.startswith("progress-") and f.endswith(".db")
    )
    for old in backups[:-KEEP_BACKUPS]:
        try:
            os.remove(os.path.join(BACKUP_DIR, old))
        except OSError:
            pass
    return dest


def stats() -> dict:
    """启动时打印出来，让「数据存在哪、有多少」肉眼可见。"""
    with connect() as c:
        done = c.execute(
            "SELECT COUNT(*) FROM progress WHERE status='done'").fetchone()[0]
        touched = c.execute("SELECT COUNT(*) FROM progress").fetchone()[0]
        works = c.execute("SELECT COUNT(*) FROM works").fetchone()[0]
    return {
        "db": os.path.abspath(DB_PATH),
        "done": done,
        "touched": touched,
        "works": works,
    }


def init() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    auto_backup()
    with connect() as c:
        c.executescript(SCHEMA)


@contextmanager
def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def get_progress(day: int) -> dict:
    with connect() as c:
        row = c.execute("SELECT * FROM progress WHERE day=?", (day,)).fetchone()
    if row is None:
        return {
            "day": day, "status": "locked", "code": "", "hints_used": 0,
            "solution_seen": 0, "run_count": 0, "error_count": 0,
            "seconds_spent": 0, "checks_passed": [], "exercises_done": [],
            "first_opened": None, "completed_at": None,
        }
    return _row_to_progress(row)


def _row_to_progress(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["checks_passed"] = json.loads(d.get("checks_passed") or "[]")
    d["exercises_done"] = json.loads(d.get("exercises_done") or "[]")
    return d


def all_progress() -> dict:
    with connect() as c:
        rows = c.execute("SELECT * FROM progress").fetchall()
    return {r["day"]: _row_to_progress(r) for r in rows}


def _ensure_row(c, day: int) -> None:
    c.execute(
        "INSERT OR IGNORE INTO progress (day, status, first_opened, updated_at)"
        " VALUES (?, 'opened', ?, ?)",
        (day, now(), now()),
    )


def update_progress(day: int, **fields) -> dict:
    allowed = {
        "status", "code", "hints_used", "solution_seen", "run_count",
        "error_count", "seconds_spent", "checks_passed", "exercises_done",
        "completed_at",
    }
    fields = {k: v for k, v in fields.items() if k in allowed and v is not None}
    for key in ("checks_passed", "exercises_done"):
        if key in fields and not isinstance(fields[key], str):
            fields[key] = json.dumps(fields[key], ensure_ascii=False)
    with connect() as c:
        _ensure_row(c, day)
        if fields:
            sets = ", ".join(f"{k}=?" for k in fields)
            c.execute(
                f"UPDATE progress SET {sets}, updated_at=? WHERE day=?",
                (*fields.values(), now(), day),
            )
    return get_progress(day)


def bump(day: int, field: str, amount: int = 1) -> dict:
    assert field in {"run_count", "error_count", "seconds_spent", "hints_used"}
    with connect() as c:
        _ensure_row(c, day)
        c.execute(
            f"UPDATE progress SET {field}={field}+?, updated_at=? WHERE day=?",
            (amount, now(), day),
        )
    return get_progress(day)


def log_event(day, kind: str, payload: dict | None = None) -> None:
    with connect() as c:
        c.execute(
            "INSERT INTO events (day, kind, payload, created_at) VALUES (?,?,?,?)",
            (day, kind, json.dumps(payload or {}, ensure_ascii=False), now()),
        )


def save_work(day: int, title: str, snippet: str, image: str | None) -> None:
    with connect() as c:
        c.execute(
            "INSERT INTO works (day, title, snippet, image, created_at)"
            " VALUES (?,?,?,?,?)"
            " ON CONFLICT(day) DO UPDATE SET title=excluded.title,"
            " snippet=excluded.snippet, image=COALESCE(excluded.image, works.image)",
            (day, title, snippet, image, now()),
        )


def list_works() -> list[dict]:
    with connect() as c:
        rows = c.execute("SELECT * FROM works ORDER BY day").fetchall()
    return [dict(r) for r in rows]


def local_date(ts: str) -> str:
    """把存进库的 UTC 时间戳换算成**本地日期**。

    时间戳按 UTC 存（跨时区不会错），但「今天做了几天」「连续几天」
    要按她所在时区的自然日算 —— 晚上 11 点做完的，算今天不算昨天。
    两边不统一的话，跨零点时连击会莫名其妙断掉。
    """
    try:
        dt = datetime.fromisoformat(ts)
    except ValueError:
        return ts[:10]
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone().date().isoformat()


def completed_dates() -> list[str]:
    with connect() as c:
        rows = c.execute(
            "SELECT completed_at FROM progress WHERE completed_at IS NOT NULL"
        ).fetchall()
    return sorted({local_date(r["completed_at"]) for r in rows})


def completed_today() -> int:
    """今天已经通关了几天的课程内容。

    她一天能做完四天 —— 这不是坏事，但连做时知识点没有过夜巩固。
    前端拿这个数字来温和提醒一句，**不做任何阻拦**。
    """
    today = date.today().isoformat()
    # 注意不能用 completed_dates()：那是个去重后的集合，
    # 一天通关四关会被压成 1。这里要按行数数。
    with connect() as c:
        rows = c.execute(
            "SELECT completed_at FROM progress WHERE completed_at IS NOT NULL"
        ).fetchall()
    return sum(1 for r in rows if local_date(r["completed_at"]) == today)


def streak_info() -> dict:
    """连续打卡：按自然日算。断签不清零历史最长记录。"""
    days = completed_dates()
    if not days:
        return {"current": 0, "longest": 0, "total": 0}
    ds = [date.fromisoformat(d) for d in days]
    longest = run = 1
    for prev, cur in zip(ds, ds[1:]):
        run = run + 1 if (cur - prev).days == 1 else 1
        longest = max(longest, run)
    today = date.today()
    gap = (today - ds[-1]).days
    current = 0
    if gap <= 1:                       # 今天或昨天完成过，连击还活着
        current = 1
        for prev, cur in zip(reversed(ds[:-1]), reversed(ds[1:])):
            if (cur - prev).days == 1:
                current += 1
            else:
                break
    return {"current": current, "longest": longest, "total": len(ds)}
