def uses_zip(ctx):
    import ast
    return any(isinstance(n, ast.Call) and getattr(n.func, "id", None) == "zip"
               for n in ast.walk(ctx["tree"]))


def uses_unpack(ctx):
    """for 的循环变量里有元组解包，比如 for name, (x, y), size in ..."""
    import ast
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.For) and isinstance(n.target, ast.Tuple):
            return True
    return False


def all_listed(ctx):
    out = ctx["stdout"]
    return all(n in out for n in ["天枢", "天璇", "天玑", "天权", "玉衡", "开阳", "摇光"])


def row_ok(ctx):
    """一行里同时有名字、坐标、亮度。"""
    import re
    return re.search(r"天枢[^\n]*-160[^\n]*40[^\n]*10", ctx["stdout"]) is not None


def _has(ctx, want, tol=0.05):
    for k, v in ctx["ns"].items():
        if k.startswith("__") or isinstance(v, bool):
            continue
        try:
            if abs(float(v) - want) <= tol:
                return True
        except (TypeError, ValueError):
            continue
    return False


def center_x_ok(ctx):
    return _has(ctx, 12.9)


def center_y_ok(ctx):
    return _has(ctx, 47.1)


def brightest(ctx):
    import re
    return re.search(r"摇光[^\n]*12|12[^\n]*摇光", ctx["stdout"]) is not None


def drew_stars(ctx):
    return sum(1 for c in ctx["turtle"]["cmds"] if c["op"] == "dot") >= 7


def drew_lines(ctx):
    return sum(1 for c in ctx["turtle"]["cmds"] if c["op"] == "line") >= 6


def varied_dots(ctx):
    sizes = {round(float(c.get("r", 0)), 2)
             for c in ctx["turtle"]["cmds"] if c["op"] == "dot"}
    return len(sizes) >= 3


def wrote_label(ctx):
    for c in ctx["turtle"]["cmds"]:
        if c["op"] == "write" and "摇光" in str(c.get("text", "")):
            return True
    return False


def has_bg(ctx):
    return bool(ctx["turtle"].get("bg"))


CHECKS = [
    {
        "id": "zip",
        "desc": "用 zip() 配对三组数据",
        "type": "custom", "fn": "uses_zip",
        "fail": "`for name, (x, y), size in zip(names, points, sizes):` —— 三个列表一起配",
    },
    {
        "id": "unpack",
        "desc": "遍历时把坐标解包成 x, y",
        "type": "custom", "fn": "uses_unpack",
        "fail": "循环变量写成 `name, (x, y), size`，括号里的元组会被自动拆成两个变量",
    },
    {
        "id": "listed",
        "desc": "七颗星都显示了",
        "type": "custom", "fn": "all_listed",
        "fail": "七颗星的名字都要打印出来",
    },
    {
        "id": "row",
        "desc": "每行三项信息齐全",
        "type": "custom", "fn": "row_ok",
        "fail": "一行里要有名字、坐标、亮度，像 `天枢 (-160, 40) 亮度 10`",
    },
    {
        "id": "cx",
        "desc": "x 平均值算对了（12.9）",
        "type": "custom", "fn": "center_x_ok",
        "fail": "七个 x 加起来是 90，除以 7 约等于 **12.9**（记得 round 保留 1 位）",
    },
    {
        "id": "cy",
        "desc": "y 平均值算对了（47.1）",
        "type": "custom", "fn": "center_y_ok",
        "fail": "七个 y 加起来是 330，除以 7 约等于 **47.1**",
    },
    {
        "id": "brightest",
        "desc": "找对了最亮的星",
        "type": "custom", "fn": "brightest",
        "fail": "最亮的是**摇光（12）**，名字和亮度要在同一行报出来",
    },
    {
        "id": "bg",
        "desc": "画了深色背景",
        "type": "custom", "fn": "has_bg",
        "fail": "`turtle.bgcolor(\"#0B0A1A\")` —— 星空要黑底",
    },
    {
        "id": "dots",
        "desc": "七颗星都画出来了",
        "type": "custom", "fn": "drew_stars",
        "fail": "每颗星画一个 `turtle.dot(...)`，七颗都要有",
    },
    {
        "id": "sizes",
        "desc": "星星大小跟亮度挂钩",
        "type": "custom", "fn": "varied_dots",
        "fail": "`turtle.dot(size * 2, ...)` —— 用 size 决定大小，星星才有明暗层次",
    },
    {
        "id": "lines",
        "desc": "七颗星连成了折线",
        "type": "custom", "fn": "drew_lines",
        "fail": "七个点之间要有 6 条连线。第一个点之前 `penup()`，到位后 `pendown()`",
    },
    {
        "id": "label",
        "desc": "标注了最亮的星名",
        "type": "custom", "fn": "wrote_label",
        "fail": "用 `turtle.write(best_name, ...)` 在摇光旁边写上名字",
    },
]
