import ast
import json
import os

NEEDED = ["load_book", "save_book", "validate_amount", "validate_category",
          "add_record", "total_by_kind", "balance", "group_by_month",
          "group_by_category", "top_category", "show_report", "export_csv"]

SETUP = """
import os
for _n in ["账本.json", "账本.csv"]:
    if os.path.exists(_n):
        os.remove(_n)
"""

SAMPLE = [
    {"date": "2026-08-05", "type": "收入", "category": "零花钱", "amount": 100, "note": ""},
    {"date": "2026-08-12", "type": "支出", "category": "零食", "amount": 12.5, "note": ""},
    {"date": "2026-08-20", "type": "支出", "category": "文具", "amount": 28, "note": ""},
    {"date": "2026-09-01", "type": "收入", "category": "零花钱", "amount": 100, "note": ""},
    {"date": "2026-09-03", "type": "支出", "category": "零食", "amount": 8.5, "note": ""},
    {"date": "2026-09-05", "type": "支出", "category": "娱乐", "amount": 45, "note": ""},
]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def validators_raise(ctx):
    """两个 validate 里必须有 raise —— Day 46 的分工。"""
    fns = _funcs(ctx)
    for name in ["validate_amount", "validate_category"]:
        fn = fns.get(name)
        if fn is None:
            return False
        if not any(isinstance(n, ast.Raise) for n in ast.walk(fn)):
            return False
    return True


def amount_ok(ctx):
    fn = ctx["ns"].get("validate_amount")
    if not callable(fn):
        return False
    if abs(fn("12.5") - 12.5) > 1e-9:
        return False
    for bad in ["abc", "0", "-5", ""]:
        try:
            fn(bad)
            return False
        except ValueError:
            continue
        except Exception:
            return False
    return True


def category_ok(ctx):
    fn = ctx["ns"].get("validate_category")
    if not callable(fn):
        return False
    if fn("零食") != "零食":
        return False
    try:
        fn("买房")
        return False
    except ValueError as e:
        return "零食" in str(e)
    except Exception:
        return False


def missing_returns_empty(ctx):
    fn = ctx["ns"].get("load_book")
    if not callable(fn):
        return False
    try:
        return fn("肯定不存在_xyz.json") == []
    except Exception:
        return False


def totals_ok(ctx):
    fn = ctx["ns"].get("total_by_kind")
    if not callable(fn):
        return False
    return (abs(fn(SAMPLE, "收入") - 200) < 0.01
            and abs(fn(SAMPLE, "支出") - 94) < 0.01)


def balance_ok(ctx):
    fn = ctx["ns"].get("balance")
    if not callable(fn):
        return False
    return abs(fn(SAMPLE) - 106) < 0.01 and fn([]) == 0


def month_ok(ctx):
    fn = ctx["ns"].get("group_by_month")
    if not callable(fn):
        return False
    g = fn(SAMPLE)
    if not isinstance(g, dict) or set(g.keys()) != {"2026-08", "2026-09"}:
        return False
    return abs(g["2026-08"] - 40.5) < 0.01 and abs(g["2026-09"] - 53.5) < 0.01


def category_group_ok(ctx):
    """收入分类不该混进支出统计里。"""
    fn = ctx["ns"].get("group_by_category")
    if not callable(fn):
        return False
    g = fn(SAMPLE)
    if not isinstance(g, dict):
        return False
    if "零花钱" in g:
        return False
    return (abs(g.get("零食", 0) - 21) < 0.01
            and abs(g.get("娱乐", 0) - 45) < 0.01
            and abs(g.get("文具", 0) - 28) < 0.01)


def top_ok(ctx):
    fn = ctx["ns"].get("top_category")
    if not callable(fn):
        return False
    return fn(SAMPLE) == "娱乐" and fn([]) is None


