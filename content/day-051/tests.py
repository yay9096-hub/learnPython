import ast
import json
import os

NEEDED = ["load_records", "save_records", "check_in", "total_minutes",
          "longest_streak", "current_streak", "show_records"]

SETUP = """
import os
if os.path.exists("打卡记录.json"):
    os.remove("打卡记录.json")
"""

SAMPLE = [
    {"date": "2026-09-01", "minutes": 40, "topic": "a"},
    {"date": "2026-09-02", "minutes": 35, "topic": "b"},
    {"date": "2026-09-04", "minutes": 50, "topic": "c"},
    {"date": "2026-09-05", "minutes": 45, "topic": "d"},
    {"date": "2026-09-06", "minutes": 40, "topic": "e"},
]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def uses_datetime(ctx):
    src = ctx["code"]
    return "date" in src and ("fromisoformat" in src or "strptime" in src)


def missing_returns_empty(ctx):
    fn = ctx["ns"].get("load_records")
    if not callable(fn):
        return False
    try:
        return fn("肯定不存在_xyz.json") == []
    except Exception:
        return False


def total_ok(ctx):
    fn = ctx["ns"].get("total_minutes")
    if not callable(fn):
        return False
    return fn(SAMPLE) == 210 and fn([]) == 0


def no_duplicate(ctx):
    fn = ctx["ns"].get("check_in")
    if not callable(fn):
        return False
    data = [dict(r) for r in SAMPLE]
    before = len(data)
    fn(data, "2026-09-06", 999, "重复")
    if len(data) != before:
        return False
    fn(data, "2026-09-09", 30, "新的")
    return len(data) == before + 1


def check_in_shape(ctx):
    fn = ctx["ns"].get("check_in")
    if not callable(fn):
        return False
    data = []
    fn(data, "2026-01-01", 25, "测试")
    if len(data) != 1:
        return False
    r = data[0]
    return (r.get("date") == "2026-01-01" and r.get("minutes") == 25
            and r.get("topic") == "测试")


def longest_ok(ctx):
    fn = ctx["ns"].get("longest_streak")
    if not callable(fn):
        return False
    # 09-01,02 断 03，04,05,06 -> 最长 3
    if fn(SAMPLE) != 3:
        return False
    if fn([]) != 0:
        return False
    one = [{"date": "2026-09-01", "minutes": 1, "topic": "x"}]
    return fn(one) == 1


def longest_dedups(ctx):
    """同一天出现两次不该被算成连续 2 天。"""
    fn = ctx["ns"].get("longest_streak")
    if not callable(fn):
        return False
    dup = [
        {"date": "2026-09-01", "minutes": 1, "topic": "x"},
        {"date": "2026-09-01", "minutes": 1, "topic": "y"},
    ]
    return fn(dup) == 1


def current_ok(ctx):
    fn = ctx["ns"].get("current_streak")
    if not callable(fn):
        return False
    # 从 09-06 往回：06,05,04 连着，03 断 -> 3
    if fn(SAMPLE, "2026-09-06") != 3:
        return False
    # 今天没打卡 -> 0
    if fn(SAMPLE, "2026-09-08") != 0:
        return False
    return fn([], "2026-09-06") == 0


def saved_and_reloaded(ctx):
    """跑完之后文件里应该有 6 条（5 天 + 玩家那天）。"""
    if not os.path.exists("打卡记录.json"):
        return False
    try:
        with open("打卡记录.json", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False
    return isinstance(data, list) and len(data) == 6


def user_minutes_recorded(ctx):
    try:
        with open("打卡记录.json", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False
    return any(r.get("minutes") == 55 for r in data)


def stats_printed(ctx):
    out = ctx["stdout"]
    return "210" in out and "3" in out


def sorted_display(ctx):
    """显示时按日期排序：09-01 要出现在 09-06 前面。"""
    out = ctx["stdout"]
    a = out.find("2026-09-01")
    b = out.rfind("2026-09-06")
    return a >= 0 and b >= 0 and a < b


def dup_tested(ctx):
    return "重复" in ctx["stdout"]


CASES = [
    {
        "setup": SETUP,
        "stdin": ["55"],
        "checks": [
            {"id": "defined", "desc": "七个函数都定义了",
             "type": "custom", "fn": "all_defined",
             "fail": "load_records / save_records / check_in / total_minutes / "
                     "longest_streak / current_streak / show_records"},
            {"id": "datetime", "desc": "用了 datetime 处理日期",
             "type": "custom", "fn": "uses_datetime",
             "fail": "算连续要把日期文字转成真正的日期："
                     "`date.fromisoformat(\"2026-09-01\")`"},
            {"id": "missing", "desc": "文件不存在返回空列表",
             "type": "custom", "fn": "missing_returns_empty",
             "fail": "`load_records` 遇到不存在的文件要返回 `[]`"},
            {"id": "shape", "desc": "打卡记录结构正确",
             "type": "custom", "fn": "check_in_shape",
             "fail": "每条形如 `{\"date\": ..., \"minutes\": ..., \"topic\": ...}`，键名照抄"},
            {"id": "no-dup", "desc": "同一天不会重复打卡",
             "type": "custom", "fn": "no_duplicate",
             "fail": "加之前先遍历检查有没有这个日期，有就直接 return"},
            {"id": "total", "desc": "总时长算对了（210 分钟）",
             "type": "custom", "fn": "total_ok",
             "fail": "40+35+50+45+40 = 210。空列表要返回 0"},
            {"id": "longest", "desc": "最长连续算对了（3 天）",
             "type": "custom", "fn": "longest_ok",
             "fail": "09-01、09-02 连着（2 天），09-03 断了，"
                     "09-04~09-06 连着（3 天）—— 最长是 **3**。空记录返回 0"},
            {"id": "dedup", "desc": "同一天出现两次不算连续",
             "type": "custom", "fn": "longest_dedups",
             "fail": "算之前要先 `set()` 去重，否则一天打两次卡会被当成连续 2 天"},
            {"id": "current", "desc": "当前连击算对了",
             "type": "custom", "fn": "current_ok",
             "fail": "从今天往回数：09-06、05、04 连着 = **3**。"
                     "今天没打卡要返回 **0**"},
            {"id": "sorted", "desc": "显示时按日期排序",
             "type": "custom", "fn": "sorted_display",
             "fail": "`sorted(records, key=lambda r: r[\"date\"])` —— "
                     "日期是 YYYY-MM-DD 格式，直接按文字排就是按时间排"},
            {"id": "stats", "desc": "打印了总时长和连击",
             "type": "custom", "fn": "stats_printed",
             "fail": "总时长、最长连击、当前连击都要打印出来"},
            {"id": "dup-test", "desc": "演示了重复打卡被挡住",
             "type": "custom", "fn": "dup_tested",
             "fail": "故意给同一天打两次卡，打印前后条数证明没有重复"},
            {"id": "saved", "desc": "存盘后共 6 条记录",
             "type": "custom", "fn": "saved_and_reloaded",
             "fail": "补录 5 天 + 玩家打卡 1 天 = 6 条，用 `save_records` 存进 json"},
            {"id": "user", "desc": "玩家输入的时长记进去了",
             "type": "custom", "fn": "user_minutes_recorded",
             "fail": "把 `input()` 拿到的分钟数（记得 int 转换）打卡进去",
            },
        ],
    }
]
