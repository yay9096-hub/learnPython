def has_bg(ctx):
    return bool(ctx["turtle"].get("bg"))


def enough_colors(ctx):
    colors = set()
    for c in ctx["turtle"]["cmds"]:
        if c.get("color"):
            colors.add(str(c["color"]).lower())
    return len(colors) >= 3


def has_fill(ctx):
    return any(c["op"] == "fill" for c in ctx["turtle"]["cmds"])


def enough_dots(ctx):
    return sum(1 for c in ctx["turtle"]["cmds"] if c["op"] == "dot") >= 2


def has_text(ctx):
    for c in ctx["turtle"]["cmds"]:
        if c["op"] == "write" and str(c.get("text", "")).strip():
            return True
    return False


def two_circles(ctx):
    """两层圆环 —— circle() 会被拆成很多小线段，所以数调用次数更靠谱。"""
    code = ctx["code"].replace(" ", "")
    return code.count(".circle(") >= 2


CHECKS = [
    {
        "id": "bg",
        "desc": "设置了画布背景色",
        "type": "custom", "fn": "has_bg",
        "fail": "用 `turtle.bgcolor(\"#1A1625\")` 加个深色底，线条会亮很多",
    },
    {
        "id": "circles",
        "desc": "画了至少两层圆环",
        "type": "custom", "fn": "two_circles",
        "fail": "写两次 `turtle.circle(半径)`。别忘了每次先 `goto(0, -半径)` 让圆心对齐",
    },
    {
        "id": "fill",
        "desc": "有一个填充图形",
        "type": "custom", "fn": "has_fill",
        "fail": "用 `begin_fill()` 和 `end_fill()` 夹住一个闭合图形，中间会被涂满",
    },
    {
        "id": "setheading",
        "desc": "用了 setheading() 指定朝向",
        "type": "ast_calls", "name": "setheading", "min": 1,
        "fail": "画放射线时用 `turtle.setheading(90)` 这种绝对朝向，比一直 right() 好控制",
    },
    {
        "id": "colors",
        "desc": "至少用了三种颜色",
        "type": "custom", "fn": "enough_colors",
        "fail": "多换几次 `pencolor()`，魔法阵要够花才好看 ✨",
    },
    {
        "id": "dots",
        "desc": "点了至少两个装饰点",
        "type": "custom", "fn": "enough_dots",
        "fail": "用 `turtle.dot(18, \"#F59E0B\")` 在几个位置点上装饰点",
    },
    {
        "id": "text",
        "desc": "写上了名字或咒语",
        "type": "custom", "fn": "has_text",
        "fail": "用 `turtle.write(\"你的名字\")` 在阵中心留下签名",
    },
]
