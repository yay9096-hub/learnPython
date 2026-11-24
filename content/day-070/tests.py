"""毕业作品的判题。

跟前面 69 天不同：这里**不检查具体做了什么**，只检查
「有没有把这 70 天学的东西用起来」—— 题目是她自己定的，
判题只能验能力，不能验内容。
"""
import ast

BAD_NAMES = {"f", "g", "h", "k", "p", "q", "a", "b", "c", "d", "e",
             "x1", "x2", "func1", "func2", "aaa", "test1"}

SETUP = '''
import os
for _n in ["我的番剧.json", "评分分布.png"]:
    if os.path.exists(_n):
        os.remove(_n)
'''


def _funcs(ctx):
    """模块级函数（不含类里的方法）。"""
    return [n for n in ctx["tree"].body if isinstance(n, ast.FunctionDef)]


def _classes(ctx):
    return [n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.ClassDef)]


def has_module_doc(ctx):
    doc = ast.get_docstring(ctx["tree"])
    return doc is not None and len(doc.strip()) >= 10


def has_constants(ctx):
    n = 0
    for node in ctx["tree"].body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.isupper() and len(t.id) > 2:
                    n += 1
    return n >= 3


def six_functions(ctx):
    return len(_funcs(ctx)) >= 6


def all_have_docstrings(ctx):
    fns = _funcs(ctx)
    if len(fns) < 6:
        return False
    return all(ast.get_docstring(f) for f in fns)


def has_class(ctx):
    return len(_classes(ctx)) >= 1


def class_has_init_and_methods(ctx):
    for cls in _classes(ctx):
        methods = [f.name for f in cls.body if isinstance(f, ast.FunctionDef)]
        normal = [m for m in methods if not m.startswith("__")]
        if "__init__" in methods and len(normal) >= 2:
            return True
    return False


def class_has_dunder(ctx):
    """除了 __init__ 之外还要有别的特殊方法。"""
    for cls in _classes(ctx):
        for f in cls.body:
            if isinstance(f, ast.FunctionDef):
                if f.name.startswith("__") and f.name != "__init__":
                    return True
    return False


def uses_list_and_dict(ctx):
    has_list = any(isinstance(n, (ast.List, ast.ListComp))
                   for n in ast.walk(ctx["tree"]))
    has_dict = any(isinstance(n, (ast.Dict, ast.DictComp))
                   for n in ast.walk(ctx["tree"]))
    return has_list and has_dict


def uses_try(ctx):
    return any(isinstance(n, ast.Try) for n in ast.walk(ctx["tree"]))


def no_bare_except(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ExceptHandler) and n.type is None:
            return False
    return True


def uses_file(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "open":
            return True
    return False


def uses_loop_and_if(ctx):
    has_loop = any(isinstance(n, (ast.For, ast.While)) for n in ast.walk(ctx["tree"]))
    has_if = any(isinstance(n, ast.If) for n in ast.walk(ctx["tree"]))
    return has_loop and has_if


def makes_something_visual(ctx):
    """turtle 画了东西，或者 matplotlib 画了图。"""
    drew_turtle = len(ctx["turtle"].get("cmds", [])) >= 5
    drew_plot = ctx["plot"].get("axes", 0) >= 1
    return drew_turtle or drew_plot


def good_names(ctx):
    """函数名和参数名都要有意义。"""
    for fn in _funcs(ctx):
        if fn.name in BAD_NAMES or len(fn.name) < 3:
            return False
        for arg in fn.args.args:
            if arg.arg in BAD_NAMES and arg.arg not in {"a", "b"}:
                return False
    for cls in _classes(ctx):
        for f in cls.body:
            if isinstance(f, ast.FunctionDef):
                if f.name in BAD_NAMES:
                    return False
    return True


def enough_output(ctx):
    return len([l for l in ctx["stdout"].splitlines() if l.strip()]) >= 12


def instantiates_class(ctx):
    """类要真的被用起来，不能只定义不用。"""
    names = {c.name for c in _classes(ctx)}
    if not names:
        return False
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) in names:
            return True
    return False


