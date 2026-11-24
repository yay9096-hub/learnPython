STARTER = {"atk": 88, "defense": 25, "crit_rate": 1.5}


def _given(ctx, key):
    """atk / defense / crit_rate 是 starter 里给好的。
    她要是改了数值，判题跟着她的数走；要是把变量删了，就用 starter 的默认值。"""
    v = ctx["ns"].get(key, STARTER[key])
    try:
        return float(v)
    except (TypeError, ValueError):
        return float(STARTER[key])


def _has_value(ctx, want, tol=0.06):
    """有任何一个变量等于这个值就算过 —— 变量叫什么名字不重要。"""
    for k, v in ctx["ns"].items():
        if k.startswith("__") or isinstance(v, bool):
            continue
        try:
            if abs(float(v) - want) <= tol:
                return True
        except (TypeError, ValueError):
            continue
    return False


def damage_right(ctx):
    return _has_value(ctx, _given(ctx, "atk") - _given(ctx, "defense"))


def crit_right(ctx):
    base = _given(ctx, "atk") - _given(ctx, "defense")
    return _has_value(ctx, base * _given(ctx, "crit_rate"))


def shows_both(ctx):
    """两个伤害数字都得打印出来。同样不看变量名，只看数字有没有出现在输出里。"""
    out = ctx["stdout"]
    base = _given(ctx, "atk") - _given(ctx, "defense")
    crit = base * _given(ctx, "crit_rate")
    return _num_in(out, base) and _num_in(out, crit)


def _num_in(text, want, tol=0.06):
    import re
    for m in re.finditer(r"-?\d+(?:\.\d+)?", text):
        if abs(float(m.group()) - want) <= tol:
            return True
    return False


def uses_ops(ctx):
    code = ctx["code"]
    return "-" in code and "*" in code


CHECKS = [
    {
        "id": "damage",
        "desc": "算对了普通攻击伤害",
        "type": "custom", "fn": "damage_right",
        "fail": "普通伤害 = `atk - defense`，应该算出 **63**（变量叫什么名字都行）",
    },
    {
        "id": "crit",
        "desc": "算对了暴击伤害",
        "type": "custom", "fn": "crit_right",
        "fail": "暴击 = `(atk - defense) * crit_rate` —— 注意括号！先减再乘，应该算出 **94.5**",
    },
    {
        "id": "round",
        "desc": "用了 round() 保留小数",
        "type": "ast_calls", "name": "round", "min": 1,
        "fail": "暴击伤害是小数，用 `round(结果, 1)` 让它只留一位小数",
    },
    {
        "id": "report",
        "desc": "报告里两个伤害数字都出现了",
        "type": "custom", "fn": "shows_both",
        "fail": "用 f-string 把普通伤害和暴击伤害都打印出来",
    },
    {
        "id": "fstring",
        "desc": "用了 f-string",
        "type": "ast_has", "node": "fstring", "min": 1,
        "fail": "别忘了引号前面那个 `f`",
    },
    {
        "id": "ops",
        "desc": "代码里用到了减法和乘法",
        "type": "custom", "fn": "uses_ops",
        "fail": "公式里应该有 `-` 和 `*`，不要自己心算完直接写答案哦 😉",
    },
]
