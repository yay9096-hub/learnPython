import ast

PURE = ["pick_number", "get_difficulty", "check_guess", "is_valid", "make_hint"]
ALL_FN = PURE + ["show_result", "play"]

# 判题时把答案固定成 42，好写确定的剧本
SETUP = "import random\nrandom.randint = lambda a, b: 42\n"


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in ALL_FN)


def pure_no_print(ctx):
    fns = _funcs(ctx)
    for name in PURE:
        fn = fns.get(name)
        if fn is None:
            return False
        for n in ast.walk(fn):
            if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "print":
                return False
    return True


def difficulty_ok(ctx):
    fn = ctx["ns"].get("get_difficulty")
    if not callable(fn):
        return False
    try:
        easy = tuple(fn("简单"))
        normal = tuple(fn("普通"))
        hard = tuple(fn("困难"))
        other = tuple(fn("乱写的"))
    except Exception:
        return False
    return (easy == (50, 8) and normal == (100, 7)
            and hard == (200, 6) and other == (100, 7))


def check_guess_ok(ctx):
    fn = ctx["ns"].get("check_guess")
    if not callable(fn):
        return False
    return (fn(50, 42) == "太大" and fn(10, 42) == "太小"
            and fn(42, 42) == "猜对了")


def is_valid_ok(ctx):
    fn = ctx["ns"].get("is_valid")
    if not callable(fn):
        return False
    try:
        a = fn("abc", 100)
        b = fn("50", 100)
        c = fn("500", 100)
        d = fn("0", 100)
    except Exception:
        return False
    return (a[0] is False and b[0] is True
            and c[0] is False and d[0] is False
            and isinstance(a[1], str) and len(a[1]) > 0)


def hint_ok(ctx):
    fn = ctx["ns"].get("make_hint")
    if not callable(fn):
        return False
    even = fn(42)
    odd = fn(37)
    return isinstance(even, str) and isinstance(odd, str) and even != odd


def play_returns_bool(ctx):
    fn = _funcs(ctx).get("play")
    if fn is None:
        return False
    return any(isinstance(n, ast.Return) and n.value is not None
               for n in ast.walk(fn))


def play_uses_helpers(ctx):
    """play 要调用别的函数，不能自己重写判断逻辑。"""
    fn = _funcs(ctx).get("play")
    if fn is None:
        return False
    called = {getattr(n.func, "id", None) for n in ast.walk(fn)
              if isinstance(n, ast.Call)}
    return len(called & set(PURE)) >= 3


def has_while(ctx):
    fn = _funcs(ctx).get("play")
    if fn is None:
        return False
    return any(isinstance(n, (ast.While, ast.For)) for n in ast.walk(fn))


def won_flow(ctx):
    return "猜对了" in ctx["stdout"]


def bad_input_free(ctx):
    """非法输入不该扣次数：喂了 abc 之后仍然能用满次数猜中。"""
    return "猜对了" in ctx["stdout"]


def shows_answer_on_lose(ctx):
    return "42" in ctx["stdout"]


def hint_shown(ctx):
    return "偶数" in ctx["stdout"] or "奇数" in ctx["stdout"]


CASES = [
    {
        "setup": SETUP,
        "stdin": ["普通", "abc", "50", "10", "42"],
        "checks": [
            {
                "id": "defined",
                "desc": "七个函数都定义了",
                "type": "custom", "fn": "all_defined",
                "fail": "pick_number / get_difficulty / check_guess / is_valid / "
                        "make_hint / show_result / play，函数名照抄",
            },
            {
                "id": "pure",
                "desc": "五个「算」的函数里没有 print",
                "type": "custom", "fn": "pure_no_print",
                "fail": "pick_number / get_difficulty / check_guess / is_valid / make_hint "
                        "只负责算和 return，**一个 print 都不要写**",
            },
            {
                "id": "difficulty",
                "desc": "三档难度返回值都对",
                "type": "custom", "fn": "difficulty_ok",
                "fail": "简单 (50, 8)、普通 (100, 7)、困难 (200, 6)，"
                        "不认识的难度名按普通算",
            },
            {
                "id": "check",
                "desc": "check_guess 三种结果都对",
                "type": "custom", "fn": "check_guess_ok",
                "fail": "只返回 `\"太大\"` / `\"太小\"` / `\"猜对了\"` 三个字符串之一",
            },
            {
                "id": "valid",
                "desc": "is_valid 能挡住非法输入",
                "type": "custom", "fn": "is_valid_ok",
                "fail": "`\"abc\"` 不合法、`\"500\"`（超范围）不合法、`\"0\"` 不合法、"
                        "`\"50\"` 合法。返回 (布尔, 说明) 两个值",
            },
            {
                "id": "hint",
                "desc": "make_hint 对奇偶给不同提示",
                "type": "custom", "fn": "hint_ok",
                "fail": "用 `answer % 2 == 0` 判断奇偶，两种情况返回不同的字符串",
            },
            {
                "id": "play-return",
                "desc": "play 有返回值",
                "type": "custom", "fn": "play_returns_bool",
                "fail": "`play` 要 `return` 赢没赢，主流程才能根据结果说话",
            },
            {
                "id": "play-reuse",
                "desc": "play 调用了其它函数",
                "type": "custom", "fn": "play_uses_helpers",
                "fail": "`play` 里要调 `pick_number` / `is_valid` / `check_guess` 这些，"
                        "别把逻辑再抄一遍",
            },
            {
                "id": "loop",
                "desc": "play 里有循环",
                "type": "custom", "fn": "has_while",
                "fail": "一局要能猜好几次，用 `while used < chances:`",
            },
            {
                "id": "bad-input",
                "desc": "非法输入不算次数，最后仍能猜中",
                "type": "custom", "fn": "bad_input_free",
                "fail": "喂进去的顺序是 abc → 50 → 10 → 42。"
                        "`abc` 不该扣次数（用 `continue` 跳过），最后应该能猜中 42",
            },
            {
                "id": "won",
                "desc": "猜中时有正确反馈",
                "type": "custom", "fn": "won_flow",
                "fail": "猜中时 `check_guess` 应返回「猜对了」并结束这一局",
            },
        ],
    },
    {
        "setup": SETUP,
        "stdin": ["困难", "1", "2", "3", "4", "5", "6"],
        "checks": [
            {
                "id": "lose",
                "desc": "次数用完会公布答案",
                "type": "custom", "fn": "shows_answer_on_lose",
                "fail": "困难模式 6 次机会全用完还没猜中，要在 `show_result` 里公布答案 42",
            },
            {
                "id": "hint-shown",
                "desc": "快用完次数时给了提示",
                "type": "custom", "fn": "hint_shown",
                "fail": "剩下没几次时调用一次 `make_hint(answer)` 并打印出来",
            },
        ],
    },
]
