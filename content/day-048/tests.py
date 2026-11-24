import ast

NEEDED = ["read_all", "read_lines", "count_lines", "count_chars",
          "find_by_date", "search", "show_numbered"]

# ENTRIES 五行的总字数（strip 之后）
EXPECT_CHARS = sum(len(s) for s in [
    "2026-09-02 今天学会了写文件，程序终于能记住东西了",
    "2026-09-03 写文件比想象中简单，就是别忘了 encoding",
    "2026-09-04 刷新页面文件还在，有点感动",
    "2026-09-05 读文件也学会了，w 和 a 别搞混",
    "2026-09-06 明天要做错题本，感觉能派上大用场",
])


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def uses_with(ctx):
    return any(isinstance(n, ast.With) for n in ast.walk(ctx["tree"]))


def utf8_everywhere(ctx):
    found = 0
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "open":
            found += 1
            if "encoding" not in {k.arg for k in n.keywords}:
                return False
    return found >= 2


def read_all_ok(ctx):
    fn = ctx["ns"].get("read_all")
    if not callable(fn):
        return False
    t = fn("我的日记.txt")
    return isinstance(t, str) and "2026-09-02" in t and "2026-09-06" in t


def read_lines_ok(ctx):
    fn = ctx["ns"].get("read_lines")
    if not callable(fn):
        return False
    lines = fn("我的日记.txt")
    if not isinstance(lines, list) or len(lines) != 5:
        return False
    # 每一行都必须已经 strip 过
    return all(l == l.strip() and l for l in lines)


def count_lines_ok(ctx):
    fn = ctx["ns"].get("count_lines")
    return callable(fn) and fn("我的日记.txt") == 5


def count_chars_ok(ctx):
    fn = ctx["ns"].get("count_chars")
    if not callable(fn):
        return False
    return fn("我的日记.txt") == EXPECT_CHARS


def find_ok(ctx):
    fn = ctx["ns"].get("find_by_date")
    if not callable(fn):
        return False
    hit = fn("我的日记.txt", "2026-09-04")
    miss = fn("我的日记.txt", "2020-01-01")
    return isinstance(hit, str) and "感动" in hit and miss is None


def search_ok(ctx):
    fn = ctx["ns"].get("search")
    if not callable(fn):
        return False
    hits = fn("我的日记.txt", "文件")
    none = fn("我的日记.txt", "不存在的词xyz")
    return isinstance(hits, list) and len(hits) >= 3 and none == []


def numbered_output(ctx):
    """带行号打印过：输出里有 1. 到 5."""
    import re
    out = ctx["stdout"]
    return all(re.search(r"%d\.\s" % i, out) for i in [1, 2, 3, 4, 5])


def stats_shown(ctx):
    out = ctx["stdout"]
    return "5" in out and str(EXPECT_CHARS) in out


def found_and_missing(ctx):
    out = ctx["stdout"]
    return "感动" in out and ("没写" in out or "没有" in out)


def search_hit(ctx):
    return "找到" in ctx["stdout"]


CASES = [
    {
        "stdin": ["文件"],
        "checks": [
            {
                "id": "defined",
                "desc": "七个函数都定义了",
                "type": "custom", "fn": "all_defined",
                "fail": "read_all / read_lines / count_lines / count_chars / "
                        "find_by_date / search / show_numbered",
            },
            {
                "id": "with",
                "desc": "用 with open 读文件",
                "type": "custom", "fn": "uses_with",
                "fail": "读文件也要用 `with open(...) as f:`",
            },
            {
                "id": "utf8",
                "desc": "读写都带 encoding",
                "type": "custom", "fn": "utf8_everywhere",
                "fail": "读的时候也要写 `encoding=\"utf-8\"`，不然中文会乱码",
            },
            {
                "id": "read-all",
                "desc": "read_all 返回整个字符串",
                "type": "custom", "fn": "read_all_ok",
                "fail": "`return f.read()` —— 整个文件读成一个字符串",
            },
            {
                "id": "read-lines",
                "desc": "read_lines 已 strip 且无空行",
                "type": "custom", "fn": "read_lines_ok",
                "fail": "每行要 `.strip()` 掉换行符，空行不要放进列表。"
                        "五篇日记应该得到 5 项",
            },
            {
                "id": "count-lines",
                "desc": "count_lines 数对了（5 篇）",
                "type": "custom", "fn": "count_lines_ok",
                "fail": "直接 `return len(read_lines(filename))` —— 复用已有的函数",
            },
            {
                "id": "count-chars",
                "desc": "count_chars 没把换行符算进去",
                "type": "custom", "fn": "count_chars_ok",
                "fail": "统计前每行要先 `.strip()`，否则每行会多算一个换行符",
            },
            {
                "id": "find",
                "desc": "find_by_date 找到 / 找不到都正确",
                "type": "custom", "fn": "find_ok",
                "fail": "用 `line.startswith(date)` 判断，找到就立刻 return，"
                        "循环跑完还没有就 `return None`",
            },
            {
                "id": "search",
                "desc": "search 返回全部匹配的行",
                "type": "custom", "fn": "search_ok",
                "fail": "用 `if keyword in line:` 筛选，一条都没有时返回空列表 `[]`",
            },
            {
                "id": "numbered",
                "desc": "带行号列出了 5 篇",
                "type": "custom", "fn": "numbered_output",
                "fail": "用 `enumerate(lines, start=1)` 生成行号",
            },
            {
                "id": "stats",
                "desc": "打印了篇数和字数",
                "type": "custom", "fn": "stats_shown",
                "fail": "主流程要打印总篇数（5）和总字数",
            },
            {
                "id": "find-both",
                "desc": "查了存在和不存在的两个日期",
                "type": "custom", "fn": "found_and_missing",
                "fail": "查 `2026-09-04`（有）和一个没写过的日期（没有），两种都要有反馈",
            },
            {
                "id": "search-out",
                "desc": "搜索结果打印出来了",
                "type": "custom", "fn": "search_hit",
                "fail": "搜「文件」应该能找到好几条，把它们列出来",
            },
        ],
    },
    {
        "stdin": ["完全不存在的词"],
        "checks": [
            {
                "id": "no-hit",
                "desc": "搜不到时有提示",
                "type": "stdout_contains", "value": "没有找到",
                "fail": "`search` 返回空列表时，要提示「没有找到」而不是什么都不显示",
            },
        ],
    },
]
