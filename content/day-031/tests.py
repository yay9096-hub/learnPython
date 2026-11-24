def all_listed(ctx):
    out = ctx["stdout"]
    return all(n in out for n in
               ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪", "风见幽香"])


def full_row(ctx):
    """一行里同时有名字、HP、ATK、属性。"""
    import re
    return re.search(r"星野樱[^\n]*340[^\n]*88[^\n]*火", ctx["stdout"]) is not None


def uses_sort_key(ctx):
    return "key=lambda" in ctx["code"].replace(" ", "").replace("key=lambda", "key=lambda")


def sorted_by_atk(ctx):
    """排序后 team 里第一个应该是水城凛（110）。"""
    t = ctx["ns"].get("team")
    if not isinstance(t, list) or not t:
        return False
    return t[0].get("name") == "水城凛"


def strong_ok(ctx):
    """筛出来 4 个人。"""
    for k, v in ctx["ns"].items():
        if k.startswith("__") or k == "team":
            continue
        if isinstance(v, list) and len(v) == 4 and all(isinstance(x, dict) for x in v):
            names = {x.get("name") for x in v}
            if names == {"星野樱", "月见琉璃", "水城凛", "风见幽香"}:
                return True
    return False


def member_added(ctx):
    t = ctx["ns"].get("team")
    return isinstance(t, list) and len(t) == 7


def hp_boosted(ctx):
    """全员 +50 之后，星野樱应该是 390。"""
    t = ctx["ns"].get("team")
    if not isinstance(t, list):
        return False
    for m in t:
        if m.get("name") == "星野樱":
            return m.get("hp") == 390
    return False


def nested_access(ctx):
    """真的用了 m["字段"] 这种取值方式。"""
    import ast
    return any(isinstance(n, ast.Subscript) for n in ast.walk(ctx["tree"]))


CASES = [
    {
        "stdin": ["水"],
        "checks": [
            {
                "id": "listed",
                "desc": "全队六人都显示了",
                "type": "custom", "fn": "all_listed",
                "fail": "用 `for m in team:` 遍历，每人打印一行",
            },
            {
                "id": "row",
                "desc": "每行四项信息齐全",
                "type": "custom", "fn": "full_row",
                "fail": "一行里要有名字、HP、ATK、属性。用 `m['name']`、`m['hp']` 这样取",
            },
            {
                "id": "access",
                "desc": "用字段名取值",
                "type": "custom", "fn": "nested_access",
                "fail": "每一项是字典，用 `m[\"name\"]` 取字段，不是 `m[0]`",
            },
            {
                "id": "total",
                "desc": "总血量算对了（1960）",
                "type": "value_present", "value": 1960,
                "fail": "340+280+310+250+420+360 = **1960**（在加血之前算）",
            },
            {
                "id": "avg",
                "desc": "平均攻击算对了（86.8）",
                "type": "value_present", "value": 86.8, "tol": 0.05,
                "fail": "521 ÷ 6 = 86.8（记得 `round(..., 1)`）",
            },
            {
                "id": "sortkey",
                "desc": "用 key=lambda 排序",
                "type": "custom", "fn": "uses_sort_key",
                "fail": "`team.sort(key=lambda m: m[\"atk\"], reverse=True)` —— 固定句式，照抄改字段名",
            },
            {
                "id": "sorted",
                "desc": "排序结果正确",
                "type": "custom", "fn": "sorted_by_atk",
                "fail": "按攻击力从高到低，第一个应该是**水城凛（110）**",
            },
            {
                "id": "strong",
                "desc": "筛出了 4 名高攻成员",
                "type": "custom", "fn": "strong_ok",
                "fail": "攻击 >= 88 的是 星野樱88 / 月见琉璃95 / 水城凛110 / 风见幽香90，"
                        "共 **4 人**。套路：建空列表 → 遍历 → 符合就 append",
            },
            {
                "id": "added",
                "desc": "新增了一名成员（7 人）",
                "type": "custom", "fn": "member_added",
                "fail": "`team.append({\"name\": ..., \"hp\": ..., \"atk\": ..., \"element\": ...})` —— "
                        "加进去的必须是一整个字典",
            },
            {
                "id": "boost",
                "desc": "全员血量 +50 生效了",
                "type": "custom", "fn": "hp_boosted",
                "fail": "遍历时写 `m[\"hp\"] += 50`，星野樱应该从 340 变成 390",
            },
            {
                "id": "query",
                "desc": "查到了水属性成员",
                "type": "stdout_contains", "value": ["月见琉璃", "水城凛"],
                "fail": "水属性有月见琉璃和水城凛两人，都要列出来",
            },
        ],
    },
    {
        "stdin": ["雷"],
        "checks": [
            {
                "id": "not-found",
                "desc": "查不到的属性有提示",
                "type": "stdout_contains", "value": "没有这个属性",
                "fail": "队里没有雷属性，要提示「没有这个属性的成员」",
            },
        ],
    },
]
