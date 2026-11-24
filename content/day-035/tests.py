NEEDED = ["show_line", "show_title", "show_hero", "show_enemy", "show_victory"]


def _funcs(ctx):
    import ast
    return {n.name: n for n in ast.walk(ctx["tree"])
            if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def all_called(ctx):
    """五个函数都被真的调用过（不算函数内部的调用）。"""
    import ast
    called = set()
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            called.add(node.func.id)
    return all(f in called for f in NEEDED)


def title_uses_line(ctx):
    """show_title 内部要调用 show_line —— 小零件拼大零件。"""
    import ast
    fn = _funcs(ctx).get("show_title")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "show_line":
            return True
    return False


def line_called_enough(ctx):
    """分隔线至少出现 4 条 —— 体现一次定义多次调用。"""
    n = 0
    for line in ctx["stdout"].splitlines():
        s = line.strip()
        if len(s) >= 20 and len(set(s)) <= 2:
            n += 1
    return n >= 4


def has_docstrings(ctx):
    import ast
    fns = _funcs(ctx)
    if not fns:
        return False
    return sum(1 for f in fns.values() if ast.get_docstring(f)) >= 5


def defined_before_called(ctx):
    """所有 def 都在主流程调用之前 —— 好习惯。"""
    import ast
    last_def = -1
    first_top_call = 10 ** 9
    for node in ctx["tree"].body:
        if isinstance(node, ast.FunctionDef):
            last_def = max(last_def, node.lineno)
        elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            first_top_call = min(first_top_call, node.lineno)
    return first_top_call > last_def


def enough_output(ctx):
    return len([l for l in ctx["stdout"].splitlines() if l.strip()]) >= 10


CHECKS = [
    {
        "id": "defined",
        "desc": "五个函数都定义了",
        "type": "custom", "fn": "all_defined",
        "fail": "要有 show_line / show_title / show_hero / show_enemy / show_victory，"
                "函数名照抄",
    },
    {
        "id": "called",
        "desc": "五个函数都被调用了",
        "type": "custom", "fn": "all_called",
        "fail": "光 `def` 是不会执行的，最下面还要写 `show_title()` 这样调用一次。"
                "⚠️ 括号不能省",
    },
    {
        "id": "nested",
        "desc": "show_title 内部用了 show_line",
        "type": "custom", "fn": "title_uses_line",
        "fail": "在 `show_title` 里调用 `show_line()`，小零件拼成大零件",
    },
    {
        "id": "reuse",
        "desc": "分隔线至少出现 4 次",
        "type": "custom", "fn": "line_called_enough",
        "fail": "多调用几次 `show_line()` —— 这就是函数的价值：一次定义，到处使用",
    },
    {
        "id": "docstring",
        "desc": "每个函数都写了说明",
        "type": "custom", "fn": "has_docstrings",
        "fail": "函数第一行用三引号写一句说明，比如 `\"\"\"打印一条分隔线。\"\"\"`",
    },
    {
        "id": "order",
        "desc": "定义写在调用前面",
        "type": "custom", "fn": "defined_before_called",
        "fail": "所有 `def` 要写在主流程调用之前，否则 Python 还不认识它们",
    },
    {
        "id": "output",
        "desc": "播报内容够丰富（至少 10 行）",
        "type": "custom", "fn": "enough_output",
        "fail": "标题 + 我方 + 敌方 + 胜利画面，加起来应该不止这几行",
    },
]
