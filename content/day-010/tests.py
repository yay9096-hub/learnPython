RARITIES = ["SSR", "SR", "R", "N"]


def _has(ctx, var):
    return var in ctx["ns"] and str(ctx["ns"][var]).strip() != ""


def rarity_ok(ctx):
    return _has(ctx, "rarity") and str(ctx["ns"]["rarity"]).upper() in RARITIES


def atk_ok(ctx):
    if "atk" not in ctx["ns"]:
        return False
    try:
        return 1 <= int(ctx["ns"]["atk"]) <= 9999
    except Exception:
        return False


def card_printed(ctx):
    out = ctx["stdout"]
    ns = ctx["ns"]
    for var in ["rarity", "char", "element", "atk"]:
        if var not in ns or str(ns[var]) not in out:
            return False
    return True


def frame_drawn(ctx):
    return sum(1 for c in ctx["turtle"]["cmds"] if c["op"] == "line") >= 4


def frame_text(ctx):
    for c in ctx["turtle"]["cmds"]:
        if c["op"] == "write" and str(c.get("text", "")).strip():
            return True
    return False


def choice_count(ctx):
    return ctx["code"].replace(" ", "").count(".choice(") >= 3


CASES = [
    {
        "stdin": ["星野樱"],
        "checks": [
            {
                "id": "imports",
                "desc": "搬进了 random 工具箱",
                "type": "ast_imports", "name": "random",
                "fail": "开头要写 `import random`",
            },
            {
                "id": "player",
                "desc": "问了玩家名字",
                "type": "ast_calls", "name": "input", "min": 1,
                "fail": "用 `player = input(\"报上名来：\")` 问一下玩家的名字",
            },
            {
                "id": "choices",
                "desc": "用了 3 次 random.choice",
                "type": "custom", "fn": "choice_count",
                "fail": "稀有度、角色、属性都要用 `random.choice([...])` 随机抽",
            },
            {
                "id": "rarity",
                "desc": "抽出了合法的稀有度",
                "type": "custom", "fn": "rarity_ok",
                "fail": "`rarity` 要从 SSR / SR / R / N 里抽一个出来",
            },
            {
                "id": "atk",
                "desc": "用 randint 抽了攻击力",
                "type": "custom", "fn": "atk_ok",
                "fail": "`atk = random.randint(50, 999)`，记得存进名叫 atk 的变量",
            },
            {
                "id": "card",
                "desc": "卡面上四项信息齐全",
                "type": "custom", "fn": "card_printed",
                "fail": "稀有度、角色、属性、攻击力 —— 四样都要打印到卡面上",
            },
            {
                "id": "player-shown",
                "desc": "卡面上出现了玩家名字",
                "type": "stdout_contains", "value": "星野樱",
                "fail": "把玩家的名字也印在卡面上，有仪式感一点 ✨",
            },
            {
                "id": "frame",
                "desc": "turtle 画出了卡框",
                "type": "custom", "fn": "frame_drawn",
                "fail": "用 turtle 画一个矩形当卡框，需要 4 条 `forward()`",
            },
            {
                "id": "frame-text",
                "desc": "卡框里写上了角色名",
                "type": "custom", "fn": "frame_text",
                "fail": "用 `turtle.write(char)` 把角色名写进卡框",
            },
        ],
    }
]
