BOX_CHARS = "═║╔╗╚╝─│┌┐└┘+-|"


def has_box(ctx):
    """至少有两行看起来像方框的边（连续的边框字符）。"""
    hits = 0
    for line in ctx["stdout"].splitlines():
        s = line.strip()
        if len(s) >= 6 and sum(1 for ch in s if ch in BOX_CHARS) >= 6:
            hits += 1
    return hits >= 2


def has_quote_mark(ctx):
    out = ctx["stdout"]
    return any(q in out for q in ["\"", "“", "”", "「", "」", "'"])


def uses_triple(ctx):
    code = ctx["code"]
    return "\"\"\"" in code or "'''" in code


def uses_newline_escape(ctx):
    return "\n" in ctx["code"]


def enough_lines(ctx):
    return len([l for l in ctx["stdout"].splitlines() if l.strip()]) >= 8


CHECKS = [
    {
        "id": "triple",
        "desc": "用三引号写了对话框",
        "type": "custom", "fn": "uses_triple",
        "fail": "用三个引号 `\"\"\"` 把整个方框包起来，里面怎么排版就怎么显示",
    },
    {
        "id": "box",
        "desc": "对话框有上下边框",
        "type": "custom", "fn": "has_box",
        "fail": "至少要有两行边框线，比如 `╔══════╗` 和 `╚══════╝`",
    },
    {
        "id": "quote",
        "desc": "台词带引号",
        "type": "custom", "fn": "has_quote_mark",
        "fail": "给台词加上引号，看起来才像在说话～",
    },
    {
        "id": "escape-n",
        "desc": "用了 \n 打印旁白",
        "type": "custom", "fn": "uses_newline_escape",
        "fail": "旁白那一句要用 `\n` 换行，而不是再写一个 print",
    },
    {
        "id": "sep",
        "desc": "用 sep 打印了状态栏",
        "type": "stdout_regex", "pattern": "HP.*\|.*MP|HP.*-.*MP|\|.*Lv",
        "fail": "状态栏要用 `print(\"HP: 340\", \"MP: 180\", sep=\" | \")` 这种写法",
    },
    {
        "id": "end",
        "desc": "用 end 拼出了一整行",
        "type": "stdout_regex", "pattern": "[=#▓█\-]{10,}",
        "fail": "进度条要用 `print(..., end=\"\")` 让几个 print 挤在同一行",
    },
    {
        "id": "lines",
        "desc": "整体输出够丰富（至少 8 行）",
        "type": "custom", "fn": "enough_lines",
        "fail": "对话框 + 旁白 + 状态栏 + 进度条，加起来应该不止这么点内容～",
    },
]
