import re


def three_loops(ctx):
    import ast
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.For)) >= 3


def few_prints(ctx):
    """三个图案 20 多行输出，但 print 不该超过 8 个 —— 否则就是手写的。"""
    import ast
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "print")
    return n <= 8


def countdown(ctx):
    """倒计时：5 4 3 2 1 必须按这个顺序出现。"""
    nums = re.findall(r"\d+", ctx["stdout"])
    for k in range(len(nums) - 4):
        if nums[k:k + 5] == ["5", "4", "3", "2", "1"]:
            return True
    return False


def times_table(ctx):
    out = ctx["stdout"]
    return all(str(7 * i) in out for i in range(1, 10))


def pyramid(ctx):
    """找 5 行星星，个数依次是 1 3 5 7 9，而且要居中（前面有空格）。"""
    rows = []
    for line in ctx["stdout"].splitlines():
        stars = line.count("★") + line.count("*")
        if stars > 0:
            rows.append((stars, len(line) - len(line.lstrip())))
    for k in range(len(rows) - 4):
        window = rows[k:k + 5]
        if [w[0] for w in window] == [1, 3, 5, 7, 9]:
            # 居中的话，缩进要一行比一行少
            spaces = [w[1] for w in window]
            return spaces == sorted(spaces, reverse=True) and spaces[0] > spaces[-1]
    return False


def uses_range2(ctx):
    """至少用过一次两参数以上的 range。"""
    import ast
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "range":
            if len(n.args) >= 2:
                return True
    return False


CHECKS = [
    {
        "id": "loops",
        "desc": "三个图案都用了 for 循环",
        "type": "custom", "fn": "three_loops",
        "fail": "倒计时、乘法表、金字塔，各要一个 `for` 循环，一共三个",
    },
    {
        "id": "no-manual",
        "desc": "没有一行行手写 print",
        "type": "custom", "fn": "few_prints",
        "fail": "print 写太多了 😉 图案要靠循环生成，不是一行行敲出来的",
    },
    {
        "id": "range2",
        "desc": "用了带起点的 range",
        "type": "custom", "fn": "uses_range2",
        "fail": "至少用一次 `range(起点, 终点)` 的写法，比如 `range(1, 10)`",
    },
    {
        "id": "countdown",
        "desc": "倒计时 5 4 3 2 1",
        "type": "custom", "fn": "countdown",
        "fail": "倒着数要用 `range(5, 0, -1)` —— 第三个参数 -1 表示每次减 1",
    },
    {
        "id": "launch",
        "desc": "倒计时结束后发射",
        "type": "stdout_contains", "value": "发射",
        "fail": "「发射！」要写在循环**外面**（顶格），不然每数一个数就发射一次 😅",
    },
    {
        "id": "table",
        "desc": "七的乘法表 1~9 都对",
        "type": "custom", "fn": "times_table",
        "fail": "从 7 到 63 的九个结果都要出现。用 `range(1, 10)`（终点不含 10）",
    },
    {
        "id": "pyramid",
        "desc": "金字塔 5 层且居中",
        "type": "custom", "fn": "pyramid",
        "fail": "每层星星数应该是 1、3、5、7、9（也就是 `2 * i - 1`），"
                "前面再补 `(5 - i)` 个空格让它居中",
    },
]
