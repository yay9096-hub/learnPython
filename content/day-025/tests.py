def uses_sum(ctx):
    import ast
    return any(isinstance(n, ast.Call) and getattr(n.func, "id", None) == "sum"
               for n in ast.walk(ctx["tree"]))


def uses_for(ctx):
    import ast
    return any(isinstance(n, ast.For) for n in ast.walk(ctx["tree"]))


def uses_if_in_loop(ctx):
    """条件统计：循环里必须有 if。"""
    import ast
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.For):
            for child in ast.walk(node):
                if isinstance(child, ast.If):
                    return True
    return False


def few_prints(ctx):
    import ast
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "print")
    return n <= 10


def _has(ctx, want, tol=0.05):
    for k, v in ctx["ns"].items():
        if k.startswith("__") or isinstance(v, bool):
            continue
        try:
            if abs(float(v) - want) <= tol:
                return True
        except (TypeError, ValueError):
            continue
    return False


def total_ok(ctx):
    return _has(ctx, 1600)


def avg_ok(ctx):
    return _has(ctx, 86.2)


def strong_ok(ctx):
    return _has(ctx, 3)


def all_members_listed(ctx):
    out = ctx["stdout"]
    return all(n in out for n in ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"])


CHECKS = [
    {
        "id": "for",
        "desc": "用循环逐行显示成员",
        "type": "custom", "fn": "uses_for",
        "fail": "用 `for i in range(len(names)):` 遍历，别一行行手写",
    },
    {
        "id": "few-prints",
        "desc": "没有一行行手写 print",
        "type": "custom", "fn": "few_prints",
        "fail": "print 写太多了 😉 成员列表要靠循环生成",
    },
    {
        "id": "members",
        "desc": "五个成员都显示了",
        "type": "custom", "fn": "all_members_listed",
        "fail": "五个人的名字都要出现在面板上",
    },
    {
        "id": "paired",
        "desc": "名字和数值对上号了",
        "type": "stdout_regex",
        "pattern": "星野樱[^\n]*340[^\n]*88",
        "fail": "同一行里要同时有名字、HP、ATK。用同一个编号 `i` 从三个列表里取",
    },
    {
        "id": "sum",
        "desc": "用 sum() 算了总和",
        "type": "custom", "fn": "uses_sum",
        "fail": "`total_hp = sum(hps)` —— 有现成的就别自己写循环了",
    },
    {
        "id": "total",
        "desc": "总血量算对了（1600）",
        "type": "custom", "fn": "total_ok",
        "fail": "340+280+310+250+420 = **1600**",
    },
    {
        "id": "avg",
        "desc": "平均攻击力算对了（86.2）",
        "type": "custom", "fn": "avg_ok",
        "fail": "`sum(atks) / len(atks)` 再 `round(..., 1)`，答案是 **86.2**",
    },
    {
        "id": "top",
        "desc": "找对了血量最高的成员",
        "type": "stdout_regex", "pattern": "夜刀神澪[^\n]*420|420[^\n]*夜刀神澪",
        "fail": "血量最高的是**夜刀神澪（420）**，名字和数值要在同一行报出来",
    },
    {
        "id": "low",
        "desc": "找对了血量最低的成员",
        "type": "stdout_regex", "pattern": "水城凛[^\n]*250|250[^\n]*水城凛",
        "fail": "血量最低的是**水城凛（250）**",
    },
    {
        "id": "if-loop",
        "desc": "用循环 + if 做了条件统计",
        "type": "custom", "fn": "uses_if_in_loop",
        "fail": "「血量超过 300 的有几人」这种统计 `sum()` 做不了，要靠 `for` + `if`",
    },
    {
        "id": "strong",
        "desc": "条件统计算对了（3 人）",
        "type": "custom", "fn": "strong_ok",
        "fail": "340、310、420 三个超过 300，答案是 **3 人**",
    },
]
