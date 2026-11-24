def uses_set(ctx):
    import ast
    return any(isinstance(n, ast.Call) and getattr(n.func, "id", None) == "set"
               for n in ast.walk(ctx["tree"]))


def uses_ops(ctx):
    """三种集合运算符都用上了。"""
    import ast
    ops = set()
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.BinOp):
            ops.add(type(n.op).__name__)
    return {"BitAnd", "BitOr", "Sub"} <= ops


def uses_sorted(ctx):
    import ast
    return any(isinstance(n, ast.Call) and getattr(n.func, "id", None) == "sorted"
               for n in ast.walk(ctx["tree"]))


def _find_set(ctx, want):
    for k, v in ctx["ns"].items():
        if k.startswith("__"):
            continue
        if isinstance(v, set) and v == want:
            return True
    return False


def my_set_ok(ctx):
    return _find_set(ctx, {"星野樱", "月见琉璃", "天野灯", "水城凛"})


def common_ok(ctx):
    return _find_set(ctx, {"月见琉璃", "水城凛"})


def union_ok(ctx):
    return _find_set(ctx, {"星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪", "风见幽香"})


def only_mine_ok(ctx):
    return _find_set(ctx, {"星野樱", "天野灯"})


def only_hers_ok(ctx):
    return _find_set(ctx, {"夜刀神澪", "风见幽香"})


def all_common_ok(ctx):
    return _find_set(ctx, {"水城凛"})


CHECKS = [
    {
        "id": "set",
        "desc": "用 set() 做了去重",
        "type": "custom", "fn": "uses_set",
        "fail": "`my_set = set(mine)` —— 一行就去重了，不用再写循环",
    },
    {
        "id": "dedup",
        "desc": "去重结果正确（4 人）",
        "type": "custom", "fn": "my_set_ok",
        "fail": "我的列表有 6 条，其中「星野樱」和「月见琉璃」各重复一次，去重后是 **4 人**",
    },
    {
        "id": "dedup-shown",
        "desc": "报出了去重前后的数量",
        "type": "stdout_contains", "value": ["6", "4"],
        "fail": "把 `len(mine)` 和 `len(my_set)` 都打印出来，才看得出去重的效果",
    },
    {
        "id": "ops",
        "desc": "三种集合运算都用了（& | -）",
        "type": "custom", "fn": "uses_ops",
        "fail": "交集用 `&`、并集用 `|`、差集用 `-`，三个都要用到",
    },
    {
        "id": "common",
        "desc": "共同好友算对了",
        "type": "custom", "fn": "common_ok",
        "fail": "`my_set & her_set` 应该是 月见琉璃、水城凛 两人",
    },
    {
        "id": "union",
        "desc": "并集算对了（6 人）",
        "type": "custom", "fn": "union_ok",
        "fail": "`my_set | her_set` 合起来去重是 6 人",
    },
    {
        "id": "only-mine",
        "desc": "只有我认识的算对了",
        "type": "custom", "fn": "only_mine_ok",
        "fail": "`my_set - her_set` 应该是 星野樱、天野灯",
    },
    {
        "id": "only-hers",
        "desc": "只有她认识的算对了",
        "type": "custom", "fn": "only_hers_ok",
        "fail": "`her_set - my_set` 应该是 夜刀神澪、风见幽香。"
                "⚠️ 差集有方向，两边不能写反",
    },
    {
        "id": "all-common",
        "desc": "三人共同好友算对了",
        "type": "custom", "fn": "all_common_ok",
        "fail": "`my_set & her_set & his_set` —— `&` 可以连着用，答案是 **水城凛** 一人",
    },
    {
        "id": "sorted",
        "desc": "显示前排了序",
        "type": "custom", "fn": "uses_sorted",
        "fail": "集合没有顺序，打印前用 `sorted(集合)` 排一下，输出才稳定",
    },
]
