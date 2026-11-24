def signature_not_empty(ctx):
    for c in ctx["turtle"]["cmds"]:
        if c["op"] == "write" and str(c.get("text", "")).strip():
            return True
    return False


def turned_144(ctx):
    """五角星的关键：转了至少 4 次 144 度。"""
    code = ctx["code"].replace(" ", "")
    return code.count("(144)") >= 4


CHECKS = [
    {
        "id": "import",
        "desc": "把 turtle 工具箱搬进来了",
        "type": "ast_imports", "name": "turtle",
        "fail": "第一行要写 `import turtle`，不然小海龟不会来 🐢",
    },
    {
        "id": "star-lines",
        "desc": "五角星画了 5 条边",
        "type": "turtle_min_ops", "op": "line", "min": 5,
        "fail": "五角星有 5 条边，要写 5 个 `turtle.forward(...)`",
    },
    {
        "id": "angle",
        "desc": "每个尖角转了 144 度",
        "type": "custom", "fn": "turned_144",
        "fail": "五角星的转角是 144 度。写 `turtle.right(144)`，一共要转 4 次以上",
    },
    {
        "id": "pensize",
        "desc": "设置了画笔粗细",
        "type": "ast_calls", "name": "pensize", "min": 1,
        "fail": "用 `turtle.pensize(5)` 把线条调粗一点，会好看很多",
    },
    {
        "id": "colors",
        "desc": "至少用了两种颜色",
        "type": "turtle_colors_min", "min": 2,
        "fail": "星星一个颜色、光环另一个颜色 —— 用 `turtle.pencolor(\"#8B5CF6\")` 换色",
    },
    {
        "id": "circle",
        "desc": "画了一个圆当光环",
        "type": "ast_calls", "name": "circle", "min": 1,
        "fail": "用 `turtle.circle(120)` 画一个圆环",
    },
    {
        "id": "penup",
        "desc": "换位置的时候抬笔了",
        "type": "ast_calls", "name": "penup", "min": 1,
        "fail": "挪窝之前先 `turtle.penup()`，不然会拖出一条不想要的线",
    },
    {
        "id": "sign",
        "desc": "用 write() 署名了",
        "type": "custom", "fn": "signature_not_empty",
        "fail": "用 `turtle.write(\"你的名字\")` 在画上签个名 ✍️",
    },
]
