import ast
import os

NEEDED = ["write_diary", "append_diary", "write_lines", "save_role"]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def uses_with(ctx):
    """至少 4 处 with open —— 不许手动 open/close。"""
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.With)) >= 4


def no_manual_close(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "close":
                return False
    return True


def always_utf8(ctx):
    """每个 open() 都要带 encoding。"""
    found = 0
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "open":
            found += 1
            names = {k.arg for k in n.keywords}
            if "encoding" not in names:
                return False
    return found >= 4


def _read(name):
    try:
        with open(name, encoding="utf-8") as f:
            return f.read()
    except OSError:
        return None


def diary_exists(ctx):
    return _read("日记.txt") is not None


def diary_has_all(ctx):
    """三篇日记 + 玩家补记，都要在同一个文件里 —— 证明 a 模式没覆盖。"""
    text = _read("日记.txt")
    if text is None:
        return False
    return all(d in text for d in ["2026-09-02", "2026-09-03", "2026-09-04"])


def diary_kept_user_line(ctx):
    text = _read("日记.txt")
    return text is not None and "今天真开心" in text


def append_mode_used(ctx):
    """代码里真的用了 a 模式。"""
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "open":
            for a in n.args:
                if isinstance(a, ast.Constant) and a.value == "a":
                    return True
    return False


def todo_lines(ctx):
    """待办至少 4 行，而且每行都真的分开了。"""
    text = _read("待办.txt")
    if text is None:
        return False
    lines = [l for l in text.splitlines() if l.strip()]
    return len(lines) >= 4


def card_written(ctx):
    text = _read("角色卡.txt")
    if text is None:
        return False
    return "星野樱" in text and len([l for l in text.splitlines() if l.strip()]) >= 4


def read_back(ctx):
    """主流程把文件读回来打印了。"""
    out = ctx["stdout"]
    return "2026-09-02" in out and "星野樱" in out


def write_no_auto_newline(ctx):
    """write_lines 写出来的必须是多行，不能全挤在一行。"""
    fn = ctx["ns"].get("write_lines")
    if not callable(fn):
        return False
    try:
        fn("__测试换行.txt", ["甲", "乙", "丙"])
    except Exception:
        return False
    text = _read("__测试换行.txt")
    try:
        os.remove("__测试换行.txt")
    except OSError:
        pass
    if text is None:
        return False
    return len([l for l in text.splitlines() if l.strip()]) == 3


CASES = [
    {
        "stdin": ["今天真开心"],
        "checks": [
            {
                "id": "defined",
                "desc": "四个函数都定义了",
                "type": "custom", "fn": "all_defined",
                "fail": "write_diary / append_diary / write_lines / save_role",
            },
            {
                "id": "with",
                "desc": "全部用 with open",
                "type": "custom", "fn": "uses_with",
                "fail": "每个写文件的函数都要用 `with open(...) as f:`，"
                        "这样出错也能保证文件被关上",
            },
            {
                "id": "no-close",
                "desc": "没有手动 close()",
                "type": "custom", "fn": "no_manual_close",
                "fail": "用了 `with` 就不需要 `f.close()` 了 —— 它会自动关",
            },
            {
                "id": "utf8",
                "desc": "每个 open 都带 encoding",
                "type": "custom", "fn": "always_utf8",
                "fail": "中文必须写 `encoding=\"utf-8\"`，"
                        "不然换台电脑打开就是乱码",
            },
            {
                "id": "diary",
                "desc": "日记.txt 写出来了",
                "type": "custom", "fn": "diary_exists",
                "fail": "用 `write_diary(\"日记.txt\", ...)` 写第一篇",
            },
            {
                "id": "append-mode",
                "desc": "用了 a 追加模式",
                "type": "custom", "fn": "append_mode_used",
                "fail": "`append_diary` 里要用 `open(filename, \"a\", ...)`，"
                        "用 `\"w\"` 会把前一篇清空",
            },
            {
                "id": "three-entries",
                "desc": "三篇日记都还在（没被覆盖）",
                "type": "custom", "fn": "diary_has_all",
                "fail": "第一篇用 `\"w\"`，后两篇用 `\"a\"`。三个日期都应该在同一个文件里",
            },
            {
                "id": "user-entry",
                "desc": "玩家写的那句也追加进去了",
                "type": "custom", "fn": "diary_kept_user_line",
                "fail": "把 `input()` 拿到的内容也用 `append_diary` 追加到日记里",
            },
            {
                "id": "todo",
                "desc": "待办.txt 有至少 4 行",
                "type": "custom", "fn": "todo_lines",
                "fail": "`write_lines` 每写一项要加 `\"\n\"` —— "
                        "`write` **不会自动换行**",
            },
            {
                "id": "newline",
                "desc": "write_lines 真的分行了",
                "type": "custom", "fn": "write_no_auto_newline",
                "fail": "传 3 项进去应该写出 3 行。全挤在一行说明漏了 `+ \"\n\"`",
            },
            {
                "id": "card",
                "desc": "角色卡.txt 写出来了",
                "type": "custom", "fn": "card_written",
                "fail": "用 `for key, value in role.items():` 把每个属性写一行",
            },
            {
                "id": "readback",
                "desc": "把文件读回来打印了",
                "type": "custom", "fn": "read_back",
                "fail": "写完之后用 `with open(...) as f: print(f.read())` 读回来，"
                        "亲眼确认真的写进去了",
            },
        ],
    }
]
