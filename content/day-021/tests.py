# 战斗伤害固定，好让「森林 -> 迎战」这条路能稳定走到胜利结局。
SCRIPT = """
import random
random.randint = lambda a, b: b       # 一律取上限：属性拉满、狼咬得最疼也扛得住
"""


def uses_while(ctx):
    import ast
    return any(isinstance(n, ast.While) for n in ast.walk(ctx["tree"]))


def enough_branches(ctx):
    import ast
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.If)) >= 4


def enough_inputs(ctx):
    import ast
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "input")
    return n >= 3


def uses_random(ctx):
    import ast
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.Import):
            if any(a.name.split(".")[0] == "random" for a in node.names):
                return True
    return False


def long_enough(ctx):
    return len([l for l in ctx["stdout"].splitlines() if l.strip()]) >= 10


CASES = [
    {
        "setup": SCRIPT,
        "stdin": ["星野樱", "1", "1"],
        "checks": [
            {
                "id": "name",
                "desc": "问了名字并用上了",
                "type": "stdout_contains", "value": "星野樱",
                "fail": "问玩家名字，之后的剧情里要用 f-string 把它显示出来",
            },
            {
                "id": "random",
                "desc": "用 random 生成了初始属性",
                "type": "custom", "fn": "uses_random",
                "fail": "HP 和攻击力要用 `random.randint(...)` 随机生成",
            },
            {
                "id": "inputs",
                "desc": "至少 3 次输入（名字 + 两个选择点）",
                "type": "custom", "fn": "enough_inputs",
                "fail": "名字一次、两个选择点各一次，至少三个 `input()`",
            },
            {
                "id": "while",
                "desc": "用 while 做了输入校验",
                "type": "custom", "fn": "uses_while",
                "fail": "用 `while choice not in [\"1\", \"2\"]:` 让玩家输错时能重问",
            },
            {
                "id": "branches",
                "desc": "分支够多（至少 4 个 if）",
                "type": "custom", "fn": "enough_branches",
                "fail": "两个选择点 + 三种结局，`if` 应该不止 4 个",
            },
            {
                "id": "route1",
                "desc": "路线 1-1 能走到结局",
                "type": "stdout_contains", "value": "结局",
                "fail": "选「1 森林」再选「1 迎战」应该能走到一个结局",
            },
            {
                "id": "rich",
                "desc": "剧情内容够丰富",
                "type": "custom", "fn": "long_enough",
                "fail": "输出至少 10 行 —— 加点场景描写和战况，游戏才有味道",
            },
        ],
    },
    {
        "setup": SCRIPT,
        "stdin": ["月见琉璃", "2", "1"],
        "checks": [
            {
                "id": "route2",
                "desc": "路线 2-1 也能走到结局",
                "type": "stdout_contains", "value": "结局",
                "fail": "选「2 洞穴」这条路也要能走到结局，不能卡住或崩掉",
            },
            {
                "id": "route2-name",
                "desc": "第二条路线也认名字",
                "type": "stdout_contains", "value": "月见琉璃",
                "fail": "无论走哪条路，结局里都要出现玩家的名字",
            },
        ],
    },
    {
        "setup": SCRIPT,
        "stdin": ["天野灯", "9", "x", "2", "2"],
        "checks": [
            {
                "id": "validate",
                "desc": "输错了不会崩，会重问",
                "type": "stdout_contains", "value": "结局",
                "fail": "玩家输入了 `9` 和 `x` 这种无效选项时，"
                        "要用 `while` 重新问，而不是直接崩掉或跳过",
            },
        ],
    },
]
