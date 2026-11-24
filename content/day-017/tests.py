# 把随机固定成一份剧本，好检查统计对不对。
# 稀有度：R SR R SSR R R SR R SSR R  -> 2 个 SSR
# 战力  ：120 340 210 987 150 660 430 220 770 310 -> 最高 987
# judge 判完会自动还原 random，不影响她自己点「运行」。
SCRIPT = """
import random

_R = ["R", "SR", "R", "SSR", "R", "R", "SR", "R", "SSR", "R"]
_P = [120, 340, 210, 987, 150, 660, 430, 220, 770, 310]
_i = {"r": 0, "p": 0}


def _choice(seq):
    seq = list(seq)
    if "SSR" in seq:                 # 抽稀有度
        v = _R[_i["r"] % len(_R)]
        _i["r"] += 1
        return v
    return seq[0]                    # 抽角色名之类，固定取第一个


def _randint(a, b):
    v = _P[_i["p"] % len(_P)]
    _i["p"] += 1
    return v


random.choice = _choice
random.randint = _randint
random.randrange = lambda *a, **k: _randint(0, 0)
"""


def uses_for(ctx):
    import ast
    return any(isinstance(n, ast.For) for n in ast.walk(ctx["tree"]))


def uses_break_or_continue(ctx):
    import ast
    return any(isinstance(n, (ast.Break, ast.Continue)) for n in ast.walk(ctx["tree"]))


def _has(ctx, want):
    for k, v in ctx["ns"].items():
        if k.startswith("__") or isinstance(v, bool):
            continue
        if isinstance(v, int) and v == want:
            return True
    return False


def ssr_counted(ctx):
    """这份剧本里正好出 2 个 SSR。变量叫什么名字不重要。"""
    return _has(ctx, 2)


def best_found(ctx):
    """最高战力是 987。"""
    return _has(ctx, 987)


def ten_draws(ctx):
    lines = [l for l in ctx["stdout"].splitlines() if l.strip()]
    return len(lines) >= 11


CASES = [
    {
        "setup": SCRIPT,
        "checks": [
            {
                "id": "for",
                "desc": "用 for 循环抽了十次",
                "type": "custom", "fn": "uses_for",
                "fail": "把单抽的代码缩进到 `for i in range(10):` 里面，就是十连了",
            },
            {
                "id": "random",
                "desc": "用了 random 抽卡",
                "type": "ast_imports", "name": "random",
                "fail": "开头要 `import random`",
            },
            {
                "id": "ten",
                "desc": "输出了十抽的结果",
                "type": "custom", "fn": "ten_draws",
                "fail": "十抽 + 总结，输出应该有 11 行以上。`print` 要写在循环**里面**",
            },
            {
                "id": "ssr",
                "desc": "统计对了 SSR 数量",
                "type": "custom", "fn": "ssr_counted",
                "fail": "这一局正好出 2 个 SSR。检查一下：归零的那句 `ssr_count = 0` "
                        "是不是写进循环里了？它应该在循环**外面**",
            },
            {
                "id": "best",
                "desc": "找对了最高战力",
                "type": "custom", "fn": "best_found",
                "fail": "这一局最高战力是 987。套路是：先设 `best = 0`，"
                        "循环里 `if power > best: best = power`",
            },
            {
                "id": "flow",
                "desc": "用到了 break 或 continue",
                "type": "custom", "fn": "uses_break_or_continue",
                "fail": "至少用一次 `break` 或 `continue`，比如抽到 SSR 时特别提示",
            },
            {
                "id": "summary",
                "desc": "最后有总结",
                "type": "stdout_contains", "value": "十连结束",
                "fail": "循环**外面**（顶格）打印一句带「十连结束」的总结",
            },
            {
                "id": "show-stats",
                "desc": "总结里报出了统计结果",
                "type": "stdout_contains", "value": ["2", "987"],
                "fail": "把 SSR 个数和最高战力都用 f-string 打印出来",
            },
        ],
    }
]
