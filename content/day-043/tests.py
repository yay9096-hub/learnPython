import ast


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def _is_recursive(ctx, name):
    fn = _funcs(ctx).get(name)
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == name:
            return True
    return False


def _has_guard(ctx, name):
    """函数体里要有 if + return（出口条件）。"""
    fn = _funcs(ctx).get(name)
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.If):
            for sub in ast.walk(n):
                if isinstance(sub, ast.Return):
                    return True
    return False


def countdown_recursive(ctx):
    return _is_recursive(ctx, "countdown")


def countdown_works(ctx):
    out = ctx["stdout"]
    return "发射" in out and "5" in out and "1" in out


def factorial_recursive(ctx):
    return _is_recursive(ctx, "factorial")


def factorial_correct(ctx):
    fn = ctx["ns"].get("factorial")
    if not callable(fn):
        return False
    return fn(1) == 1 and fn(5) == 120 and fn(0) == 1 and fn(6) == 720


def factorial_printed(ctx):
    return "120" in ctx["stdout"]


def tree_recursive(ctx):
    return _is_recursive(ctx, "tree")


def tree_has_exit(ctx):
    return _has_guard(ctx, "tree")


def tree_shrinks(ctx):
    """递归调用时长度要变小 —— 代码里得有乘法。"""
    fn = _funcs(ctx).get("tree")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "tree":
            for a in n.args:
                if isinstance(a, ast.BinOp) and isinstance(a.op, ast.Mult):
                    return True
    return False


def tree_backtracks(ctx):
    """画完要退回起点。"""
    fn = _funcs(ctx).get("tree")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr in ("backward", "back", "bk"):
                return True
    return False


def enough_branches(ctx):
    """6 层树至少 60 根树枝（2^6 - 2 = 62）。"""
    return sum(1 for c in ctx["turtle"]["cmds"] if c["op"] == "line") >= 60


def varied_widths(ctx):
    """粗细跟层数挂钩 —— 至少 4 种不同线宽。"""
    widths = {round(float(c.get("w", 0)), 2)
              for c in ctx["turtle"]["cmds"] if c["op"] == "line"}
    return len(widths) >= 4


def two_colors(ctx):
    colors = {c.get("color") for c in ctx["turtle"]["cmds"]
              if c["op"] == "line" and c.get("color")}
    return len(colors) >= 2


def deep_enough(ctx):
    """主流程里 tree 的第二个参数至少 6。"""
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "tree":
            if len(n.args) >= 2 and isinstance(n.args[1], ast.Constant):
                if isinstance(n.args[1].value, int) and n.args[1].value >= 6:
                    return True
    return False


CHECKS = [
    {
        "id": "countdown-rec",
        "desc": "countdown 是递归的",
        "type": "custom", "fn": "countdown_recursive",
        "fail": "函数体里要调用它自己：`countdown(n - 1)`",
    },
    {
        "id": "countdown-out",
        "desc": "倒数跑通了",
        "type": "custom", "fn": "countdown_works",
        "fail": "从 5 数到 1，然后打印「发射！」。出口是 `if n <= 0: return`",
    },
    {
        "id": "fact-rec",
        "desc": "factorial 是递归的",
        "type": "custom", "fn": "factorial_recursive",
        "fail": "`return n * factorial(n - 1)` —— 用自己算自己",
    },
    {
        "id": "fact-ok",
        "desc": "阶乘算得对（含边界）",
        "type": "custom", "fn": "factorial_correct",
        "fail": "5! = 120，6! = 720。⚠️ `factorial(0)` 和 `factorial(1)` 都该返回 1 —— "
                "出口写 `if n <= 1: return 1`",
    },
    {
        "id": "fact-print",
        "desc": "打印了 factorial(5)",
        "type": "custom", "fn": "factorial_printed",
        "fail": "主流程里打印一下 `factorial(5)`，应该看到 120",
    },
    {
        "id": "tree-rec",
        "desc": "tree 是递归的",
        "type": "custom", "fn": "tree_recursive",
        "fail": "`tree` 里要调用两次它自己 —— 左边一棵、右边一棵",
    },
    {
        "id": "tree-exit",
        "desc": "tree 有出口条件",
        "type": "custom", "fn": "tree_has_exit",
        "fail": "函数第一句写 `if depth == 0: return`，"
                "没有出口会一直递归到 RecursionError",
    },
    {
        "id": "tree-shrink",
        "desc": "每层树枝变短",
        "type": "custom", "fn": "tree_shrinks",
        "fail": "递归时传 `length * 0.72` 这样的缩短系数，树才有层次",
    },
    {
        "id": "tree-back",
        "desc": "画完退回了起点",
        "type": "custom", "fn": "tree_backtracks",
        "fail": "⚠️ 函数最后要 `turtle.backward(length)` 退回起点，"
                "否则下一根树枝会从错误的位置长出来",
    },
    {
        "id": "depth",
        "desc": "树至少 6 层",
        "type": "custom", "fn": "deep_enough",
        "fail": "调用时 depth 至少给 6，比如 `tree(100, 7)`",
    },
    {
        "id": "branches",
        "desc": "树枝够多（至少 60 根）",
        "type": "custom", "fn": "enough_branches",
        "fail": "6 层树应该有 60 根以上的树枝。少了说明递归没展开，检查出口和两次调用",
    },
    {
        "id": "widths",
        "desc": "粗细随层数变化",
        "type": "custom", "fn": "varied_widths",
        "fail": "用 `turtle.pensize(depth)`，越往末梢越细",
    },
    {
        "id": "colors",
        "desc": "末梢和主干颜色不同",
        "type": "custom", "fn": "two_colors",
        "fail": "用 `if depth <= 2:` 把末梢画成绿色、主干画成木色",
    },
]
