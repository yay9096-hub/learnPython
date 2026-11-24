"""派森酱学院 · 后端 API。单用户本地部署，无鉴权。"""
import sys

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import content, db

app = FastAPI(title="派森酱学院 API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)
api = APIRouter(prefix="/api")


def _log(msg: str) -> None:
    """Windows 控制台默认是 GBK，emoji 和部分符号会直接抛 UnicodeEncodeError
    把后端搞挂。启动横幅不值得为它崩，编码不了就降级输出。"""
    try:
        print(msg, flush=True)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "ascii"
        print(msg.encode(enc, "replace").decode(enc, "replace"), flush=True)


@app.on_event("startup")
def _startup() -> None:
    db.init()
    # 把「数据存在哪、有多少」直接打在启动日志里。
    # 之前丢过一次进度，就是因为没人看得见这个文件的存在。
    s = db.stats()
    _log("=" * 58)
    _log(f"  进度数据库：{s['db']}")
    _log(f"  已通关 {s['done']} 天 · 打开过 {s['touched']} 天 · 作品 {s['works']} 件")
    _log(f"  自动备份：{db.BACKUP_DIR}")
    _log(f"  （每次启动自动存一份，保留最近 {db.KEEP_BACKUPS} 份；make backups 可查看）")
    _log("=" * 58)


# ---------------------------------------------------------------- 课程内容

@api.get("/days")
def list_days():
    days = content.available_days()
    progress = db.all_progress()
    out = []
    for d in days:
        m = content.meta(d)
        p = progress.get(d) or {}
        out.append({
            **m,
            "status": p.get("status", "locked"),
            "checks_passed": p.get("checks_passed", []),
        })
    return {"days": out, "streak": db.streak_info(), "total": len(days)}


@api.get("/days/{day}")
def get_day(day: int):
    b = content.bundle(day)
    if b is None:
        raise HTTPException(404, f"Day {day} 还没有内容")
    p = db.get_progress(day)
    if p["status"] == "locked":
        p = db.update_progress(day, status="opened")
        db.log_event(day, "open")
    return {**b, "progress": p}


@api.get("/days/{day}/solution")
def get_solution(day: int):
    src = content.solution(day)
    if not src:
        raise HTTPException(404, "这一天没有参考答案")
    db.update_progress(day, solution_seen=1)
    db.log_event(day, "solution_viewed")
    return {"solution": src}


@api.get("/my-data")
def my_data():
    """把她自己的学习记录导出成一份干净的数据集。

    第七章的 Day 65 会把这份数据喂进 Pyodide，让她画自己的学习曲线 ——
    用真实数据学数据可视化，说服力是编出来的假数据比不了的。
    """
    progress = db.all_progress()
    rows = []
    for d in content.available_days():
        m = content.meta(d) or {}
        p = progress.get(d) or {}
        rows.append({
            "day": d,
            "title": m.get("title", f"Day {d}"),
            "stage": m.get("stage", 1),
            "status": p.get("status", "locked"),
            "minutes": round((p.get("seconds_spent") or 0) / 60, 1),
            "runs": p.get("run_count", 0),
            "errors": p.get("error_count", 0),
            "hints": p.get("hints_used", 0),
            "completed_at": (p.get("completed_at") or "")[:10],
        })
    return {"records": rows, "streak": db.streak_info()}


@api.get("/cheatsheet")
def get_cheatsheet():
    done = [d for d, p in db.all_progress().items() if p["status"] != "locked"]
    return {"items": content.cheatsheet(max(done) if done else 0)}


# ---------------------------------------------------------------- 进度

class CodePayload(BaseModel):
    code: str


class CompletePayload(BaseModel):
    code: str = ""
    checks_passed: list[str] = []
    title: str = ""
    snippet: str = ""
    image: str | None = None


class EventPayload(BaseModel):
    kind: str = "info"
    payload: dict = {}


class ExercisePayload(BaseModel):
    exercise_id: str


@api.get("/progress")
def get_all_progress():
    return {"progress": db.all_progress(), "streak": db.streak_info()}


@api.put("/progress/{day}/code")
def save_code(day: int, body: CodePayload):
    return db.update_progress(day, code=body.code)


@api.post("/progress/{day}/run")
def record_run(day: int, body: EventPayload):
    db.bump(day, "run_count")
    if body.kind == "error":
        db.bump(day, "error_count")
        db.log_event(day, "error", body.payload)
    return {"ok": True}


@api.post("/progress/{day}/hint")
def record_hint(day: int, body: EventPayload):
    level = int(body.payload.get("level", 1))
    p = db.get_progress(day)
    if level > p["hints_used"]:
        db.update_progress(day, hints_used=level)
    db.log_event(day, "hint", {"level": level})
    return {"ok": True}


@api.post("/progress/{day}/exercise")
def record_exercise(day: int, body: ExercisePayload):
    p = db.get_progress(day)
    done = set(p["exercises_done"]) | {body.exercise_id}
    return db.update_progress(day, exercises_done=sorted(done))


@api.post("/progress/{day}/time")
def record_time(day: int, body: EventPayload):
    db.bump(day, "seconds_spent", int(body.payload.get("seconds", 0)))
    return {"ok": True}


@api.post("/progress/{day}/complete")
def complete_day(day: int, body: CompletePayload):
    p = db.get_progress(day)
    fields = {
        "status": "done",
        "checks_passed": body.checks_passed,
        "code": body.code or p["code"],
    }
    if not p["completed_at"]:
        fields["completed_at"] = db.now()
    p = db.update_progress(day, **fields)
    m = content.meta(day) or {}
    db.save_work(day, body.title or m.get("title", f"Day {day}"),
                 body.snippet, body.image)
    db.log_event(day, "complete")
    return {
        "progress": p,
        "streak": db.streak_info(),
        # 今天已经通关几天的内容了 —— 前端用它决定要不要温和提醒一句
        "done_today": db.completed_today(),
    }


# ---------------------------------------------------------------- 作品陈列馆

class WorkPayload(BaseModel):
    title: str = ""
    snippet: str = ""
    image: str | None = None


@api.get("/gallery")
def gallery():
    works = db.list_works()
    for w in works:
        m = content.meta(w["day"]) or {}
        w["hook"] = m.get("hook", "")
    return {"works": works, "streak": db.streak_info()}


@api.put("/gallery/{day}")
def upsert_work(day: int, body: WorkPayload):
    m = content.meta(day) or {}
    db.save_work(day, body.title or m.get("title", f"Day {day}"),
                 body.snippet, body.image)
    return {"ok": True}


@app.get("/healthz")
def healthz():
    return {"ok": True, "days": len(content.available_days())}


app.include_router(api)
