def two_loops(ctx):
    import ast
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.For)) >= 2


def nested_loop(ctx):
    """循环里面还有循环 —— 万花筒的关键结构。"""
    import ast
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.For):
            for child in ast.walk(n):
                if isinstance(child, ast.For) and child is not n:
                    return True
    return False


def few_forwards(ctx):
    """靠循环生成，不是复制粘贴。forward 顶多写两次。"""
    return ctx["code"].replace(" ", "").count(".forward(") <= 2


def enough_lines(ctx):
    """嵌套循环至少要画出几十条线。"""
    return sum(1 for c in ctx["turtle"]["cmds"] if c["op"] == "line") >= 30


def has_bg(ctx):
    return bool(ctx["turtle"].get("bg"))


def enough_colors(ctx):
    colors = {str(c["color"]).lower() for c in ctx["turtle"]["cmds"] if c.get("color")}
    return len(colors) >= 3


CHECKS = [
    {
        "id": "loops",
        "desc": "用了两个以上的 for 循环",
        "type": "custom", "fn": "two_loops",
        "fail": "一个循环画基本图形，一个循环负责旋转重复",
    },
    {
        "id": "nested",
        "desc": "循环里面套了循环",
        "type": "custom", "fn": "nested_loop",
        "fail": "内层 `for` 要写在外层 `for` 的**里面**（缩进 8 格）",
    },
    {
        "id": "no-copy",
        "desc": "没有复制粘贴 forward",
        "type": "custom", "fn": "few_forwards",
        "fail": "`turtle.forward(...)` 最多写两次 —— 剩下的交给循环 😉",
    },
    {
        "id": "lines",
        "desc": "画出了足够多的线条",
        "type": "custom", "fn": "enough_lines",
        "fail": "至少要画 30 条线。旋转次数调到 8 以上试试",
    },
    {
        "id": "colors",
        "desc": "至少用了三种颜色",
        "type": "custom", "fn": "enough_colors",
        "fail": "用 `turtle.pencolor(colors[i % 4])` 让每层颜色都不一样",
    },
    {
        "id": "bg",
        "desc": "设置了背景色",
        "type": "custom", "fn": "has_bg",
        "fail": "用 `turtle.bgcolor(\"#1A1625\")` 加个深色底，线条会亮很多",
    },
    {
        "id": "angle",
        "desc": "旋转角度是算出来的",
        "type": "ast_calls", "name": "right", "min": 1,
        "fail": "用 `turtle.right(360 / layers)` 把角度算出来，别自己心算填死",
    },
]
