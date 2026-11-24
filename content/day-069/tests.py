import ast
import os

NEEDED = ["load_records", "overview", "by_stage", "bar",
          "highlights", "build_report", "draw_charts"]

SETUP = '''
import json, os
for _n in ["学习报告.txt", "学习图表.png"]:
    if os.path.exists(_n):
        os.remove(_n)
_rows = [
    {"day": 1, "title": "角色出场卡", "stage": 1, "status": "done",
     "minutes": 42.0, "runs": 12, "errors": 3, "hints": 1, "completed_at": "2026-09-01"},
    {"day": 2, "title": "角色属性面板", "stage": 1, "status": "done",
     "minutes": 35.0, "runs": 9, "errors": 0, "hints": 0, "completed_at": "2026-09-02"},
    {"day": 3, "title": "伤害计算器", "stage": 1, "status": "done",
     "minutes": 58.0, "runs": 20, "errors": 7, "hints": 2, "completed_at": "2026-09-02"},
    {"day": 4, "title": "入学登记处", "stage": 1, "status": "locked",
     "minutes": 0, "runs": 0, "errors": 0, "hints": 0, "completed_at": ""},
    {"day": 11, "title": "魔法结界", "stage": 2, "status": "done",
     "minutes": 40.0, "runs": 14, "errors": 4, "hints": 1, "completed_at": "2026-09-03"},
    {"day": 12, "title": "属性克制判定", "stage": 2, "status": "locked",
     "minutes": 0, "runs": 0, "errors": 0, "hints": 0, "completed_at": ""},
]
with open("我的学习记录.json", "w", encoding="utf-8") as _f:
    json.dump(_rows, _f, ensure_ascii=False, indent=2)
'''

# done 四天：42+35+58+40 = 175 分钟，平均 43.8
# runs 12+9+20+14 = 55，errors 3+0+7+4 = 14，报错率 25.5%
# 第 1 章：3/4 完成、135 分钟；第 2 章：1/2 完成、40 分钟
# 最投入 Day 3（58），最顺 Day 2（0 错），最费劲 Day 3（7 错）


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def load_missing(ctx):
    fn = ctx["ns"].get("load_records")
    if not callable(fn):
        return False
    try:
        return fn("肯定不存在_xyz.json") == []
    except Exception:
        return False


def _records(ctx):
    fn = ctx["ns"].get("load_records")
    if not callable(fn):
        return None
    try:
        return fn("我的学习记录.json")
    except Exception:
        return None


def overview_ok(ctx):
    fn = ctx["ns"].get("overview")
    recs = _records(ctx)
    if not callable(fn) or recs is None:
        return False
    o = fn(recs)
    if not isinstance(o, dict):
        return False
    return (o.get("done") == 4 and o.get("total") == 6
            and abs(float(o.get("minutes", 0)) - 175) < 0.5
            and abs(float(o.get("avg", 0)) - 43.8) < 0.2
            and o.get("runs") == 55 and o.get("errors") == 14
            and abs(float(o.get("rate", 0)) - 25.5) < 0.2)


def overview_empty_safe(ctx):
    fn = ctx["ns"].get("overview")
    if not callable(fn):
        return False
    try:
        o = fn([])
    except Exception:
        return False
    return o.get("done") == 0 and float(o.get("avg", -1)) == 0 and float(o.get("rate", -1)) == 0


def by_stage_ok(ctx):
    fn = ctx["ns"].get("by_stage")
    recs = _records(ctx)
    if not callable(fn) or recs is None:
        return False
    s = fn(recs)
    if not isinstance(s, dict) or 1 not in s or 2 not in s:
        return False
    d1, t1, m1 = s[1]
    d2, t2, m2 = s[2]
    return (d1 == 3 and t1 == 4 and abs(m1 - 135) < 0.5
            and d2 == 1 and t2 == 2 and abs(m2 - 40) < 0.5)


def bar_ok(ctx):
    fn = ctx["ns"].get("bar")
    if not callable(fn):
        return False
    full = fn(10, 10, 10)
    half = fn(5, 10, 10)
    zero = fn(0, 10, 10)
    if not all(isinstance(x, str) for x in [full, half, zero]):
        return False
    return full.count("█") == 10 and half.count("█") == 5 and zero.count("█") == 0


def bar_no_divzero(ctx):
    fn = ctx["ns"].get("bar")
    if not callable(fn):
        return False
    try:
        return isinstance(fn(0, 0, 10), str)
    except Exception:
        return False


def highlights_ok(ctx):
    fn = ctx["ns"].get("highlights")
    recs = _records(ctx)
    if not callable(fn) or recs is None:
        return False
    longest, smoothest, hardest = fn(recs)
    return (longest["day"] == 3 and smoothest["day"] == 2
            and hardest["day"] == 3)


def highlights_empty_safe(ctx):
    fn = ctx["ns"].get("highlights")
    if not callable(fn):
        return False
    try:
        a, b, c = fn([])
    except Exception:
        return False
    return a is None and b is None and c is None


def report_returns_string(ctx):
    """build_report 只返回字符串，不许自己 print。"""
    fn = ctx["ns"].get("build_report")
    recs = _records(ctx)
    if not callable(fn) or recs is None:
        return False
    r = fn(recs)
    return isinstance(r, str) and len(r) > 100


def report_no_print(ctx):
    fn = _funcs(ctx).get("build_report")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "print":
            return False
    return True


def report_has_sections(ctx):
    fn = ctx["ns"].get("build_report")
    recs = _records(ctx)
    if not callable(fn) or recs is None:
        return False
    r = fn(recs)
    return ("总览" in r and "各章" in r and "记录" in r
            and "175" in r and "伤害计算器" in r)


