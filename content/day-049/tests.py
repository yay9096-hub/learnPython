import ast
import os

NEEDED = ["load_notes", "add_note", "count_notes",
          "search_notes", "show_notes", "clear_notes"]

# 判题前先把错题本删掉，模拟「第一次运行」
SETUP = """
import os
for _n in ["错题本.txt"]:
    if os.path.exists(_n):
        os.remove(_n)
"""


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def handles_missing(ctx):
    """load_notes 对不存在的文件必须返回空列表。"""
    fn = ctx["ns"].get("load_notes")
    if not callable(fn):
        return False
    try:
        r = fn("肯定不存在的文件_xyz.txt")
    except Exception:
        return False
    return r == []


def guards_missing_file(ctx):
    """代码里要么 try FileNotFoundError，要么用 os.path.exists。"""
    src = ctx["code"]
    if "FileNotFoundError" in src:
        return True
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "exists":
                return True
    return False


def survived_first_run(ctx):
    """整个程序跑完没崩 —— 第一次运行时文件是不存在的。"""
    return ctx["error"] is None


def empty_hint_shown(ctx):
    """第一次 show_notes 要给「空」的提示。"""
    return "空" in ctx["stdout"]


def append_mode(ctx):
    fn = _funcs(ctx).get("add_note")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "open":
            for a in n.args:
                if isinstance(a, ast.Constant) and a.value == "a":
                    return True
    return False


def add_and_count(ctx):
    """直接调她的函数：加两条，数出来要是 2。"""
    add = ctx["ns"].get("add_note")
    cnt = ctx["ns"].get("count_notes")
    if not callable(add) or not callable(cnt):
        return False
    name = "__判题临时.txt"
    if os.path.exists(name):
        os.remove(name)
    try:
        add(name, "题目一", "答案一")
        add(name, "题目二", "答案二")
        ok = cnt(name) == 2
    except Exception:
        ok = False
    finally:
        if os.path.exists(name):
            os.remove(name)
    return ok


def search_works(ctx):
    fn = ctx["ns"].get("search_notes")
    add = ctx["ns"].get("add_note")
    if not callable(fn) or not callable(add):
        return False
    name = "__判题搜索.txt"
    if os.path.exists(name):
        os.remove(name)
    try:
        add(name, "列表编号从几开始", "从 0")
        add(name, "字典怎么取值", "用键名")
        hits = fn(name, "列表")
        none = fn(name, "完全不存在xyz")
        ok = isinstance(hits, list) and len(hits) == 1 and none == []
    except Exception:
        ok = False
    finally:
        if os.path.exists(name):
            os.remove(name)
    return ok


def clear_works(ctx):
    add = ctx["ns"].get("add_note")
    clear = ctx["ns"].get("clear_notes")
    cnt = ctx["ns"].get("count_notes")
    if not all(callable(x) for x in [add, clear, cnt]):
        return False
    name = "__判题清空.txt"
    try:
        add(name, "题", "答")
        clear(name)
        ok = cnt(name) == 0 and os.path.exists(name)
    except Exception:
        ok = False
    finally:
        if os.path.exists(name):
            os.remove(name)
    return ok


def three_added(ctx):
    """输出里能看到三条初始错题。"""
    out = ctx["stdout"]
    return "str()" in out and "0" in out and "sort" in out


def numbered(ctx):
    import re
    return re.search(r"1\.\s*❓|1\.\s", ctx["stdout"]) is not None


def user_note_added(ctx):
    return "我今天错的题" in ctx["stdout"] or "已记下" in ctx["stdout"]


def cleared_at_end(ctx):
    """最后清空之后条数应该是 0。"""
    out = ctx["stdout"]
    return "剩 0 条" in out or "0 条" in out


CASES = [
    {
        "setup": SETUP,
        "stdin": ["我今天错的题", "正确答案", "列表"],
        "checks": [
            {
                "id": "defined",
                "desc": "六个函数都定义了",
                "type": "custom", "fn": "all_defined",
                "fail": "load_notes / add_note / count_notes / search_notes / "
                        "show_notes / clear_notes",
            },
            {
                "id": "guard",
                "desc": "处理了「文件还不存在」",
                "type": "custom", "fn": "guards_missing_file",
                "fail": "用 `except FileNotFoundError:` 或者 `os.path.exists()` "
                        "来应对文件还没创建的情况",
            },
            {
                "id": "missing",
                "desc": "读不存在的文件返回空列表",
                "type": "custom", "fn": "handles_missing",
                "fail": "`load_notes` 遇到不存在的文件要返回 `[]`，"
                        "**不是 None，也不能抛异常**",
            },
            {
                "id": "survive",
                "desc": "第一次运行不崩",
                "type": "custom", "fn": "survived_first_run",
                "fail": "程序开头就调用 `show_notes`，此时文件还不存在 —— 必须撑住",
            },
            {
                "id": "empty-hint",
                "desc": "空错题本有友好提示",
                "type": "custom", "fn": "empty_hint_shown",
                "fail": "一条都没有时要说一句「错题本还是空的」，不能什么都不显示",
            },
            {
                "id": "append",
                "desc": "add_note 用了 a 模式",
                "type": "custom", "fn": "append_mode",
                "fail": "追加要用 `open(filename, \"a\", ...)`，用 `\"w\"` 会把之前的全清掉",
            },
            {
                "id": "add-count",
                "desc": "加两条能数出 2 条",
                "type": "custom", "fn": "add_and_count",
                "fail": "每条写成一行（末尾带 `\n`），`count_notes` 才数得对",
            },
            {
                "id": "search",
                "desc": "搜索正确，搜不到返回空列表",
                "type": "custom", "fn": "search_works",
                "fail": "用 `if keyword in line:` 筛，一条都没有时返回 `[]`",
            },
            {
                "id": "clear",
                "desc": "清空后条数为 0 且文件还在",
                "type": "custom", "fn": "clear_works",
                "fail": "用 `\"w\"` 模式写入空字符串 —— 内容没了但文件保留",
            },
            {
                "id": "three",
                "desc": "记了三条初始错题",
                "type": "custom", "fn": "three_added",
                "fail": "用 `add_note` 加三条不同的错题",
            },
            {
                "id": "numbered",
                "desc": "显示时带编号",
                "type": "custom", "fn": "numbered",
                "fail": "用 `enumerate(notes, start=1)` 加编号",
            },
            {
                "id": "user",
                "desc": "玩家输入的错题也记下了",
                "type": "custom", "fn": "user_note_added",
                "fail": "问玩家题目和答案，用 `add_note` 加进去",
            },
            {
                "id": "cleared",
                "desc": "最后清空并验证了",
                "type": "custom", "fn": "cleared_at_end",
                "fail": "最后 `clear_notes` 再 `show_notes`，条数应该回到 0",
            },
        ],
    }
]
