NEEDED = {
    "show_line": ["char", "width"],
    "show_role": ["name", "hp", "atk"],
    "deal_damage": ["attacker", "atk", "defense"],
    "show_team": ["team"],
}


def _funcs(ctx):
    import ast
    return {n.name: n for n in ast.walk(ctx["tree"])
            if isinstance(n, ast.FunctionDef)}


def signatures_ok(ctx):
    """函数名和参数个数都要对上（参数名建议照抄，个数必须对）。"""
    fns = _funcs(ctx)
    for name, params in NEEDED.items():
        fn = fns.get(name)
        if fn is None or len(fn.args.args) != len(params):
            return False
    return True


def line_varied(ctx):
    """show_line 用不同符号和宽度调过至少 3 次。"""
    import ast
    seen = set()
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "show_line":
            key = tuple(
                getattr(a, "value", None) for a in n.args
            )
            seen.add(key)
    return len(seen) >= 3


def _count_calls(ctx, name):
    import ast
    return sum(1 for n in ast.walk(ctx["tree"])
               if isinstance(n, ast.Call) and getattr(n.func, "id", None) == name)


def role_twice(ctx):
    return _count_calls(ctx, "show_role") >= 2


def damage_thrice(ctx):
    return _count_calls(ctx, "deal_damage") >= 3


def team_called(ctx):
    return _count_calls(ctx, "show_team") >= 1


def damage_min_guard(ctx):
    """攻击力低于防御力时，伤害要保底为 1。直接调她的函数验。"""
    fn = ctx["ns"].get("deal_damage")
    if not callable(fn):
        return False
    import io, sys
    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        fn("测试者", 10, 99)
    except Exception:
        return False
    finally:
        sys.stdout = real
    out = buf.getvalue()
    return "1" in out and "-" not in out


def damage_math(ctx):
    """普通情况算得对不对。"""
    fn = ctx["ns"].get("deal_damage")
    if not callable(fn):
        return False
    import io, sys
    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        fn("测试者", 88, 25)
    except Exception:
        return False
    finally:
        sys.stdout = real
    return "63" in buf.getvalue()


def line_flexible(ctx):
    """直接调她的 show_line，验证真的按参数走。"""
    fn = ctx["ns"].get("show_line")
    if not callable(fn):
        return False
    import io, sys
    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        fn("@", 7)
    except Exception:
        return False
    finally:
        sys.stdout = real
    return "@@@@@@@" in buf.getvalue()


def team_flexible(ctx):
    fn = ctx["ns"].get("show_team")
    if not callable(fn):
        return False
    import io, sys
    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        fn(["甲", "乙"])
    except Exception:
        return False
    finally:
        sys.stdout = real
    out = buf.getvalue()
    return "甲" in out and "乙" in out and "2" in out


CHECKS = [
    {
        "id": "signatures",
        "desc": "四个函数的参数个数都对",
        "type": "custom", "fn": "signatures_ok",
        "fail": "照表格来：`show_line(char, width)`、`show_role(name, hp, atk)`、"
                "`deal_damage(attacker, atk, defense)`、`show_team(team)`",
    },
    {
        "id": "line-works",
        "desc": "show_line 真的按参数画线",
        "type": "custom", "fn": "line_flexible",
        "fail": "`show_line(\"@\", 7)` 应该打印 7 个 @。函数体写 `print(char * width)`",
    },
    {
        "id": "line-varied",
        "desc": "show_line 用了 3 种不同的调用",
        "type": "custom", "fn": "line_varied",
        "fail": "换不同的符号和宽度各调一次，才看得出参数的价值",
    },
    {
        "id": "role",
        "desc": "show_role 至少调用 2 次",
        "type": "custom", "fn": "role_twice",
        "fail": "传两个不同的角色各调一次",
    },
    {
        "id": "damage-math",
        "desc": "伤害算得对（88 打 25 = 63）",
        "type": "custom", "fn": "damage_math",
        "fail": "伤害 = `atk - defense`，88 - 25 应该是 63",
    },
    {
        "id": "damage-guard",
        "desc": "伤害保底 1 点，不会出现负数",
        "type": "custom", "fn": "damage_min_guard",
        "fail": "攻击力低于防御力时会算出负数。用 `if damage < 1: damage = 1` 保底",
    },
    {
        "id": "damage-calls",
        "desc": "deal_damage 至少调用 3 次",
        "type": "custom", "fn": "damage_thrice",
        "fail": "调 3 次，其中一次让攻击力小于防御力，验证保底生效",
    },
    {
        "id": "team-works",
        "desc": "show_team 能处理任意列表",
        "type": "custom", "fn": "team_flexible",
        "fail": "传进来的列表要遍历打印，人数用 `len(team)` 算，不要写死",
    },
    {
        "id": "team-called",
        "desc": "show_team 被调用了",
        "type": "custom", "fn": "team_called",
        "fail": "传一个至少 3 人的列表调用一次",
    },
]
