# 正确排序：998水城凛 / 995月见琉璃 / 905风见幽香 / 820星野樱 / 770夜刀神澪 / 640天野灯
ORDER = ["水城凛", "月见琉璃", "风见幽香", "星野樱", "夜刀神澪", "天野灯"]


def uses_sort(ctx):
    import ast
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Attribute) and f.attr == "sort":
                return True
            if isinstance(f, ast.Name) and f.id == "sorted":
                return True
    return False


def uses_reverse_flag(ctx):
    return "reverse=True" in ctx["code"].replace(" ", "")


def ranking_order(ctx):
    """榜单里六个名字出现的先后，必须是战力从高到低。"""
    out = ctx["stdout"]
    pos = []
    for n in ORDER:
        i = out.find(n)
        if i < 0:
            return False
        pos.append(i)
    return pos == sorted(pos)


def numbered(ctx):
    """有「第 N 名」这样的编号。"""
    import re
    return len(re.findall(r"第\s*\d+\s*名", ctx["stdout"])) >= 6


def uses_slice(ctx):
    import ast
    return any(isinstance(n, ast.Slice) for n in ast.walk(ctx["tree"]))


def uses_in_check(ctx):
    import ast
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Compare):
            for op in n.ops:
                if isinstance(op, (ast.In, ast.NotIn)):
                    return True
    return False


CASES = [
    {
        "stdin": ["月见琉璃"],
        "checks": [
            {
                "id": "sort",
                "desc": "用了排序",
                "type": "custom", "fn": "uses_sort",
                "fail": "用 `pairs.sort(...)` 或 `sorted(pairs, ...)` 排序，别自己手动排",
            },
            {
                "id": "desc",
                "desc": "排的是从高到低",
                "type": "custom", "fn": "uses_reverse_flag",
                "fail": "排行榜要从高到低，加上 `reverse=True`",
            },
            {
                "id": "order",
                "desc": "榜单顺序正确",
                "type": "custom", "fn": "ranking_order",
                "fail": "正确顺序是 水城凛(998) → 月见琉璃(995) → 风见幽香(905) → "
                        "星野樱(820) → 夜刀神澪(770) → 天野灯(640)。"
                        "名字和战力要**打包成一对**再排，否则名字不会跟着动",
            },
            {
                "id": "numbered",
                "desc": "榜单带名次编号",
                "type": "custom", "fn": "numbered",
                "fail": "每行要有「第 N 名」。用 `enumerate` 拿编号，记得 `i + 1`",
            },
            {
                "id": "slice",
                "desc": "用切片取了前三名",
                "type": "custom", "fn": "uses_slice",
                "fail": "前三名用 `pairs[:3]`（Day 26 学的切片）",
            },
            {
                "id": "top-bottom",
                "desc": "报出了榜首和榜尾",
                "type": "stdout_contains", "value": ["榜首", "榜尾"],
                "fail": "用 `pairs[0]` 和 `pairs[-1]` 取榜首榜尾各打印一次",
            },
            {
                "id": "in-check",
                "desc": "查名次前先用 in 检查",
                "type": "custom", "fn": "uses_in_check",
                "fail": "查一个不存在的名字，`.index()` 会直接报错。先用 `in` 确认",
            },
            {
                "id": "query",
                "desc": "查到了月见琉璃是第 2 名",
                "type": "stdout_regex", "pattern": "月见琉璃[^\n]*第\s*2\s*名|第\s*2\s*名[^\n]*月见琉璃",
                "fail": "月见琉璃战力 995，排**第 2 名**。`.index()` 返回的是编号，报名次要 +1",
            },
        ],
    },
    {
        "stdin": ["路人甲"],
        "checks": [
            {
                "id": "not-found",
                "desc": "查不到的人有提示",
                "type": "stdout_contains", "value": "榜上无名",
                "fail": "查不到时要走 `else` 提示「榜上无名」，而不是崩掉",
            },
        ],
    },
]
