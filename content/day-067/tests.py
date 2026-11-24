import ast

NEEDED = ["koch", "snowflake", "draw_at", "count_segments"]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def koch_recursive(ctx):
    """koch 里要调用自己，而且至少 4 次。"""
    fn = _funcs(ctx).get("koch")
    if fn is None:
        return False
    n = sum(1 for x in ast.walk(fn)
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "koch")
    return n >= 4


def koch_has_exit(ctx):
    """出口条件：depth == 0 时画直线然后 return。"""
    fn = _funcs(ctx).get("koch")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.If):
            if any(isinstance(x, ast.Return) for x in ast.walk(n)):
                return True
    return False


def koch_divides(ctx):
    """递归时长度要除以 3。"""
    fn = _funcs(ctx).get("koch")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "koch":
            for a in n.args:
                if isinstance(a, ast.BinOp) and isinstance(a.op, ast.Div):
                    return True
    return False


def angles_cancel(ctx):
    """三个转角必须是 60 / 120 / 60，加起来抵消。"""
    src = ctx["code"].replace(" ", "")
    return "(60)" in src and "(120)" in src


def snowflake_loops(ctx):
    """雪花是循环 3 次画的。"""
    fn = _funcs(ctx).get("snowflake")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.For):
            for sub in ast.walk(n):
                if isinstance(sub, ast.Call) and getattr(sub.func, "id", None) == "koch":
                    return True
    return False


def count_correct(ctx):
    fn = ctx["ns"].get("count_segments")
    if not callable(fn):
        return False
    return fn(0) == 1 and fn(1) == 4 and fn(3) == 64 and fn(5) == 1024


def draw_at_moves(ctx):
    """draw_at 要抬笔移动再落笔，否则会拖线。"""
    fn = _funcs(ctx).get("draw_at")
    if fn is None:
        return False
    called = {n.func.attr for n in ast.walk(fn)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    return {"penup", "goto", "pendown"} <= called


def three_flakes(ctx):
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "draw_at")
    if n >= 3:
        return True
    # 也允许用循环 + 数据表的写法
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.For):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and getattr(sub.func, "id", None) == "draw_at":
                    return True
    return False


def enough_lines(ctx):
    """至少一片 depth>=3（一片 192 段），三片加起来应该几百段。"""
    return sum(1 for c in ctx["turtle"]["cmds"] if c["op"] == "line") >= 250


def has_dark_bg(ctx):
    bg = ctx["turtle"].get("bg")
    if not bg:
        return False
    text = str(bg).lstrip("#")
    if len(text) != 6:
        return True
    try:
        r, g, b = (int(text[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return True
    return (r + g + b) / 3 < 128


def varied_colors(ctx):
    colors = {c.get("color") for c in ctx["turtle"]["cmds"]
              if c["op"] == "line" and c.get("color")}
    return len(colors) >= 3


def varied_widths(ctx):
    widths = {round(float(c.get("w", 0)), 2)
              for c in ctx["turtle"]["cmds"] if c["op"] == "line"}
    return len(widths) >= 2


def uses_speed_zero(ctx):
    src = ctx["code"].replace(" ", "")
    return "speed(0)" in src


def table_printed(ctx):
    """线段数增长表：1 / 4 / 16 / 64 / 256 / 1024 都要出现。"""
    out = ctx["stdout"]
    return all(str(4 ** d) in out for d in range(6))


def total_printed(ctx):
    return "一共画了" in ctx["stdout"] or "总共" in ctx["stdout"]


CHECKS = [
    {"id": "defined", "desc": "四个函数都定义了",
     "type": "custom", "fn": "all_defined",
     "fail": "koch / snowflake / draw_at / count_segments"},
    {"id": "recursive", "desc": "koch 递归调用了自己四次",
     "type": "custom", "fn": "koch_recursive",
     "fail": "一条线要拆成**四段**更短的科赫曲线，所以要调 4 次 `koch(...)`"},
    {"id": "exit", "desc": "koch 有出口条件",
     "type": "custom", "fn": "koch_has_exit",
     "fail": "`if depth == 0: turtle.forward(length); return` —— "
             "没出口会一直递归到 RecursionError"},
    {"id": "divide", "desc": "每层长度除以 3",
     "type": "custom", "fn": "koch_divides",
     "fail": "递归时传 `length / 3` —— 一条线分成三等份"},
    {"id": "angles", "desc": "转角是 60 / 120 / 60",
     "type": "custom", "fn": "angles_cancel",
     "fail": "左转 60、右转 120、左转 60 —— 加起来正好抵消，"
             "雪花才闭合得上"},
    {"id": "snowflake", "desc": "雪花用循环画三条边",
     "type": "custom", "fn": "snowflake_loops",
     "fail": "`for i in range(3): koch(length, depth); turtle.right(120)`"},
    {"id": "count", "desc": "线段数公式对（4 的幂）",
     "type": "custom", "fn": "count_correct",
     "fail": "`return 4 ** depth`。depth=3 是 64，depth=5 是 1024"},
    {"id": "draw-at", "desc": "draw_at 抬笔移动再落笔",
     "type": "custom", "fn": "draw_at_moves",
     "fail": "`penup()` → `goto(x, y)` → `pendown()`，"
             "少了会从上一片拖一条线过来"},
    {"id": "three", "desc": "画了至少三片雪花",
     "type": "custom", "fn": "three_flakes",
     "fail": "调三次 `draw_at`（或者用循环 + 一个参数表）"},
    {"id": "lines", "desc": "线段够多（至少 250 段）",
     "type": "custom", "fn": "enough_lines",
     "fail": "至少要有一片 `depth >= 3`。少了说明递归没展开，检查出口和四次调用"},
    {"id": "bg", "desc": "深色背景",
     "type": "custom", "fn": "has_dark_bg",
     "fail": "`turtle.bgcolor(\"#0B1020\")` —— 深色底才有星空感"},
    {"id": "colors", "desc": "三片雪花颜色不同",
     "type": "custom", "fn": "varied_colors",
     "fail": "每片传不同的 `color`"},
    {"id": "widths", "desc": "线宽有变化",
     "type": "custom", "fn": "varied_widths",
     "fail": "小的那片用细一点的线，层次感更好"},
    {"id": "speed", "desc": "用了 speed(0)",
     "type": "custom", "fn": "uses_speed_zero",
     "fail": "几百段线不用 `turtle.speed(0)` 会画很久"},
    {"id": "table", "desc": "打印了线段数增长表",
     "type": "custom", "fn": "table_printed",
     "fail": "depth 0~5 的线段数：1 / 4 / 16 / 64 / 256 / 1024，都要打印出来"},
    {"id": "total", "desc": "报出了这次一共画了多少段",
     "type": "custom", "fn": "total_printed",
     "fail": "每片是 `3 * count_segments(depth)` 段，加起来报一下"},
]