def saved_json(ctx):
    if not os.path.exists("账本.json"):
        return False
    try:
        with open("账本.json", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False
    return isinstance(data, list) and len(data) == 7


def csv_exported(ctx):
    if not os.path.exists("账本.csv"):
        return False
    with open("账本.csv", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    return len(lines) == 8 and "date" in lines[0] and "amount" in lines[0]


def report_printed(ctx):
    out = ctx["stdout"]
    return "收入" in out and "支出" in out and "结余" in out


def months_shown(ctx):
    out = ctx["stdout"]
    return "2026-08" in out and "2026-09" in out


def top_marked(ctx):
    return "花得最多" in ctx["stdout"]


def user_record_ok(ctx):
    try:
        with open("账本.json", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return False
    return any(abs(r.get("amount", 0) - 15.5) < 0.01 for r in data)


def survived(ctx):
    return ctx["error"] is None


CASES = [
    {
        "setup": SETUP,
        "stdin": ["零食", "15.5", "薯片"],
        "checks": [
            {"id": "defined", "desc": "十二个函数都定义了",
             "type": "custom", "fn": "all_defined",
             "fail": "对照任务表检查函数名，一个都不能少"},
            {"id": "raise", "desc": "两个 validate 只 raise 不 try",
             "type": "custom", "fn": "validators_raise",
             "fail": "Day 46 的分工：校验函数只管抛错，接住交给主流程"},
            {"id": "amount", "desc": "金额校验正确",
             "type": "custom", "fn": "amount_ok",
             "fail": "12.5 要返回 12.5；abc、0、-5、空串都要抛 ValueError"},
            {"id": "category", "desc": "分类校验且列出可选值",
             "type": "custom", "fn": "category_ok",
             "fail": "不认识的分类要抛 ValueError，**错误信息里要列出可选分类**"},
            {"id": "missing", "desc": "账本不存在返回空列表",
             "type": "custom", "fn": "missing_returns_empty",
             "fail": "第一次打开时文件还没有，要返回空列表"},
            {"id": "totals", "desc": "收入支出总额算对",
             "type": "custom", "fn": "totals_ok",
             "fail": "收入 200、支出 94（12.5 + 28 + 8.5 + 45）"},
            {"id": "balance", "desc": "结余算对且空账本为 0",
             "type": "custom", "fn": "balance_ok",
             "fail": "200 - 94 = **106**。空账本要返回 0"},
            {"id": "month", "desc": "按月统计正确",
             "type": "custom", "fn": "month_ok",
             "fail": "8 月支出 40.5、9 月支出 53.5。月份用日期的前 7 个字符切出来，"
                     "而且**只统计支出**"},
            {"id": "cat-group", "desc": "按分类统计只算支出",
             "type": "custom", "fn": "category_group_ok",
             "fail": "零食 21、文具 28、娱乐 45。零花钱是收入，**不该出现**在支出统计里"},
            {"id": "top", "desc": "找对花钱最多的分类",
             "type": "custom", "fn": "top_ok",
             "fail": "娱乐 45 元最多。空账本返回 None"},
            {"id": "report", "desc": "报表打印了三项汇总",
             "type": "custom", "fn": "report_printed",
             "fail": "收入、支出、结余都要打印出来"},
            {"id": "months-shown", "desc": "按月统计显示了两个月",
             "type": "custom", "fn": "months_shown",
             "fail": "2026-08 和 2026-09 都要显示"},
            {"id": "top-marked", "desc": "标出了花得最多的分类",
             "type": "custom", "fn": "top_marked",
             "fail": "在花钱最多的那一行后面标一句「← 花得最多」"},
            {"id": "user", "desc": "玩家记的那笔存进去了",
             "type": "custom", "fn": "user_record_ok",
             "fail": "校验通过后要 add_record 加进去，金额 15.5"},
            {"id": "saved", "desc": "存盘后共 7 条",
             "type": "custom", "fn": "saved_json",
             "fail": "补录 6 笔 + 玩家 1 笔 = 7 条，用 save_book 存进 json"},
            {"id": "csv", "desc": "导出的 CSV 有表头和 7 行数据",
             "type": "custom", "fn": "csv_exported",
             "fail": "先写表头行，再写 7 行数据，一共 8 行"},
            {"id": "survive", "desc": "全程没有崩溃",
             "type": "custom", "fn": "survived",
             "fail": "校验失败要用 try 接住，不能让程序中断"},
        ],
    },
    {
        "setup": SETUP,
        "stdin": ["买房", "15.5", "备注"],
        "checks": [
            {"id": "bad-cat", "desc": "非法分类被拦下且不崩",
             "type": "stdout_contains", "value": "记不了",
             "fail": "分类不认识时要提示「记不了」并说明原因，程序继续跑完"},
        ],
    },
    {
        "setup": SETUP,
        "stdin": ["零食", "不是数字", "备注"],
        "checks": [
            {"id": "bad-amount", "desc": "非法金额被拦下且不崩",
             "type": "stdout_contains", "value": "记不了",
             "fail": "金额不是数字时同样要被 validate_amount 挡住"},
        ],
    },
]