def report_has_bars(ctx):
    fn = ctx["ns"].get("build_report")
    recs = _records(ctx)
    if not callable(fn) or recs is None:
        return False
    return "█" in fn(recs)


def report_file_written(ctx):
    if not os.path.exists("学习报告.txt"):
        return False
    with open("学习报告.txt", encoding="utf-8") as f:
        text = f.read()
    return "总览" in text and "175" in text


def chart_file_written(ctx):
    return os.path.exists("学习图表.png") and os.path.getsize("学习图表.png") > 1000


def uses_savefig(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "savefig":
                return True
    return False


def four_charts(ctx):
    return ctx["plot"].get("axes", 0) >= 4 or chart_file_written(ctx)


def chart_titles(ctx):
    return len(ctx["plot"].get("titles", [])) >= 4 or chart_file_written(ctx)


def printed_report(ctx):
    out = ctx["stdout"]
    return "总览" in out and "175" in out


def survived(ctx):
    return ctx["error"] is None


CASES = [
    {
        "setup": SETUP,
        "checks": [
            {"id": "defined", "desc": "七个函数都定义了",
             "type": "custom", "fn": "all_defined",
             "fail": "load_records / overview / by_stage / bar / "
                     "highlights / build_report / draw_charts"},
            {"id": "load", "desc": "文件不存在返回空列表",
             "type": "custom", "fn": "load_missing",
             "fail": "接住 `FileNotFoundError`，返回 `[]`"},
            {"id": "overview", "desc": "总览七项都算对",
             "type": "custom", "fn": "overview_ok",
             "fail": "完成 4/6，总时长 **175**，平均 **43.8**，"
                     "运行 **55**，报错 **14**，报错率 **25.5%**"},
            {"id": "overview-empty", "desc": "空数据时总览不崩",
             "type": "custom", "fn": "overview_empty_safe",
             "fail": "没有完成的天时，平均和报错率都要返回 0，别除以零"},
            {"id": "stage", "desc": "分章汇总正确",
             "type": "custom", "fn": "by_stage_ok",
             "fail": "第 1 章 3/4 完成、135 分钟；第 2 章 1/2 完成、40 分钟。"
                     "⚠️ **总数要算上没完成的天**，时长只算完成的"},
            {"id": "bar", "desc": "进度条长度正确",
             "type": "custom", "fn": "bar_ok",
             "fail": "满格 10 个 █、一半 5 个、零个 0 个"},
            {"id": "bar-zero", "desc": "total 为 0 时进度条不崩",
             "type": "custom", "fn": "bar_no_divzero",
             "fail": "开头先 `if total <= 0: return ...`"},
            {"id": "highlights", "desc": "三个记录都找对了",
             "type": "custom", "fn": "highlights_ok",
             "fail": "最投入 Day 3（58 分钟）、最顺 Day 2（0 次报错）、"
                     "最费劲 Day 3（7 次报错）"},
            {"id": "highlights-empty", "desc": "空数据返回三个 None",
             "type": "custom", "fn": "highlights_empty_safe",
             "fail": "`return None, None, None`"},
            {"id": "report-str", "desc": "build_report 返回字符串",
             "type": "custom", "fn": "report_returns_string",
             "fail": "用 `lines = []` 一路 append，最后 `\"\\n\".join(lines)` 返回"},
            {"id": "report-noprint", "desc": "build_report 内部没有 print",
             "type": "custom", "fn": "report_no_print",
             "fail": "它只负责**生成文字**，打印交给主流程 —— "
                     "这样才能同时打印和写文件"},
            {"id": "report-content", "desc": "报告三个板块都有",
             "type": "custom", "fn": "report_has_sections",
             "fail": "总览、各章进度、记录，三块都要有，"
                     "而且数字要对得上"},
            {"id": "report-bars", "desc": "报告里有文字进度条",
             "type": "custom", "fn": "report_has_bars",
             "fail": "各章进度那一段要用 `bar(...)` 画出来"},
            {"id": "report-file", "desc": "报告写进了文件",
             "type": "custom", "fn": "report_file_written",
             "fail": "`with open(\"学习报告.txt\", \"w\", encoding=\"utf-8\") as f:`"},
            {"id": "savefig", "desc": "用了 savefig 存图",
             "type": "custom", "fn": "uses_savefig",
             "fail": "`plt.savefig(filename, dpi=110)` —— "
                     "⚠️ 要写在 `plt.show()` **之前**"},
            {"id": "chart-file", "desc": "图片文件真的存出来了",
             "type": "custom", "fn": "chart_file_written",
             "fail": "跑完之后「📁 文件」里应该出现 `学习图表.png`"},
            {"id": "four", "desc": "画了四格图",
             "type": "custom", "fn": "four_charts",
             "fail": "`plt.subplot(2, 2, 1)` 到 `(2, 2, 4)`"},
            {"id": "titles", "desc": "四格都有标题",
             "type": "custom", "fn": "chart_titles",
             "fail": "每格一句 `plt.title(...)`"},
            {"id": "printed", "desc": "报告也打印到终端了",
             "type": "custom", "fn": "printed_report",
             "fail": "`print(report)` —— 同一份文字既打印又写文件"},
            {"id": "survive", "desc": "全程没有崩溃",
             "type": "custom", "fn": "survived",
             "fail": "真实数据里有 minutes 为 0、runs 为 0 的天，处处要防除零"},
        ],
    }
]
