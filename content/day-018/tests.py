import re


def _loops(ctx):
    import ast
    return [n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.For)]


def enough_loops(ctx):
    return len(_loops(ctx)) >= 4


def nested_count(ctx):
    """至少三处「循环里套循环」。"""
    import ast
    n = 0
    for outer in _loops(ctx):
        for child in ast.walk(outer):
            if isinstance(child, ast.For) and child is not outer:
                n += 1
                break
    return n >= 3


def uses_end(ctx):
    return 'end=""' in ctx["code"].replace(" ", "") or "end=''" in ctx["code"].replace(" ", "")


def few_prints(ctx):
    import ast
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "print")
    return n <= 15


def checkerboard(ctx):
    """找 8 行、每行 8 格、黑白交替的棋盘。"""
    rows = [l for l in ctx["stdout"].splitlines()
            if len(l) >= 8 and all(ch in "⬛⬜■□▪▫#. " for ch in l) and ("⬛" in l or "■" in l or "#" in l)]
    return len(rows) >= 8


def times_table(ctx):
    out = ctx["stdout"]
    return "9×9=81" in out.replace(" ", "") or "9*9=81" in out.replace(" ", "")


def diamond(ctx):
    """星星数依次 1 3 5 7 9 7 5 3 1，而且居中。"""
    seq = []
    for line in ctx["stdout"].splitlines():
        s = line.count("★") + line.count("*")
        if s:
            seq.append(s)
    want = [1, 3, 5, 7, 9, 7, 5, 3, 1]
    for k in range(len(seq) - 8):
        if seq[k:k + 9] == want:
            return True
    return False


def hollow_box(ctx):
    """找 5 行：首尾行是实心 5 颗，中间三行只有头尾两颗。"""
    rows = []
    for line in ctx["stdout"].splitlines():
        if line.count("★") + line.count("*") > 0:
            rows.append(line.rstrip())
    for k in range(len(rows) - 4):
        w = rows[k:k + 5]
        counts = [r.count("★") + r.count("*") for r in w]
        if counts == [5, 2, 2, 2, 5]:
            return True
    return False


CHECKS = [
    {
        "id": "loops",
        "desc": "四个图案都用了循环",
        "type": "custom", "fn": "enough_loops",
        "fail": "四个图案，至少要 4 个 `for` 循环",
    },
    {
        "id": "nested",
        "desc": "至少三处嵌套循环",
        "type": "custom", "fn": "nested_count",
        "fail": "棋盘、乘法表、方框都需要「循环里套循环」",
    },
    {
        "id": "end",
        "desc": "用 end=\"\" 让内层横着排",
        "type": "custom", "fn": "uses_end",
        "fail": "内层要写 `print(\"★\", end=\"\")`，外层再用一个空的 `print()` 换行",
    },
    {
        "id": "no-manual",
        "desc": "没有一行行手写",
        "type": "custom", "fn": "few_prints",
        "fail": "print 写太多了 😉 图案要靠嵌套循环生成",
    },
    {
        "id": "board",
        "desc": "棋盘 8×8 且黑白交替",
        "type": "custom", "fn": "checkerboard",
        "fail": "用 `(row + col) % 2 == 0` 判断这一格画黑还是画白",
    },
    {
        "id": "table",
        "desc": "九九乘法表算到 9×9=81",
        "type": "custom", "fn": "times_table",
        "fail": "内层写 `range(1, i + 1)`，让每行的列数跟着行号走",
    },
    {
        "id": "diamond",
        "desc": "菱形上下对称",
        "type": "custom", "fn": "diamond",
        "fail": "星星数要是 1 3 5 7 9 7 5 3 1。下半部分用 `range(4, 0, -1)` 倒着跑",
    },
    {
        "id": "box",
        "desc": "空心方框只有边框",
        "type": "custom", "fn": "hollow_box",
        "fail": "首尾两行 5 颗星，中间三行只有头尾各 1 颗。"
                "判断条件是 `row == 0 or row == 4 or col == 0 or col == 4`",
    },
]
