def uses_items(ctx):
    import ast
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "items" for n in ast.walk(ctx["tree"]))


def uses_values(ctx):
    import ast
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "values" for n in ast.walk(ctx["tree"]))


def all_listed(ctx):
    out = ctx["stdout"]
    return all(n in out for n in ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"])


def paired(ctx):
    """名字和战力在同一行。"""
    import re
    return re.search(r"星野樱[^\n]*820", ctx["stdout"]) is not None


def added(ctx):
    b = ctx["ns"].get("book")
    return isinstance(b, dict) and len(b) == 6


def few_prints(ctx):
    import ast
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "print")
    return n <= 14


CASES = [
    {
        "stdin": ["月见琉璃"],
        "checks": [
            {
                "id": "items",
                "desc": "用 .items() 遍历图鉴",
                "type": "custom", "fn": "uses_items",
                "fail": "遍历字典用 `for name, power in book.items():` —— 一次拿到键和值",
            },
            {
                "id": "listed",
                "desc": "五个角色都显示了",
                "type": "custom", "fn": "all_listed",
                "fail": "图鉴里五个人都要逐行显示出来",
            },
            {
                "id": "paired",
                "desc": "名字和战力在同一行",
                "type": "custom", "fn": "paired",
                "fail": "格式像 `星野樱 —— 战力 820`，名字和数值放一行",
            },
            {
                "id": "few-prints",
                "desc": "没有一行行手写",
                "type": "custom", "fn": "few_prints",
                "fail": "图鉴内容要靠 `.items()` 循环生成，不是一行行 print",
            },
            {
                "id": "values",
                "desc": "用 .values() 做统计",
                "type": "custom", "fn": "uses_values",
                "fail": "`sum(book.values())` —— 只要值的时候用 `.values()`",
            },
            {
                "id": "total",
                "desc": "总战力算对了（4223）",
                "type": "value_present", "value": 4223,
                "fail": "820+995+640+998+770 = **4223**",
            },
            {
                "id": "avg",
                "desc": "平均战力算对了（844.6）",
                "type": "value_present", "value": 844.6, "tol": 0.05,
                "fail": "4223 ÷ 5 = 844.6（记得 `round(..., 1)`）",
            },
            {
                "id": "best",
                "desc": "找对了最强的角色",
                "type": "stdout_regex", "pattern": "水城凛[^\n]*998|998[^\n]*水城凛",
                "fail": "最强是**水城凛（998）**，名字和数值要在同一行",
            },
            {
                "id": "strong",
                "desc": "800 以上的人数对（3 人）",
                "type": "value_present", "value": 3,
                "fail": "820、995、998 三个达到 800，答案是 **3 人**",
            },
            {
                "id": "added",
                "desc": "收录了新角色（变成 6 人）",
                "type": "custom", "fn": "added",
                "fail": "`book[\"风见幽香\"] = 905` 收录一个新人，收录后 `len(book)` 应该是 6",
            },
            {
                "id": "query",
                "desc": "查到了月见琉璃",
                "type": "stdout_contains", "value": "995",
                "fail": "查「月见琉璃」应该报出战力 995",
            },
        ],
    },
    {
        "stdin": ["路人甲"],
        "checks": [
            {
                "id": "not-found",
                "desc": "查不到的人有提示",
                "type": "stdout_contains", "value": "暂无此人",
                "fail": "查不到时提示「图鉴中暂无此人」，别用 `book[who]` 直接查（会 KeyError）",
            },
        ],
    },
]