def survived(ctx):
    return ctx["error"] is None


def long_enough(ctx):
    """毕业作品总得有点体量 —— 至少 60 行有效代码。"""
    lines = [l for l in ctx["code"].splitlines()
             if l.strip() and not l.strip().startswith("#")]
    return len(lines) >= 60


CASES = [
    {
        "setup": SETUP,
        "checks": [
            {"id": "module-doc", "desc": "文件开头有作品说明",
             "type": "custom", "fn": "has_module_doc",
             "fail": "第一行用三引号写清楚：作品叫什么、做什么用（D42）"},
            {"id": "constants", "desc": "至少 3 个全大写常量",
             "type": "custom", "fn": "has_constants",
             "fail": "把文件名、上限值这些提成常量放在文件上部（D42）"},
            {"id": "functions", "desc": "至少 6 个函数",
             "type": "custom", "fn": "six_functions",
             "fail": "把功能拆成 6 个以上的函数，一个函数只做一件事（D41）"},
            {"id": "docstrings", "desc": "每个函数都有 docstring",
             "type": "custom", "fn": "all_have_docstrings",
             "fail": "每个函数第一行写一句三引号说明（D42）"},
            {"id": "class", "desc": "定义了至少 1 个类",
             "type": "custom", "fn": "has_class",
             "fail": "用 `class` 设计一个属于你这个作品的类型（D55）"},
            {"id": "class-shape", "desc": "类有 __init__ 和 2 个以上方法",
             "type": "custom", "fn": "class_has_init_and_methods",
             "fail": "类里要有 `__init__` 和至少两个普通方法（D56–57）"},
            {"id": "dunder", "desc": "类有特殊方法",
             "type": "custom", "fn": "class_has_dunder",
             "fail": "加一个 `__str__`，让 `print(对象)` 好看（D61）"},
            {"id": "used", "desc": "类真的被用起来了",
             "type": "custom", "fn": "instantiates_class",
             "fail": "主流程里要真的造出这个类的对象来用"},
            {"id": "data", "desc": "用到了列表和字典",
             "type": "custom", "fn": "uses_list_and_dict",
             "fail": "第三章的两种数据结构都要用上（D23–31）"},
            {"id": "try", "desc": "至少一处 try / except",
             "type": "custom", "fn": "uses_try",
             "fail": "读文件、转数字这些地方要接住异常（D45）"},
            {"id": "no-bare", "desc": "except 都写明了类型",
             "type": "custom", "fn": "no_bare_except",
             "fail": "别写光秃秃的 `except:`，会把真 bug 也吞掉（D45）"},
            {"id": "file", "desc": "读或写了文件",
             "type": "custom", "fn": "uses_file",
             "fail": "让作品能存住东西 —— 用 `open(...)` 存个档（D47–50）"},
            {"id": "flow", "desc": "用了循环和条件判断",
             "type": "custom", "fn": "uses_loop_and_if",
             "fail": "第二章的基本功（D11–20）"},
            {"id": "visual", "desc": "产出了看得见的东西",
             "type": "custom", "fn": "makes_something_visual",
             "fail": "用 turtle 画个图，或者用 matplotlib 出一张图表（D8 / D64）"},
            {"id": "names", "desc": "命名都有意义",
             "type": "custom", "fn": "good_names",
             "fail": "别用 `f` `g` `x1` 这种名字 —— 写给一个月后的自己看（D42）"},
            {"id": "size", "desc": "有毕业作品该有的体量",
             "type": "custom", "fn": "long_enough",
             "fail": "至少 60 行有效代码。慢慢加功能，一次加一个"},
            {"id": "output", "desc": "跑起来有丰富的输出",
             "type": "custom", "fn": "enough_output",
             "fail": "至少 12 行输出 —— 让别人一跑就看得懂它在干嘛"},
            {"id": "survive", "desc": "完整跑完不崩溃",
             "type": "custom", "fn": "survived",
             "fail": "从头跑到尾不能报错。**这是毕业的底线** —— "
                     "每加一个功能就跑一次，别攒到最后"},
        ],
    }
]
