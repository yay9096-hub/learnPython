import ast

PURE = ["total_hp", "avg_atk", "strongest",
        "filter_by_element", "filter_by_atk", "find_member"]

SAMPLE = [
    {"name": "甲", "hp": 100, "atk": 50, "element": "火"},
    {"name": "乙", "hp": 200, "atk": 80, "element": "水"},
    {"name": "丙", "hp": 300, "atk": 60, "element": "火"},
]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    need = PURE + ["show_team", "show_report"]
    return all(f in _funcs(ctx) for f in need)


def pure_no_print(ctx):
    """算的函数里不许打印 —— 单一职责。"""
    fns = _funcs(ctx)
    for name in PURE:
        fn = fns.get(name)
        if fn is None:
            return False
        for n in ast.walk(fn):
            if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "print":
                return False
    return True


def total_ok(ctx):
    fn = ctx["ns"].get("total_hp")
    return callable(fn) and fn(SAMPLE) == 600 and fn([]) == 0


def avg_ok(ctx):
    fn = ctx["ns"].get("avg_atk")
    if not callable(fn):
        return False
    v = fn(SAMPLE)
    return abs(float(v) - 63.3) < 0.1 and fn([]) == 0


def strongest_ok(ctx):
    fn = ctx["ns"].get("strongest")
    if not callable(fn):
        return False
    r = fn(SAMPLE)
    return isinstance(r, dict) and r.get("name") == "乙" and fn([]) is None


def filter_element_ok(ctx):
    fn = ctx["ns"].get("filter_by_element")
    if not callable(fn):
        return False
    r = fn(SAMPLE, "火")
    if not isinstance(r, list) or len(r) != 2:
        return False
    names = {m["name"] for m in r}
    return names == {"甲", "丙"} and fn(SAMPLE, "雷") == []


def filter_atk_ok(ctx):
    fn = ctx["ns"].get("filter_by_atk")
    if not callable(fn):
        return False
    return (len(fn(SAMPLE, 60)) == 2 and len(fn(SAMPLE, 80)) == 1
            and len(fn(SAMPLE, 999)) == 0)


def filter_no_mutate(ctx):
    """筛选不该改动原队伍。"""
    fn = ctx["ns"].get("filter_by_element")
    if not callable(fn):
        return False
    data = [dict(m) for m in SAMPLE]
    fn(data, "火")
    return len(data) == 3


def find_ok(ctx):
    fn = ctx["ns"].get("find_member")
    if not callable(fn):
        return False
    r = fn(SAMPLE, "乙")
    return isinstance(r, dict) and r.get("hp") == 200 and fn(SAMPLE, "路人") is None


def report_uses_helpers(ctx):
    """show_report 要调用统计函数，而不是自己重算一遍。"""
    fn = _funcs(ctx).get("show_report")
    if fn is None:
        return False
    called = {getattr(n.func, "id", None) for n in ast.walk(fn)
              if isinstance(n, ast.Call)}
    return len(called & set(PURE)) >= 3


def empty_safe(ctx):
    """空队伍报告不能崩。"""
    fn = ctx["ns"].get("show_report")
    if not callable(fn):
        return False
    import io
    import sys
    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        fn([])
    except Exception:
        return False
    finally:
        sys.stdout = real
    return True


def main_shows_all(ctx):
    out = ctx["stdout"]
    return all(n in out for n in
               ["星野樱", "月见琉璃", "天野灯", "水城凛", "风见幽香"])


def main_filtered(ctx):
    """火属性筛选和攻击力筛选的结果都出现了。"""
    out = ctx["stdout"]
    return "火属性" in out or "风见幽香" in out


def main_empty_test(ctx):
    """主流程用空列表调过 show_report。"""
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "show_report":
            for a in n.args:
                if isinstance(a, ast.List) and not a.elts:
                    return True
    return False


