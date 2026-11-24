import ast
import os

NEEDED = ["write_lines_csv", "read_csv", "add_total", "subject_avg",
          "top_student", "sort_by_total", "write_csv"]

SETUP = """
import os
for _n in ["成绩.csv", "排名.csv"]:
    if os.path.exists(_n):
        os.remove(_n)
"""

# 星野樱 259 / 月见琉璃 264 / 天野灯 225 / 水城凛 283 / 夜刀神澪 218
SAMPLE = [
    {"姓名": "甲", "语文": 80, "数学": 90, "英语": 70, "总分": 240},
    {"姓名": "乙", "语文": 60, "数学": 70, "英语": 80, "总分": 210},
    {"姓名": "丙", "语文": 100, "数学": 50, "英语": 90, "总分": 240},
]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def read_csv_shape(ctx):
    """读出来是列表套字典，键就是表头。"""
    fn = ctx["ns"].get("read_csv")
    if not callable(fn):
        return False
    rows = fn("成绩.csv")
    if not isinstance(rows, list) or len(rows) != 5:
        return False
    r = rows[0]
    return (isinstance(r, dict) and r.get("姓名") == "星野樱"
            and set(["姓名", "语文", "数学", "英语"]) <= set(r.keys()))


def read_csv_converts(ctx):
    """数字字段必须转成 int，不然排序会按文字排。"""
    fn = ctx["ns"].get("read_csv")
    if not callable(fn):
        return False
    rows = fn("成绩.csv")
    r = rows[0]
    return (isinstance(r["语文"], int) and isinstance(r["数学"], int)
            and isinstance(r["姓名"], str))


def uses_zip_or_index(ctx):
    src = ctx["code"]
    return "zip(" in src or "header" in src


def total_ok(ctx):
    fn = ctx["ns"].get("add_total")
    if not callable(fn):
        return False
    data = [{"姓名": "x", "语文": 10, "数学": 20, "英语": 30}]
    fn(data)
    return data[0].get("总分") == 60


def avg_ok(ctx):
    fn = ctx["ns"].get("subject_avg")
    if not callable(fn):
        return False
    v = fn(SAMPLE, "语文")
    return abs(float(v) - 80.0) < 0.05


def avg_empty_safe(ctx):
    fn = ctx["ns"].get("subject_avg")
    if not callable(fn):
        return False
    try:
        return fn([], "语文") == 0
    except Exception:
        return False


def top_ok(ctx):
    fn = ctx["ns"].get("top_student")
    if not callable(fn):
        return False
    r = fn(SAMPLE)
    return isinstance(r, dict) and r["总分"] == 240 and fn([]) is None


def sort_ok(ctx):
    fn = ctx["ns"].get("sort_by_total")
    if not callable(fn):
        return False
    data = [dict(r) for r in SAMPLE]
    out = fn(data)
    if not isinstance(out, list) or len(out) != 3:
        return False
    totals = [r["总分"] for r in out]
    return totals == [240, 240, 210]


def sort_no_mutate(ctx):
    """排序要返回新列表，不改原来的。"""
    fn = ctx["ns"].get("sort_by_total")
    if not callable(fn):
        return False
    data = [dict(r) for r in SAMPLE]
    fn(data)
    return data[0]["姓名"] == "甲"


