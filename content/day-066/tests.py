import ast

NEEDED = ["find_dates", "find_numbers", "find_emails", "find_urls",
          "find_day_minutes", "mask_phones", "count_chinese"]

SAMPLE = (
    "2026-09-01 Day 1 用了 42 分钟，联系 sakura@example.com\n"
    "2026-09-03 Day 3 用了 58 分钟，问了老师 13812345678\n"
    "2026-09-04 Day 11 用了 40 分钟，笔记在 http://note.example.cn/py\n"
    "2026-09-05 Day 12 用了 45 分钟，同学 ruri@test.org 也在学\n"
    "参考 https://docs.python.org/zh-cn/3/\n"
)


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def uses_re(ctx):
    return "import re" in ctx["code"]


def uses_raw_strings(ctx):
    """正则模式要用 r"..." 原样字符串。"""
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            if "\\d" in n.value or "\\w" in n.value:
                return True
    return False


def dates_ok(ctx):
    fn = ctx["ns"].get("find_dates")
    if not callable(fn):
        return False
    got = fn(SAMPLE)
    return got == ["2026-09-01", "2026-09-03", "2026-09-04", "2026-09-05"]


def numbers_are_ints(ctx):
    fn = ctx["ns"].get("find_numbers")
    if not callable(fn):
        return False
    got = fn("有 42 个和 7 个")
    return got == [42, 7] and all(isinstance(x, int) for x in got)


def emails_ok(ctx):
    fn = ctx["ns"].get("find_emails")
    if not callable(fn):
        return False
    got = set(fn(SAMPLE))
    return "sakura@example.com" in got and "ruri@test.org" in got and len(got) == 2


def urls_ok(ctx):
    """http 和 https 都要抓到。"""
    fn = ctx["ns"].get("find_urls")
    if not callable(fn):
        return False
    got = fn(SAMPLE)
    joined = " ".join(got)
    return (len(got) == 2 and "http://note.example.cn" in joined
            and "https://docs.python.org" in joined)


def day_minutes_ok(ctx):
    fn = ctx["ns"].get("find_day_minutes")
    if not callable(fn):
        return False
    got = fn(SAMPLE)
    want = [(1, 42), (3, 58), (11, 40), (12, 45)]
    if got != want:
        return False
    return all(isinstance(a, int) and isinstance(b, int) for a, b in got)


def mask_ok(ctx):
    fn = ctx["ns"].get("mask_phones")
    if not callable(fn):
        return False
    got = fn("电话 13812345678 结束")
    return "138****5678" in got and "1234" not in got


def mask_keeps_rest(ctx):
    """打码不能把别的数字也吃了。"""
    fn = ctx["ns"].get("mask_phones")
    if not callable(fn):
        return False
    got = fn("2026-09-01 用了 42 分钟")
    return "2026-09-01" in got and "42" in got


def chinese_ok(ctx):
    fn = ctx["ns"].get("count_chinese")
    if not callable(fn):
        return False
    return fn("你好 abc 世界123") == 4 and fn("abc123") == 0


def uses_sub(ctx):
    return "re.sub" in ctx["code"]


def uses_search(ctx):
    return "re.search" in ctx["code"]


def search_guarded(ctx):
    """re.search 可能返回 None，用之前要判断。"""
    src = ctx["code"].replace(" ", "")
    return "iffirst" in src or "ifm" in src or "isnotNone" in src or "if not" in ctx["code"]


def total_printed(ctx):
    """42+35+58+40+45 = 220。"""
    return "220" in ctx["stdout"]


def avg_printed(ctx):
    """220 / 5 = 44.0"""
    return "44" in ctx["stdout"]


def masked_printed(ctx):
    out = ctx["stdout"]
    return "138****5678" in out


def all_shown(ctx):
    out = ctx["stdout"]
    return ("sakura@example.com" in out and "2026-09-01" in out
            and "docs.python.org" in out)


def survived(ctx):
    return ctx["error"] is None


