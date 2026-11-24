RECORDS = ["R", "SR", "R", "SSR", "R", "R", "SR", "SSR", "R", "SR", "SSR", "R"]


def uses_slices(ctx):
    """真的用了切片语法，不是手写列表。"""
    import ast
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.Slice)) >= 5


def no_hardcode(ctx):
    """不许把答案直接抄成字面量列表。原始数据那一行除外。"""
    import ast
    lists = [n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.List)]
    return len(lists) <= 1


CHECKS = [
    {
        "id": "slices",
        "desc": "用了切片语法（至少 5 处）",
        "type": "custom", "fn": "uses_slices",
        "fail": "五项分析都要用 `[a:b]` 这类切片写出来，不是手敲结果",
    },
    {
        "id": "no-hardcode",
        "desc": "没有把答案手抄成列表",
        "type": "custom", "fn": "no_hardcode",
        "fail": "代码里除了原始的 `records`，不该再出现别的方括号列表字面量 😉",
    },
    {
        "id": "recent",
        "desc": "最近 5 次切对了",
        "type": "list_equals", "value": ["SSR", "R", "SR", "SSR", "R"],
        "fail": "最近 5 次用 `records[-5:]`。注意是 5 个，不是 4 个",
    },
    {
        "id": "earliest",
        "desc": "最早 3 次切对了",
        "type": "list_equals", "value": ["R", "SR", "R"],
        "fail": "最早 3 次用 `records[:3]`",
    },
    {
        "id": "reversed",
        "desc": "倒序切对了",
        "type": "list_equals", "value": RECORDS[::-1],
        "fail": "整个倒过来用 `records[::-1]`",
    },
    {
        "id": "every-other",
        "desc": "每隔一个切对了",
        "type": "list_equals", "value": ["R", "R", "R", "SR", "R", "SSR"],
        "fail": "每隔一个用 `records[::2]` —— 第三个数是步长",
    },
    {
        "id": "middle",
        "desc": "中间 4 次切对了",
        "type": "list_equals", "value": ["R", "R", "SR", "SSR"],
        "fail": "编号 4 到 7 用 `records[4:8]` —— **结束位置不包含**，所以写 8",
    },
    {
        "id": "ssr",
        "desc": "数对了最近 5 次里的 SSR",
        "type": "value_present", "value": 2,
        "fail": "最近 5 次是 SSR、R、SR、SSR、R —— 有 **2** 个 SSR。"
                "用 `recent.count(\"SSR\")` 数",
    },
    {
        "id": "printed",
        "desc": "结果都打印出来了",
        "type": "stdout_contains", "value": ["最近", "最早", "倒序"],
        "fail": "把每一项分析都打印出来，带上说明文字",
    },
]