def ranking_written(ctx):
    """排名.csv 存在、有表头、第一行是水城凛。"""
    if not os.path.exists("排名.csv"):
        return False
    with open("排名.csv", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    if len(lines) != 6:
        return False
    if "姓名" not in lines[0]:
        return False
    return lines[1].startswith("水城凛")


def ranking_roundtrip(ctx):
    """写出去的 CSV 能被自己的 read_csv 读回来。"""
    fn = ctx["ns"].get("read_csv")
    if not callable(fn):
        return False
    rows = fn("排名.csv")
    return (isinstance(rows, list) and len(rows) == 5
            and rows[0].get("姓名") == "水城凛"
            and isinstance(rows[0].get("总分"), int))


def avgs_printed(ctx):
    """三科平均：语文 82.0 数学 85.0 英语 82.8"""
    out = ctx["stdout"]
    return "82" in out and "85" in out


def ranked_output(ctx):
    """排行榜第一名是水城凛。"""
    import re
    return re.search(r"第\s*1\s*名[^\n]*水城凛", ctx["stdout"]) is not None


def query_found(ctx):
    out = ctx["stdout"]
    return "月见琉璃" in out and "264" in out


CASES = [
    {
        "setup": SETUP,
        "stdin": ["月见琉璃"],
        "checks": [
            {"id": "defined", "desc": "七个函数都定义了",
             "type": "custom", "fn": "all_defined",
             "fail": "write_lines_csv / read_csv / add_total / subject_avg / "
                     "top_student / sort_by_total / write_csv"},
            {"id": "shape", "desc": "read_csv 返回列表套字典",
             "type": "custom", "fn": "read_csv_shape",
             "fail": "第一行是表头，用它当字典的键。5 名学生应该得到 5 个字典"},
            {"id": "convert", "desc": "数字字段转成了 int",
             "type": "custom", "fn": "read_csv_converts",
             "fail": "⚠️ CSV 读出来全是文字。用 `value.isdigit()` 判断，"
                     "是数字就 `int(value)` —— 否则排序会按文字排，「9」排在「10」前面"},
            {"id": "zip", "desc": "用表头和值配对",
             "type": "custom", "fn": "uses_zip_or_index",
             "fail": "用 `zip(header, parts)` 把表头和这一行的值配成对（Day 33 学的）"},
            {"id": "total", "desc": "add_total 算对了",
             "type": "custom", "fn": "total_ok",
             "fail": "给每行加一个 `总分` 字段，值是三科之和"},
            {"id": "avg", "desc": "subject_avg 算对了",
             "type": "custom", "fn": "avg_ok",
             "fail": "某一科的平均分要 `round(..., 1)`"},
            {"id": "avg-empty", "desc": "空表求平均不崩",
             "type": "custom", "fn": "avg_empty_safe",
             "fail": "空列表时先返回 0，别除以零"},
            {"id": "top", "desc": "top_student 找对且空表返回 None",
             "type": "custom", "fn": "top_ok",
             "fail": "返回总分最高的那个**字典**；空表返回 `None`"},
            {"id": "sort", "desc": "按总分从高到低排序",
             "type": "custom", "fn": "sort_ok",
             "fail": "`sorted(rows, key=lambda r: r[\"总分\"], reverse=True)`"},
            {"id": "no-mutate", "desc": "排序不改动原列表",
             "type": "custom", "fn": "sort_no_mutate",
             "fail": "用 `sorted(...)` 返回新列表，不要用 `rows.sort()` 改原数据"},
            {"id": "written", "desc": "排名.csv 写出来了",
             "type": "custom", "fn": "ranking_written",
             "fail": "先写表头行，再写 5 行数据。第一行数据应该是水城凛（283 分）"},
            {"id": "roundtrip", "desc": "写出去的能自己读回来",
             "type": "custom", "fn": "ranking_roundtrip",
             "fail": "写 CSV 时每个值要 `str(...)`，读回来才是合法的 CSV"},
            {"id": "avgs", "desc": "打印了三科平均分",
             "type": "custom", "fn": "avgs_printed",
             "fail": "语文 82.0、数学 85.0、英语 82.8，三科都要打印"},
            {"id": "ranked", "desc": "排行榜带名次且顺序正确",
             "type": "custom", "fn": "ranked_output",
             "fail": "用 `enumerate(ranked, start=1)` 加名次，第 1 名应该是水城凛"},
            {"id": "query", "desc": "查到了月见琉璃的成绩",
             "type": "custom", "fn": "query_found",
             "fail": "查到之后把各科成绩和总分（264）都打印出来"},
        ],
    },
    {
        "setup": SETUP,
        "stdin": ["路人甲"],
        "checks": [
            {"id": "not-found", "desc": "查不到的人有提示",
             "type": "stdout_contains", "value": "查无此人",
             "fail": "找不到时提示「查无此人」，别崩"},
        ],
    },
]
