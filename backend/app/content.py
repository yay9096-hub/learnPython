"""课程内容读取。内容是磁盘上的 markdown / py 文件，改完刷新即可，不用重建镜像。"""
import json
import os
import re

CONTENT_DIR = os.environ.get("CONTENT_DIR", "/app/content")


def day_dir(day: int) -> str:
    return os.path.join(CONTENT_DIR, f"day-{day:03d}")


def _read(path: str, default: str = "") -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return default


def _read_json(path: str, default):
    raw = _read(path)
    if not raw.strip():
        return default
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return default


def available_days() -> list[int]:
    if not os.path.isdir(CONTENT_DIR):
        return []
    days = []
    for name in os.listdir(CONTENT_DIR):
        m = re.fullmatch(r"day-(\d{3})", name)
        if m and os.path.isfile(os.path.join(CONTENT_DIR, name, "meta.json")):
            days.append(int(m.group(1)))
    return sorted(days)


def meta(day: int) -> dict | None:
    m = _read_json(os.path.join(day_dir(day), "meta.json"), None)
    if m is None:
        return None
    m.setdefault("day", day)
    m.setdefault("title", f"Day {day}")
    m.setdefault("hook", "")
    m.setdefault("concepts", [])
    m.setdefault("estimated_minutes", 40)
    m.setdefault("needs_stdin", False)
    m.setdefault("uses_turtle", False)
    return m


def parse_hints(raw: str) -> list[dict]:
    """hints.md 用 `## 提示 N · 标题` 分级。"""
    if not raw.strip():
        return []
    parts = re.split(r"^##\s+", raw, flags=re.M)
    hints = []
    for part in parts:
        part = part.strip()
        if not part:
            continue
        head, _, body = part.partition("\n")
        hints.append({"title": head.strip(), "body": body.strip()})
    return hints


def bundle(day: int) -> dict | None:
    """一天的全部内容，**不含参考答案**（答案走单独接口，需要二次确认）。"""
    m = meta(day)
    if m is None:
        return None
    d = day_dir(day)
    return {
        "meta": m,
        "lesson": _read(os.path.join(d, "lesson.md")),
        "starter": _read(os.path.join(d, "starter.py")),
        "tests": _read(os.path.join(d, "tests.py")),
        "hints": parse_hints(_read(os.path.join(d, "hints.md"))),
        "exercises": _read_json(os.path.join(d, "exercises.json"), []),
    }


def solution(day: int) -> str:
    return _read(os.path.join(day_dir(day), "solution.py"))


def cheatsheet(up_to_day: int) -> list[dict]:
    """速查手册只包含已经学过的知识点，避免看到没学的被吓到。"""
    items = []
    for d in available_days():
        if d > up_to_day:
            break
        m = meta(d) or {}
        for c in m.get("cheatsheet", []):
            items.append({**c, "day": d})
    return items
