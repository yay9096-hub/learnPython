import ast

VALIDATORS = ["validate_name", "validate_age", "validate_element", "create_role"]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    need = VALIDATORS + ["try_register"]
    return all(f in _funcs(ctx) for f in need)


def uses_raise(ctx):
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.Raise)) >= 4


def validators_have_no_try(ctx):
    """里层只 raise 不 try —— 今天的核心分工。"""
    fns = _funcs(ctx)
    for name in VALIDATORS:
        fn = fns.get(name)
        if fn is None:
            return False
        if any(isinstance(n, ast.Try) for n in ast.walk(fn)):
            return False
    return True


def try_register_has_try(ctx):
    fn = _funcs(ctx).get("try_register")
    if fn is None:
        return False
    return any(isinstance(n, ast.Try) for n in ast.walk(fn))


def _raises(fn, exc, *args):
    try:
        fn(*args)
    except exc:
        return True
    except Exception:
        return False
    return False


def name_ok(ctx):
    fn = ctx["ns"].get("validate_name")
    if not callable(fn):
        return False
    if fn("  星野樱  ") != "星野樱":
        return False
    return (_raises(fn, ValueError, "樱")
            and _raises(fn, ValueError, "超级无敌宇宙第一魔法少女")
            and _raises(fn, TypeError, 123)
            and fn("小樱") == "小樱")


def age_ok(ctx):
    fn = ctx["ns"].get("validate_age")
    if not callable(fn):
        return False
    return (fn(16) == 16 and fn(0) == 0 and fn(120) == 120
            and _raises(fn, ValueError, -5)
            and _raises(fn, ValueError, 200)
            and _raises(fn, TypeError, "16"))


def element_ok(ctx):
    fn = ctx["ns"].get("validate_element")
    if not callable(fn):
        return False
    return (fn("火") == "火" and fn("雷") == "雷"
            and _raises(fn, ValueError, "土"))


def element_msg_lists_options(ctx):
    """错误信息里要告诉她有哪些选项。"""
    fn = ctx["ns"].get("validate_element")
    if not callable(fn):
        return False
    try:
        fn("土")
    except ValueError as e:
        msg = str(e)
        return "火" in msg and "水" in msg and "风" in msg
    except Exception:
        return False
    return False


def messages_are_useful(ctx):
    """错误信息里要带上实际收到的值。"""
    fn = ctx["ns"].get("validate_age")
    if not callable(fn):
        return False
    try:
        fn(-5)
    except ValueError as e:
        return "-5" in str(e)
    except Exception:
        return False
    return False


def create_role_ok(ctx):
    fn = ctx["ns"].get("create_role")
    if not callable(fn):
        return False
    r = fn("  星野樱  ", 16, "火")
    if not isinstance(r, dict) or r.get("name") != "星野樱":
        return False
    return _raises(fn, ValueError, "樱", 16, "火")


def try_register_ok(ctx):
    fn = ctx["ns"].get("try_register")
    if not callable(fn):
        return False
    ok, data = fn("星野樱", 16, "火")
    if ok is not True or not isinstance(data, dict):
        return False
    bad_ok, msg = fn("樱", 16, "火")
    return bad_ok is False and isinstance(msg, str) and len(msg) > 0


def shows_three_errors(ctx):
    """主流程打印了三条不同的错误信息。"""
    lines = [l for l in ctx["stdout"].splitlines() if "✗" in l or "失败" in l]
    return len({l.strip() for l in lines}) >= 3


def survived(ctx):
    return ctx["error"] is None and "全程没有崩溃" in ctx["stdout"]


CASES = [
    {
        "stdin": ["月见琉璃", "15", "水"],
        "checks": [
            {
                "id": "defined",
                "desc": "五个函数都定义了",
                "type": "custom", "fn": "all_defined",
                "fail": "validate_name / validate_age / validate_element / "
                        "create_role / try_register",
            },
            {
                "id": "raise",
                "desc": "至少用了 4 处 raise",
                "type": "custom", "fn": "uses_raise",
                "fail": "三个校验函数里，每种不合法情况都要 `raise` 一次",
            },
            {
                "id": "no-try-inside",
                "desc": "校验函数里没有 try",
                "type": "custom", "fn": "validators_have_no_try",
                "fail": "⚠️ 今天的核心分工：**里层只 raise，不 try**。"
                        "try 只出现在 `try_register` 和主流程里",
            },
            {
                "id": "has-try",
                "desc": "try_register 里有 try",
                "type": "custom", "fn": "try_register_has_try",
                "fail": "`try_register` 负责接住异常，转成 (False, 错误信息) 返回",
            },
            {
                "id": "name",
                "desc": "名字校验正确（含类型和边界）",
                "type": "custom", "fn": "name_ok",
                "fail": "太短/太长抛 `ValueError`，不是字符串抛 `TypeError`。"
                        "合法时返回 `.strip()` 之后的名字。2 个字和 8 个字都算合法",
            },
            {
                "id": "age",
                "desc": "年龄校验正确",
                "type": "custom", "fn": "age_ok",
                "fail": "0 和 120 都算合法；负数和超过 120 抛 `ValueError`；"
                        "传字符串抛 `TypeError`",
            },
            {
                "id": "element",
                "desc": "属性校验正确",
                "type": "custom", "fn": "element_ok",
                "fail": "只接受 火/水/风/雷，其它抛 `ValueError`",
            },
            {
                "id": "element-msg",
                "desc": "属性错误信息列出了可选值",
                "type": "custom", "fn": "element_msg_lists_options",
                "fail": "错误信息里要写清楚有哪些可选项，不然用户只能瞎猜",
            },
            {
                "id": "msg-value",
                "desc": "错误信息带上了实际收到的值",
                "type": "custom", "fn": "messages_are_useful",
                "fail": "好的错误信息要包含**实际收到了什么**，"
                        "比如「年龄不能是负数（收到的是 -5）」",
            },
            {
                "id": "create",
                "desc": "create_role 串起了三个校验",
                "type": "custom", "fn": "create_role_ok",
                "fail": "内部调用三个 validate 函数，任何一个不过就让异常自然往外传",
            },
            {
                "id": "try-register",
                "desc": "try_register 返回 (成功?, 结果)",
                "type": "custom", "fn": "try_register_ok",
                "fail": "成功返回 `(True, 角色字典)`，失败返回 `(False, 错误信息字符串)`",
            },
            {
                "id": "three-errors",
                "desc": "演示了三种不同的错误",
                "type": "custom", "fn": "shows_three_errors",
                "fail": "用名字太短、年龄负数、属性不认识三种数据各试一次，把错误信息都打出来",
            },
            {
                "id": "survive",
                "desc": "全程没有崩溃",
                "type": "custom", "fn": "survived",
                "fail": "最后要能打印「全程没有崩溃」—— 异常必须全被 try_register 接住",
            },
        ],
    },
    {
        "stdin": ["樱", "16", "火"],
        "checks": [
            {
                "id": "user-fail",
                "desc": "用户输入不合法时有提示",
                "type": "stdout_contains", "value": "太短",
                "fail": "玩家输入的名字只有 1 个字，要提示「名字太短」而不是崩掉",
            },
        ],
    },
]
