def team_is_list(ctx):
    return isinstance(ctx["ns"].get("team"), list)


def team_size(ctx):
    t = ctx["ns"].get("team")
    return isinstance(t, list) and len(t) >= 5


def replaced(ctx):
    """换过人：1 号位现在的名字，和点名日志里最早出现的 1 号不一样。"""
    import re
    out = ctx["stdout"]
    firsts = re.findall(r"^\s*2\s*号[：:]\s*(\S+)", out, re.M)
    if len(firsts) < 2:
        return False
    return firsts[0] != firsts[-1]


def uses_index_assign(ctx):
    """真的用了 team[i] = ... 这种写法，不是重新建了个列表。"""
    import ast
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Subscript):
                    return True
    return False


def uses_for(ctx):
    import ast
    return any(isinstance(n, ast.For) for n in ast.walk(ctx["tree"]))


def roll_call_twice(ctx):
    """点了两次名：编号 1 出现至少两次。"""
    import re
    return len(re.findall(r"^\s*1\s*号[：:]", ctx["stdout"], re.M)) >= 2


CHECKS = [
    {
        "id": "list",
        "desc": "建了一个叫 team 的列表",
        "type": "custom", "fn": "team_is_list",
        "fail": "用方括号建列表：`team = [\"星野樱\", \"月见琉璃\", ...]`",
    },
    {
        "id": "size",
        "desc": "队伍至少 5 人",
        "type": "custom", "fn": "team_size",
        "fail": "名字随你编，但至少要 5 个成员",
    },
    {
        "id": "len",
        "desc": "用 len() 报出了人数",
        "type": "ast_calls", "name": "len", "min": 1,
        "fail": "用 `len(team)` 数人头，别自己数完写死数字 😉",
    },
    {
        "id": "first-last",
        "desc": "单独打印了队长和替补",
        "type": "stdout_contains", "value": ["队长", "替补"],
        "fail": "用 `team[0]` 取队长、`team[-1]` 取替补，各打印一行",
    },
    {
        "id": "for",
        "desc": "用 for 循环点名",
        "type": "custom", "fn": "uses_for",
        "fail": "点名要用 `for i, member in enumerate(team):`，不是一行行 print",
    },
    {
        "id": "twice",
        "desc": "换人前后各点了一次名",
        "type": "custom", "fn": "roll_call_twice",
        "fail": "换人**前**点一次、换人**后**再点一次，才看得出变化",
    },
    {
        "id": "assign",
        "desc": "用 team[编号] = 的方式换人",
        "type": "custom", "fn": "uses_index_assign",
        "fail": "换人要写 `team[1] = \"新名字\"`，不是重新建一个列表",
    },
    {
        "id": "changed",
        "desc": "换人真的生效了",
        "type": "custom", "fn": "replaced",
        "fail": "两次点名里 2 号位的名字应该不一样。检查一下换人那句写在两次点名**中间**没有",
    },
]
