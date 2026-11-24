import ast

NEEDED = ["to_int", "to_float", "safe_divide", "safe_get", "safe_index", "register"]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def uses_try(ctx):
    """至少 5 处 try/except。"""
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.Try)) >= 5


def no_bare_except(ctx):
    """每个 except 都要写明类型 —— 光秃秃的 except: 会吞掉真 bug。"""
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ExceptHandler) and n.type is None:
            return False
    return True


def right_exception_types(ctx):
    """用对了具体的异常类型，而不是一律 Exception。"""
    names = set()
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ExceptHandler) and n.type is not None:
            if isinstance(n.type, ast.Name):
                names.add(n.type.id)
            elif isinstance(n.type, ast.Tuple):
                for e in n.type.elts:
                    if isinstance(e, ast.Name):
                        names.add(e.id)
    return {"ValueError", "ZeroDivisionError", "KeyError", "IndexError"} <= names


def to_int_ok(ctx):
    fn = ctx["ns"].get("to_int")
    if not callable(fn):
        return False
    return (fn("16") == 16 and fn("abc") == 0 and fn("") == 0
            and fn("abc", 99) == 99 and fn("-5") == -5)


def to_float_ok(ctx):
    fn = ctx["ns"].get("to_float")
    if not callable(fn):
        return False
    return (abs(fn("1.62") - 1.62) < 1e-9 and fn("abc") == 0.0
            and fn("abc", 1.7) == 1.7)


def divide_ok(ctx):
    fn = ctx["ns"].get("safe_divide")
    if not callable(fn):
        return False
    return fn(10, 2) == 5 and fn(10, 0) == 0


def safe_get_ok(ctx):
    fn = ctx["ns"].get("safe_get")
    if not callable(fn):
        return False
    d = {"hp": 340}
    return fn(d, "hp") == 340 and fn(d, "mp") == "未知" and fn(d, "mp", 0) == 0


def safe_index_ok(ctx):
    fn = ctx["ns"].get("safe_index")
    if not callable(fn):
        return False
    lst = ["a", "b"]
    return (fn(lst, 0) == "a" and fn(lst, 9) is None
            and fn(lst, 9, "没有") == "没有")


def register_returns_dict(ctx):
    """register 要返回字典 —— 直接看主流程跑出来的结果。"""
    for k, v in ctx["ns"].items():
        if k.startswith("__"):
            continue
        if isinstance(v, dict) and "name" in v and "age" in v:
            return True
    return False


def survived_bad_input(ctx):
    """喂了非法年龄和身高，程序仍要跑完。"""
    return ctx["error"] is None and "全程没有崩溃" in ctx["stdout"]


def default_used(ctx):
    """年龄输入 abc 时应该退回默认值 0，出生年份就是 2026。"""
    return "2026" in ctx["stdout"]


def divide_demo(ctx):
    return "10 / 0" in ctx["stdout"] or "除数" in ctx["stdout"]


def get_demo(ctx):
    return "未知" in ctx["stdout"]


CASES = [
    {
        "stdin": ["星野樱", "abc", "不是数字"],
        "checks": [
            {
                "id": "defined",
                "desc": "六个函数都定义了",
                "type": "custom", "fn": "all_defined",
                "fail": "to_int / to_float / safe_divide / safe_get / safe_index / register",
            },
            {
                "id": "try",
                "desc": "至少用了 5 处 try/except",
                "type": "custom", "fn": "uses_try",
                "fail": "五个 safe 函数每个都要用 `try` 包住可能出错的那一行",
            },
            {
                "id": "no-bare",
                "desc": "没有光秃秃的 except:",
                "type": "custom", "fn": "no_bare_except",
                "fail": "⚠️ `except:` 会把你自己的 bug 也一起吞掉。"
                        "一定要写明类型，比如 `except ValueError:`",
            },
            {
                "id": "types",
                "desc": "四种异常类型都用对了",
                "type": "custom", "fn": "right_exception_types",
                "fail": "转换用 `ValueError`、除法用 `ZeroDivisionError`、"
                        "字典用 `KeyError`、列表用 `IndexError`",
            },
            {
                "id": "to-int",
                "desc": "to_int 转换和兜底都对",
                "type": "custom", "fn": "to_int_ok",
                "fail": "`to_int(\"16\")` 是 16，`to_int(\"abc\")` 是 0，"
                        "`to_int(\"abc\", 99)` 是 99",
            },
            {
                "id": "to-float",
                "desc": "to_float 转换和兜底都对",
                "type": "custom", "fn": "to_float_ok",
                "fail": "`to_float(\"1.62\")` 是 1.62，转不了就返回 default",
            },
            {
                "id": "divide",
                "desc": "safe_divide 除零不崩",
                "type": "custom", "fn": "divide_ok",
                "fail": "`safe_divide(10, 0)` 要返回 0，不能抛异常",
            },
            {
                "id": "get",
                "desc": "safe_get 取不到返回默认值",
                "type": "custom", "fn": "safe_get_ok",
                "fail": "默认值参数写成 `default=\"未知\"`，取不到时返回它",
            },
            {
                "id": "index",
                "desc": "safe_index 越界返回默认值",
                "type": "custom", "fn": "safe_index_ok",
                "fail": "`safe_index([\"a\", \"b\"], 9)` 要返回 None，不能抛 IndexError",
            },
            {
                "id": "register",
                "desc": "register 返回信息字典",
                "type": "custom", "fn": "register_returns_dict",
                "fail": "返回一个至少含 name / age 的字典",
            },
            {
                "id": "survive",
                "desc": "乱输也跑完了全程",
                "type": "custom", "fn": "survived_bad_input",
                "fail": "年龄输入 `abc`、身高输入中文，程序都不该崩。"
                        "最后要打印一句「全程没有崩溃」",
            },
            {
                "id": "default",
                "desc": "非法年龄退回了默认值",
                "type": "custom", "fn": "default_used",
                "fail": "年龄转换失败按 0 算，出生年份就是 2026 - 0 = **2026**",
            },
            {
                "id": "divide-demo",
                "desc": "演示了除以 0",
                "type": "custom", "fn": "divide_demo",
                "fail": "主流程里调一次 `safe_divide(10, 0)` 看它稳稳返回",
            },
            {
                "id": "get-demo",
                "desc": "演示了取不存在的键",
                "type": "custom", "fn": "get_demo",
                "fail": "用 `safe_get` 取一个字典里没有的键，应该看到「未知」",
            },
        ],
    },
    {
        "stdin": ["月见琉璃", "16", "1.62"],
        "checks": [
            {
                "id": "normal",
                "desc": "正常输入也能正确处理",
                "type": "stdout_contains", "value": ["月见琉璃", "16", "2010"],
                "fail": "正常输入时要能正确转换：16 岁 → 出生年份 2010",
            },
        ],
    },
]
