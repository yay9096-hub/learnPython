TOTALS = {"星野樱": 259, "月见琉璃": 264, "天野灯": 225,
          "水城凛": 283, "夜刀神澪": 218, "风见幽香": 259}


def totals_added(ctx):
    st = ctx["ns"].get("students")
    if not isinstance(st, list) or len(st) != 6:
        return False
    for s in st:
        if "total" not in s or s["total"] != TOTALS.get(s.get("name")):
            return False
    return True


def report_rows(ctx):
    """成绩单里每个人一行，且带三科和总分。"""
    import re
    out = ctx["stdout"]
    return re.search(r"水城凛[^\n]*90[^\n]*99[^\n]*94[^\n]*283", out) is not None


def subject_stats(ctx):
    """数学：最高 99 最低 71 平均 85.5，三个数要在同一行。"""
    import re
    for line in ctx["stdout"].splitlines():
        if "99" in line and "71" in line and "85.5" in line:
            return True
    return False


def all_subjects(ctx):
    out = ctx["stdout"]
    return all(x in out for x in ["82.3", "85.5", "83.5"])


def uses_sort_key(ctx):
    return "key=lambda" in ctx["code"].replace(" ", "")


def ranked(ctx):
    """排序后第一个是水城凛，最后一个是夜刀神澪。"""
    st = ctx["ns"].get("students")
    if not isinstance(st, list) or len(st) != 6:
        return False
    return st[0].get("name") == "水城凛" and st[-1].get("name") == "夜刀神澪"


def rank_shown(ctx):
    import re
    return re.search(r"第\s*1\s*名[^\n]*水城凛|水城凛[^\n]*第\s*1\s*名", ctx["stdout"]) is not None


def grades_ok(ctx):
    """优秀 1、良好 3、及格 2、待努力 0。"""
    for k, v in ctx["ns"].items():
        if k.startswith("__") or not isinstance(v, dict):
            continue
        vals = {kk: vv for kk, vv in v.items() if isinstance(vv, int)}
        if len(vals) < 3:
            continue
        want = sorted([1, 3, 2, 0])
        if sorted(vals.values()) == want:
            return True
    return False


def grades_shown(ctx):
    out = ctx["stdout"]
    return "优秀" in out and "良好" in out and "及格" in out


def few_prints(ctx):
    import ast
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "print")
    return n <= 20


def uses_items_or_zip(ctx):
    import ast
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call):
            if getattr(n.func, "id", None) == "zip":
                return True
            if isinstance(n.func, ast.Attribute) and n.func.attr == "items":
                return True
    return False


CASES = [
    {
        "stdin": ["天野灯"],
        "checks": [
            {
                "id": "total",
                "desc": "给每个人加了 total 字段",
                "type": "custom", "fn": "totals_added",
                "fail": "遍历时写 `s[\"total\"] = s[\"chinese\"] + s[\"math\"] + s[\"english\"]`。"
                        "水城凛应该是 283，夜刀神澪 218",
            },
            {
                "id": "report",
                "desc": "成绩单每行信息齐全",
                "type": "custom", "fn": "report_rows",
                "fail": "一行里要有姓名、三科分数、总分",
            },
            {
                "id": "subject",
                "desc": "数学统计正确（99/71/85.5）",
                "type": "custom", "fn": "subject_stats",
                "fail": "数学最高 99、最低 71、平均 **85.5**，三个数要在同一行",
            },
            {
                "id": "all-subjects",
                "desc": "三科平均分都算了",
                "type": "custom", "fn": "all_subjects",
                "fail": "语文平均 82.3、数学 85.5、英语 83.5（都要 `round(..., 1)`）",
            },
            {
                "id": "sortkey",
                "desc": "用 key=lambda 排序",
                "type": "custom", "fn": "uses_sort_key",
                "fail": "`students.sort(key=lambda s: s[\"total\"], reverse=True)`",
            },
            {
                "id": "ranked",
                "desc": "排行榜顺序正确",
                "type": "custom", "fn": "ranked",
                "fail": "按总分从高到低：水城凛283 → 月见琉璃264 → 星野樱259 → "
                        "风见幽香259 → 天野灯225 → 夜刀神澪218",
            },
            {
                "id": "rank-shown",
                "desc": "排行榜带名次",
                "type": "custom", "fn": "rank_shown",
                "fail": "用 `enumerate` 生成名次，第 1 名应该是水城凛",
            },
            {
                "id": "grades",
                "desc": "等第统计正确",
                "type": "custom", "fn": "grades_ok",
                "fail": "优秀(≥270) **1** 人、良好(≥240) **3** 人、及格(≥210) **2** 人、待努力 **0** 人。"
                        "分档要用 `if / elif`，顺序从高到低",
            },
            {
                "id": "grades-shown",
                "desc": "等第分布显示出来了",
                "type": "custom", "fn": "grades_shown",
                "fail": "把四个等第和各自人数都打印出来",
            },
            {
                "id": "items-zip",
                "desc": "用到了 items() 或 zip()",
                "type": "custom", "fn": "uses_items_or_zip",
                "fail": "等第统计可以用 `for level, count in grades.items():` 来显示",
            },
            {
                "id": "few-prints",
                "desc": "全靠循环生成",
                "type": "custom", "fn": "few_prints",
                "fail": "print 不超过 20 个 —— 成绩单、排行榜、统计全要靠循环",
            },
            {
                "id": "query",
                "desc": "查到了天野灯的成绩和名次",
                "type": "stdout_contains", "value": ["天野灯", "225", "5"],
                "fail": "天野灯总分 225，排**第 5 名**，三科成绩也要显示",
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
                "fail": "班里没这个人时提示「查无此人」，不能崩",
            },
        ],
    },
]