CASES = [
    {
        "stdin": ["水城凛"],
        "checks": [
            {
                "id": "defined",
                "desc": "八个函数都定义了",
                "type": "custom", "fn": "all_defined",
                "fail": "六个「算」的函数 + show_team + show_report，函数名照抄",
            },
            {
                "id": "pure",
                "desc": "算的函数里没有 print",
                "type": "custom", "fn": "pure_no_print",
                "fail": "单一职责：`total_hp` / `avg_atk` / `strongest` / 三个筛选查找 "
                        "只负责算和 return，**一个 print 都不要写**",
            },
            {
                "id": "total",
                "desc": "total_hp 算对且空队返回 0",
                "type": "custom", "fn": "total_ok",
                "fail": "空列表要返回 0，不能报错",
            },
            {
                "id": "avg",
                "desc": "avg_atk 算对且空队不崩",
                "type": "custom", "fn": "avg_ok",
                "fail": "⚠️ 空队伍时 `len(team)` 是 0，直接除会崩。先 `if len(team) == 0: return 0`",
            },
            {
                "id": "strongest",
                "desc": "strongest 找对且空队返回 None",
                "type": "custom", "fn": "strongest_ok",
                "fail": "返回攻击力最高的那个**字典**；空队伍返回 `None`",
            },
            {
                "id": "filter-el",
                "desc": "filter_by_element 筛得对",
                "type": "custom", "fn": "filter_element_ok",
                "fail": "套路：建空列表 → 遍历 → `if` 符合就 append → `return`。"
                        "一个都没有时返回空列表",
            },
            {
                "id": "filter-atk",
                "desc": "filter_by_atk 用 >= 筛",
                "type": "custom", "fn": "filter_atk_ok",
                "fail": "「达到 min_atk」要用 `>=`，门槛值本身也算达标",
            },
            {
                "id": "no-mutate",
                "desc": "筛选不改动原队伍",
                "type": "custom", "fn": "filter_no_mutate",
                "fail": "筛选要**返回新列表**，不能在原队伍上 remove。原数据要永远安全",
            },
            {
                "id": "find",
                "desc": "find_member 找不到返回 None",
                "type": "custom", "fn": "find_ok",
                "fail": "找到就立刻 `return m`，循环跑完还没找到就 `return None`",
            },
            {
                "id": "report-reuse",
                "desc": "show_report 调用了统计函数",
                "type": "custom", "fn": "report_uses_helpers",
                "fail": "报告函数自己不该重算，要调 `total_hp(team)` 这些现成零件",
            },
            {
                "id": "empty-safe",
                "desc": "空队伍报告不会崩",
                "type": "custom", "fn": "empty_safe",
                "fail": "`show_report([])` 必须能正常跑完 —— 函数库要经得起各种输入",
            },
            {
                "id": "listed",
                "desc": "主流程打印了全队",
                "type": "custom", "fn": "main_shows_all",
                "fail": "用 `show_team(TEAM)` 把五个人都列出来",
            },
            {
                "id": "filtered",
                "desc": "主流程做了筛选并打印",
                "type": "custom", "fn": "main_filtered",
                "fail": "按属性筛一次、按攻击力筛一次，结果都要打印出来",
            },
            {
                "id": "empty-called",
                "desc": "主流程测试了空队伍",
                "type": "custom", "fn": "main_empty_test",
                "fail": "在最后写一句 `show_report([])`，亲眼确认它不会崩",
            },
            {
                "id": "query-found",
                "desc": "查到了水城凛",
                "type": "stdout_contains", "value": ["水城凛", "110"],
                "fail": "用 `find_member` 查到之后，把他的属性打印出来",
            },
        ],
    },
    {
        "stdin": ["路人甲"],
        "checks": [
            {
                "id": "not-found",
                "desc": "查不到的人有提示",
                "type": "stdout_contains", "value": "查无此人",
                "fail": "`find_member` 返回 None 时，要提示「查无此人」。"
                        "判断写 `if found is None:`",
            },
        ],
    },
]
