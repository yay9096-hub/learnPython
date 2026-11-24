WORDS = "牛啊 前排 牛啊 打卡 awsl 牛啊 前排 泪目 awsl 前排 牛啊 打卡".split()
UNIQUE = ["牛啊", "前排", "打卡", "awsl", "泪目"]


def uses_split(ctx):
    import ast
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "split" for n in ast.walk(ctx["tree"]))


def uses_join(ctx):
    import ast
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "join" for n in ast.walk(ctx["tree"]))


def uses_count(ctx):
    import ast
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "count" for n in ast.walk(ctx["tree"]))


def words_ok(ctx):
    for k, v in ctx["ns"].items():
        if k.startswith("__"):
            continue
        if isinstance(v, list) and v == WORDS:
            return True
    return False


def unique_ok(ctx):
    for k, v in ctx["ns"].items():
        if k.startswith("__"):
            continue
        if isinstance(v, list) and sorted(map(str, v)) == sorted(UNIQUE):
            return True
    return False


def counts_printed(ctx):
    """五个词各自的次数都出现在输出里（同一行内有词也有数）。"""
    import re
    want = {"牛啊": 4, "前排": 3, "打卡": 2, "awsl": 2, "泪目": 1}
    for line in ctx["stdout"].splitlines():
        for w, n in list(want.items()):
            if w in line and re.search(r"\b%d\b" % n, line):
                want.pop(w)
    return not want


def no_hardcode(ctx):
    """不许把去重结果直接抄成字面量。原始弹幕那一行是字符串，不算。"""
    import ast
    lists = [n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.List) and n.elts]
    return len(lists) == 0


CHECKS = [
    {
        "id": "split",
        "desc": "用 split() 把弹幕拆成列表",
        "type": "custom", "fn": "uses_split",
        "fail": "`words = danmaku.split()` —— 不加参数就是按空格拆",
    },
    {
        "id": "words",
        "desc": "拆出来是 12 条",
        "type": "custom", "fn": "words_ok",
        "fail": "拆完应该是 12 个词的列表。`print(words)` 看一眼对不对",
    },
    {
        "id": "total",
        "desc": "报出了总条数",
        "type": "stdout_contains", "value": "12",
        "fail": "用 `len(words)` 报出总条数",
    },
    {
        "id": "no-hardcode",
        "desc": "去重是算出来的，不是手抄的",
        "type": "custom", "fn": "no_hardcode",
        "fail": "代码里不该出现手写的方括号列表 —— 去重要用循环 + `not in` 算出来 😉",
    },
    {
        "id": "unique",
        "desc": "去重结果正确（5 种）",
        "type": "custom", "fn": "unique_ok",
        "fail": "不重复的词是 牛啊 / 前排 / 打卡 / awsl / 泪目，一共 **5 种**。"
                "套路：`if w not in unique: unique.append(w)`",
    },
    {
        "id": "count",
        "desc": "用 count() 统计次数",
        "type": "custom", "fn": "uses_count",
        "fail": "每个词出现几次用 `words.count(w)` 数",
    },
    {
        "id": "counts",
        "desc": "每个词的次数都对",
        "type": "custom", "fn": "counts_printed",
        "fail": "正确答案：牛啊 4 次、前排 3 次、打卡 2 次、awsl 2 次、泪目 1 次。"
                "每一行里词和次数都要有",
    },
    {
        "id": "best",
        "desc": "找出了刷得最多的词",
        "type": "stdout_regex", "pattern": "牛啊[^\n]*4|4[^\n]*牛啊",
        "fail": "刷得最多的是「牛啊」，**4 次**。用 Day 20 的找最值套路",
    },
    {
        "id": "join",
        "desc": "用 join() 拼成一行",
        "type": "custom", "fn": "uses_join",
        "fail": "用 `\" / \".join(unique)` 把不重复的词拼成一行",
    },
    {
        "id": "joined",
        "desc": "拼出来的那行显示了",
        "type": "stdout_contains", "value": "/",
        "fail": "把 join 的结果打印出来",
    },
]