CHECKS = [
    {"id": "defined", "desc": "七个函数都定义了",
     "type": "custom", "fn": "all_defined",
     "fail": "find_dates / find_numbers / find_emails / find_urls / "
             "find_day_minutes / mask_phones / count_chinese"},
    {"id": "import", "desc": "导入了 re",
     "type": "custom", "fn": "uses_re",
     "fail": "`import re`"},
    {"id": "raw", "desc": "正则用了 r\"...\" 原样字符串",
     "type": "custom", "fn": "uses_raw_strings",
     "fail": "模式前面加 `r`，比如 `r\"\\d+\"` —— 不加的话反斜杠要写两遍"},
    {"id": "dates", "desc": "日期抓得准",
     "type": "custom", "fn": "dates_ok",
     "fail": "`r\"\\d{4}-\\d{2}-\\d{2}\"` —— 4 个数字、横杠、2 个、横杠、2 个"},
    {"id": "numbers", "desc": "数字转成了 int",
     "type": "custom", "fn": "numbers_are_ints",
     "fail": "⚠️ `re.findall` 返回的是**文字**，要自己 `int()` 转一遍"},
    {"id": "emails", "desc": "邮箱抓得准（正好 2 个）",
     "type": "custom", "fn": "emails_ok",
     "fail": "`r\"[\\w.]+@[\\w.]+\\w\"` —— 结尾加 `\\w` 免得把句号也吃进去"},
    {"id": "urls", "desc": "http 和 https 都能抓",
     "type": "custom", "fn": "urls_ok",
     "fail": "`r\"https?://[\\w./\\-]+\"` —— `s?` 表示那个 s 可有可无"},
    {"id": "pairs", "desc": "Day 和分钟成对抓出来且是数字",
     "type": "custom", "fn": "day_minutes_ok",
     "fail": "用两个括号分组：`r\"Day (\\d+) 用了 (\\d+) 分钟\"`，"
             "再把两个都 `int()` 转掉"},
    {"id": "sub", "desc": "用了 re.sub",
     "type": "custom", "fn": "uses_sub",
     "fail": "打码要用 `re.sub(模式, 替换, 文本)`"},
    {"id": "mask", "desc": "手机号中间四位打码了",
     "type": "custom", "fn": "mask_ok",
     "fail": "`re.sub(r\"(\\d{3})\\d{4}(\\d{4})\", r\"\\1****\\2\", text)` —— "
             "`\\1` `\\2` 指第 1、第 2 个括号里的内容"},
    {"id": "mask-safe", "desc": "打码没误伤日期和时长",
     "type": "custom", "fn": "mask_keeps_rest",
     "fail": "模式要正好匹配 11 位手机号，别把 `2026-09-01` 里的数字也换了"},
    {"id": "chinese", "desc": "中文字数数对了",
     "type": "custom", "fn": "chinese_ok",
     "fail": "`r\"[\\u4e00-\\u9fa5]\"` 是汉字的 Unicode 范围，"
             "用 `len(re.findall(...))` 数"},
    {"id": "search", "desc": "用了 re.search 找第一个",
     "type": "custom", "fn": "uses_search",
     "fail": "`re.search(r\"\\d{4}-\\d{2}-\\d{2}\", LOG)`"},
    {"id": "search-guard", "desc": "search 的结果判断了 None",
     "type": "custom", "fn": "search_guarded",
     "fail": "⚠️ `re.search` 找不到时返回 `None`，"
             "直接 `.group()` 会崩 —— 用之前先 `if`"},
    {"id": "total", "desc": "总时长算对（220 分钟）",
     "type": "custom", "fn": "total_printed",
     "fail": "42+35+58+40+45 = **220**"},
    {"id": "avg", "desc": "平均时长算对（44.0）",
     "type": "custom", "fn": "avg_printed",
     "fail": "220 ÷ 5 = **44.0**"},
    {"id": "masked-out", "desc": "打印了打码后的文本",
     "type": "custom", "fn": "masked_printed",
     "fail": "输出里应该能看到 `138****5678`"},
    {"id": "shown", "desc": "各项提取结果都打印了",
     "type": "custom", "fn": "all_shown",
     "fail": "日期、邮箱、网址的结果都要打印出来"},
    {"id": "survive", "desc": "全程没有崩溃",
     "type": "custom", "fn": "survived",
     "fail": "注意算平均值时防除零"},
]
