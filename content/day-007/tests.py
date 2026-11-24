# 测试输入：星野樱 / 16 / fire / 7
#   hp   = 16 * 20 + 7      = 327
#   mp   = 16 * 10 + 7 * 2  = 174
#   rank = len("星野樱")     = 3

BOX_CHARS = "═║╔╗╚╝─│┌┐└┘+-|*=~"
TRIPLE_SINGLE = chr(39) * 3


def uses_triple(ctx):
    code = ctx["code"]
    return "\"\"\"" in code or TRIPLE_SINGLE in code


def has_box(ctx):
    hits = 0
    for line in ctx["stdout"].splitlines():
        s = line.strip()
        if len(s) >= 8 and sum(1 for ch in s if ch in BOX_CHARS) >= 8:
            hits += 1
    return hits >= 2


def _eq(ctx, var, want):
    return var in ctx["ns"] and str(ctx["ns"][var]) == want


def hp_ok(ctx):
    return _eq(ctx, "hp", "327")


def mp_ok(ctx):
    return _eq(ctx, "mp", "174")


def rank_ok(ctx):
    return _eq(ctx, "rank", "3")


def title_ok(ctx):
    return _eq(ctx, "title", "FIRE")


def stars_ok(ctx):
    return "★★★" in ctx["stdout"] or "☆☆☆" in ctx["stdout"]


def uses_newline_escape(ctx):
    return "\n" in ctx["code"]


CASES = [
    {
        "stdin": ["  星野樱  ", "16", "fire", "7"],
        "checks": [
            {
                "id": "title-screen",
                "desc": "第一幕：三引号做的标题画面",
                "type": "custom", "fn": "uses_triple",
                "fail": "用三引号打印一个标题框（Day 6 学过的）",
            },
            {
                "id": "box",
                "desc": "标题框有上下边框",
                "type": "custom", "fn": "has_box",
                "fail": "标题框至少要有两条边框线，让它看起来像个「框」",
            },
            {
                "id": "inputs",
                "desc": "第二幕：问了 4 个问题",
                "type": "ast_calls", "name": "input", "min": 4,
                "fail": "名字、年龄、属性、幸运数字，一共四问",
            },
            {
                "id": "hp",
                "desc": "算对了 HP",
                "type": "custom", "fn": "hp_ok",
                "fail": "`hp = age * 20 + lucky`。测试数据是 16 和 7，答案应该是 327",
            },
            {
                "id": "mp",
                "desc": "算对了 MP",
                "type": "custom", "fn": "mp_ok",
                "fail": "`mp = age * 10 + lucky * 2`。注意 lucky 要乘 2，答案是 174",
            },
            {
                "id": "rank",
                "desc": "算对了阶数",
                "type": "custom", "fn": "rank_ok",
                "fail": "`rank = len(name)`。记得先 `.strip()`，不然空格会被算进去！",
            },
            {
                "id": "title",
                "desc": "属性变成了大写",
                "type": "custom", "fn": "title_ok",
                "fail": "`title = element.upper()`，fire 要变成 FIRE",
            },
            {
                "id": "stars",
                "desc": "第三幕：星星线出现了",
                "type": "custom", "fn": "stars_ok",
                "fail": "用 `\"★\" * rank` 生成星星线并打印出来",
            },
            {
                "id": "card",
                "desc": "角色卡上信息齐全",
                "type": "stdout_contains", "value": ["星野樱", "FIRE", "327", "174"],
                "fail": "角色卡上要能看到名字、大写属性、HP、MP 四样",
            },
            {
                "id": "narration",
                "desc": "旁白用了 \n 换行",
                "type": "custom", "fn": "uses_newline_escape",
                "fail": "最后的旁白里用一次 `\n`，让它分成两行",
            },
        ],
    }
]
