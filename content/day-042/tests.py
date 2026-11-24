import ast

BAD_NAMES = {"f", "g", "h", "k", "p", "b", "a", "c", "d", "x", "y", "n", "l", "o"}
MAGIC = {999, 1.5, 400, 150, 3}


def _funcs(ctx):
    return [n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)]


def has_module_docstring(ctx):
    return ast.get_docstring(ctx["tree"]) is not None


def enough_constants(ctx):
    """至少 4 个全大写的模块级常量。"""
    n = 0
    for node in ctx["tree"].body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.isupper() and len(t.id) > 2:
                    n += 1
    return n >= 4


def good_function_names(ctx):
    for fn in _funcs(ctx):
        if fn.name in BAD_NAMES or len(fn.name) < 3:
            return False
    return True


def good_param_names(ctx):
    for fn in _funcs(ctx):
        for arg in fn.args.args:
            if arg.arg in BAD_NAMES or len(arg.arg) < 2:
                return False
    return True


def good_local_names(ctx):
    """函数体里赋值的变量名也要有意义（循环变量 i / m 之类放过）。"""
    allow = {"i", "m", "n"}
    for fn in _funcs(ctx):
        for node in ast.walk(fn):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        if t.id in BAD_NAMES and t.id not in allow:
                            return False
    return True


def all_docstrings(ctx):
    fns = _funcs(ctx)
    return len(fns) >= 6 and all(ast.get_docstring(f) for f in fns)


def has_is_prefix(ctx):
    """返回真假的那个函数要用 is_ 开头。"""
    for fn in _funcs(ctx):
        if fn.name.startswith(("is_", "has_", "can_")):
            return True
    return False


def no_magic_numbers(ctx):
    """函数体里不该再出现 999 / 1.5 / 400 / 150 / 3 这些裸数字。"""
    for fn in _funcs(ctx):
        for node in ast.walk(fn):
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                if node.value in MAGIC and not isinstance(node.value, bool):
                    return False
    return True


def damage_still_correct(ctx):
    """逻辑不能改：找出那个算伤害的函数，验证它还对。"""
    ns = ctx["ns"]
    for name, fn in ns.items():
        if name.startswith("__") or not callable(fn):
            continue
        try:
            if fn(88, 25) == 63 and fn(10, 99) == 1 and fn(9999, 0) == 999:
                return True
        except Exception:
            continue
    return False


def crit_still_correct(ctx):
    ns = ctx["ns"]
    for name, fn in ns.items():
        if name.startswith("__") or not callable(fn):
            continue
        try:
            if abs(fn(88, 25) - 94.5) < 0.01:
                return True
        except Exception:
            continue
    return False


def output_unchanged(ctx):
    """输出要和原版一致：三个回合，敌人从 500 掉到 311。"""
    out = ctx["stdout"]
    return ("63" in out and "94.5" in out and "437" in out
            and "374" in out and "311" in out)


def status_correct(ctx):
    """311 血应该是「受伤」。"""
    return "受伤" in ctx["stdout"]


CHECKS = [
    {
        "id": "module-doc",
        "desc": "文件开头有三引号说明",
        "type": "custom", "fn": "has_module_docstring",
        "fail": "文件最上面写一段三引号，说明这个文件是干什么的",
    },
    {
        "id": "constants",
        "desc": "提取了至少 4 个常量",
        "type": "custom", "fn": "enough_constants",
        "fail": "把 999 / 1.5 / 400 / 150 / 3 这些数字提成全大写常量，放在文件上部",
    },
    {
        "id": "fn-names",
        "desc": "函数名都有意义",
        "type": "custom", "fn": "good_function_names",
        "fail": "`f` `g` `h` `k` `p` `b` 全要改成动词开头的名字，"
                "比如 `deal_damage`、`show_round`",
    },
    {
        "id": "param-names",
        "desc": "参数名都有意义",
        "type": "custom", "fn": "good_param_names",
        "fail": "`a` `b` `x` `y` 要改成 `atk`、`defense`、`hp` 这种看得懂的名字",
    },
    {
        "id": "local-names",
        "desc": "函数里的变量名也有意义",
        "type": "custom", "fn": "good_local_names",
        "fail": "函数体里的 `c` `d` 也要改掉（循环变量 `i` 可以留）",
    },
    {
        "id": "docstrings",
        "desc": "每个函数都有 docstring",
        "type": "custom", "fn": "all_docstrings",
        "fail": "六个函数每个都要有三引号说明，写「解决什么问题」而不是翻译代码",
    },
    {
        "id": "is-prefix",
        "desc": "判断真假的函数用 is_ 开头",
        "type": "custom", "fn": "has_is_prefix",
        "fail": "原来那个 `h(x)` 返回的是 True/False，应该叫 `is_alive`",
    },
    {
        "id": "no-magic",
        "desc": "函数里没有魔法数字了",
        "type": "custom", "fn": "no_magic_numbers",
        "fail": "函数体里不该再出现 999 / 1.5 / 400 / 150 / 3，全部换成常量名",
    },
    {
        "id": "damage-ok",
        "desc": "伤害逻辑没被改坏",
        "type": "custom", "fn": "damage_still_correct",
        "fail": "重构不能改功能：88 打 25 还是 63，10 打 99 还是 1，上限还是 999",
    },
    {
        "id": "crit-ok",
        "desc": "暴击逻辑没被改坏",
        "type": "custom", "fn": "crit_still_correct",
        "fail": "88 打 25 的暴击还应该是 94.5",
    },
    {
        "id": "output",
        "desc": "输出和原版完全一致",
        "type": "custom", "fn": "output_unchanged",
        "fail": "三个回合敌人应该从 500 → 437 → 374 → 311。整理代码不能改结果",
    },
    {
        "id": "status",
        "desc": "状态判断还是对的",
        "type": "custom", "fn": "status_correct",
        "fail": "剩 311 血在 150~400 之间，状态应该是「受伤」",
    },
]
