def uses_for(ctx):
    import ast
    return any(isinstance(n, ast.For) for n in ast.walk(ctx["tree"]))


def enough_stars(ctx):
    return sum(1 for c in ctx["turtle"]["cmds"] if c["op"] == "dot") >= 60


def varied_sizes(ctx):
    sizes = {round(float(c.get("r", 0)), 2)
             for c in ctx["turtle"]["cmds"] if c["op"] == "dot"}
    return len(sizes) >= 3


def varied_positions(ctx):
    pts = {(round(c["x"]), round(c["y"]))
           for c in ctx["turtle"]["cmds"] if c["op"] == "dot"}
    return len(pts) >= 50


def enough_colors(ctx):
    colors = {str(c.get("color", "")).lower()
              for c in ctx["turtle"]["cmds"] if c["op"] == "dot"}
    return len(colors) >= 3


def has_bg(ctx):
    return bool(ctx["turtle"].get("bg"))


def has_moon(ctx):
    return any(c["op"] == "fill" for c in ctx["turtle"]["cmds"])


def uses_if(ctx):
    import ast
    return any(isinstance(n, ast.If) for n in ast.walk(ctx["tree"]))


def no_copy_paste(ctx):
    code = ctx["code"].replace(" ", "")
    return code.count(".dot(") + code.count(".circle(") <= 6


CHECKS = [
    {
        "id": "for",
        "desc": "用 for 循环撒星星",
        "type": "custom", "fn": "uses_for",
        "fail": "星星要用 `for i in range(...)` 生成",
    },
    {
        "id": "count",
        "desc": "撒了至少 60 颗星",
        "type": "custom", "fn": "enough_stars",
        "fail": "循环次数调到 60 以上，星空才够密",
    },
    {
        "id": "positions",
        "desc": "位置是随机的",
        "type": "custom", "fn": "varied_positions",
        "fail": "用 `turtle.goto(random.randint(-250, 250), random.randint(-190, 190))` 随机落点",
    },
    {
        "id": "sizes",
        "desc": "星星有大有小",
        "type": "custom", "fn": "varied_sizes",
        "fail": "`turtle.dot(random.randint(2, 8))` —— 大小也随机，才有远近层次",
    },
    {
        "id": "colors",
        "desc": "至少三种颜色",
        "type": "custom", "fn": "enough_colors",
        "fail": "用 `random.choice(palette)` 从色板里随机挑颜色",
    },
    {
        "id": "if",
        "desc": "用 if 做出少数亮星",
        "type": "custom", "fn": "uses_if",
        "fail": "`if random.randint(1, 10) == 1:` 就是十分之一的概率，用它画几颗特别大的",
    },
    {
        "id": "bg",
        "desc": "设置了深色背景",
        "type": "custom", "fn": "has_bg",
        "fail": "`turtle.bgcolor(\"#0B0A1A\")` —— 没有黑底就不叫星空了",
    },
    {
        "id": "moon",
        "desc": "画了月亮（有填充图形）",
        "type": "custom", "fn": "has_moon",
        "fail": "用 `begin_fill()` / `circle()` / `end_fill()` 画一个填了色的月亮",
    },
    {
        "id": "no-copy",
        "desc": "没有复制粘贴 dot",
        "type": "custom", "fn": "no_copy_paste",
        "fail": "`dot` 和 `circle` 加起来最多写 6 次，剩下交给循环 😉",
    },
]
