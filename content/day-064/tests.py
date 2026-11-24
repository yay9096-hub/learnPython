import ast


def uses_pyplot(ctx):
    src = ctx["code"]
    return "matplotlib" in src and "plt" in src


def _calls(ctx, name):
    n = 0
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == name:
                n += 1
    return n


def uses_figure(ctx):
    return _calls(ctx, "figure") >= 1


def uses_subplot(ctx):
    return _calls(ctx, "subplot") >= 2


def uses_barh(ctx):
    return _calls(ctx, "barh") >= 1


def uses_bar(ctx):
    return _calls(ctx, "bar") >= 1


def uses_text_in_loop(ctx):
    """标数值要在循环里做，不是一个个手写。"""
    for node in ast.walk(ctx["tree"]):
        if not isinstance(node, ast.For):
            continue
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                if sub.func.attr == "text":
                    return True
    return False


def uses_tight_layout(ctx):
    return _calls(ctx, "tight_layout") >= 1


def two_titles(ctx):
    return len(ctx["plot"].get("titles", [])) >= 2


def has_axis_labels(ctx):
    p = ctx["plot"]
    return len(p.get("xlabels", [])) + len(p.get("ylabels", [])) >= 2


def two_axes(ctx):
    return ctx["plot"].get("axes", 0) >= 2


def enough_bars(ctx):
    """两张图各 5 根柱子。"""
    return ctx["plot"].get("bars", 0) >= 10


def labels_on_bars(ctx):
    """柱子上标了数值 —— 图里应该有 5 个文字。"""
    texts = ctx["plot"].get("texts", [])
    values = {"88", "95", "72", "110", "90"}
    return len(values & set(str(t).strip() for t in texts)) >= 4


def two_colors(ctx):
    """两张图配色要区分开 —— 代码里至少两个颜色值。"""
    src = ctx["code"]
    import re
    colors = set(re.findall(r"color\s*=\s*[\"']([^\"']+)[\"']", src))
    return len(colors) >= 2


def summary_printed(ctx):
    out = ctx["stdout"]
    return "1540" in out and "91" in out


def strongest_printed(ctx):
    return "水城凛" in ctx["stdout"]


CHECKS = [
    {"id": "import", "desc": "导入了 matplotlib",
     "type": "custom", "fn": "uses_pyplot",
     "fail": "`import matplotlib.pyplot as plt` —— 固定写法"},
    {"id": "figure", "desc": "设置了图的尺寸",
     "type": "custom", "fn": "uses_figure",
     "fail": "`plt.figure(figsize=(9, 4))`，要写在画图之前"},
    {"id": "subplot", "desc": "分成了两格",
     "type": "custom", "fn": "uses_subplot",
     "fail": "`plt.subplot(1, 2, 1)` 和 `plt.subplot(1, 2, 2)`"},
    {"id": "axes", "desc": "图里真的有两个子图",
     "type": "custom", "fn": "two_axes",
     "fail": "两个 `subplot` 之后各画一张图"},
    {"id": "barh", "desc": "左边用了横向柱状图",
     "type": "custom", "fn": "uses_barh",
     "fail": "名字长，血量那张用 `plt.barh(names, hp)` 横着画"},
    {"id": "bar", "desc": "右边用了竖向柱状图",
     "type": "custom", "fn": "uses_bar",
     "fail": "攻击力那张用 `plt.bar(names, atk)`"},
    {"id": "bars", "desc": "两张图各画了 5 根柱子",
     "type": "custom", "fn": "enough_bars",
     "fail": "五个成员，两张图，一共至少 10 根柱子"},
    {"id": "titles", "desc": "两张图都有标题",
     "type": "custom", "fn": "two_titles",
     "fail": "每个 subplot 后面都要跟一句 `plt.title(...)` —— "
             "**没标题的图等于没画**"},
    {"id": "labels", "desc": "坐标轴有说明",
     "type": "custom", "fn": "has_axis_labels",
     "fail": "横着画的加 `plt.xlabel(...)`，竖着画的加 `plt.ylabel(...)`"},
    {"id": "text-loop", "desc": "用循环在柱子上标数值",
     "type": "custom", "fn": "uses_text_in_loop",
     "fail": "`for i in range(len(names)): plt.text(i, atk[i] + 3, str(atk[i]), ha=\"center\")`"},
    {"id": "text-values", "desc": "数值真的标上去了",
     "type": "custom", "fn": "labels_on_bars",
     "fail": "标的文字要是攻击力的数值（88 / 95 / 72 / 110 / 90）"},
    {"id": "colors", "desc": "两张图配色不同",
     "type": "custom", "fn": "two_colors",
     "fail": "给 `bar` / `barh` 传不同的 `color=\"#...\"`"},
    {"id": "tight", "desc": "用了 tight_layout",
     "type": "custom", "fn": "uses_tight_layout",
     "fail": "多图一定要 `plt.tight_layout()`，不然标题会重叠"},
    {"id": "summary", "desc": "终端里打印了文字摘要",
     "type": "custom", "fn": "summary_printed",
     "fail": "总血量 340+280+310+250+360 = **1540**，"
             "平均攻击 455÷5 = **91.0**"},
    {"id": "strongest", "desc": "报出了最强的成员",
     "type": "custom", "fn": "strongest_printed",
     "fail": "攻击力最高的是**水城凛**（110）。"
             "用 `atk.index(max(atk))` 找到位置再取名字"},
]
