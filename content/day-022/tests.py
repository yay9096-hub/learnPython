# 答案固定成 42。剧本：
#   难度选 2（1~100，7 次机会）
#   第 1 局：50(太大) -> 40(太小) -> 42(猜中)   共 3 次，赢
#   回答 y 继续
#   第 2 局：连猜 7 个错的 -> 次数用完，输
#   回答 n 结束
# 所以：总局数 2、胜利 1、最佳成绩 3
SCRIPT = """
import random
random.randint = lambda a, b: 42
random.randrange = lambda *a, **k: 42
"""


def two_whiles(ctx):
    import ast
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.While)) >= 2


def nested_while(ctx):
    """外层管局数，内层管猜测 —— 必须是嵌套的。"""
    import ast
    for outer in ast.walk(ctx["tree"]):
        if isinstance(outer, ast.While):
            for child in ast.walk(outer):
                if isinstance(child, ast.While) and child is not outer:
                    return True
    return False


def uses_break(ctx):
    import ast
    return any(isinstance(n, ast.Break) for n in ast.walk(ctx["tree"]))


def _has(ctx, want):
    for k, v in ctx["ns"].items():
        if k.startswith("__") or isinstance(v, bool):
            continue
        if isinstance(v, int) and v == want:
            return True
    return False


def games_ok(ctx):
    return _has(ctx, 2)


def best_ok(ctx):
    return _has(ctx, 3)


CASES = [
    {
        "setup": SCRIPT,
        "stdin": ["2",
                  "50", "40", "42",
                  "y",
                  "1", "2", "3", "4", "5", "6", "7",
                  "n", "n", "n"],
        "checks": [
            {
                "id": "whiles",
                "desc": "用了两层 while（多局 + 多次猜测）",
                "type": "custom", "fn": "two_whiles",
                "fail": "外层 `while True` 管一局一局，内层 while 管一局里的多次猜测",
            },
            {
                "id": "nested",
                "desc": "两层循环是嵌套的",
                "type": "custom", "fn": "nested_while",
                "fail": "猜测循环要写在游戏循环**里面**（缩进 4 格）",
            },
            {
                "id": "break",
                "desc": "用 break 退出游戏循环",
                "type": "custom", "fn": "uses_break",
                "fail": "玩家回答不是 y 的时候，用 `break` 跳出外层循环",
            },
            {
                "id": "hints",
                "desc": "猜大猜小都有提示",
                "type": "stdout_contains", "value": ["太大", "太小"],
                "fail": "猜 50 该说太大、猜 40 该说太小",
            },
            {
                "id": "win",
                "desc": "第一局猜对了",
                "type": "stdout_contains", "value": "猜对",
                "fail": "第三次猜的 42 正是答案，应该判赢",
            },
            {
                "id": "lose",
                "desc": "第二局次数用完判输",
                "type": "stdout_contains", "value": "用完",
                "fail": "普通难度只有 7 次机会，用完还没猜中就该结束这一局。"
                        "循环条件要写成 `guess != answer and tries < chances`",
            },
            {
                "id": "games",
                "desc": "总局数统计正确",
                "type": "custom", "fn": "games_ok",
                "fail": "一共玩了 **2 局**。`games += 1` 要放在外层循环开头",
            },
            {
                "id": "best",
                "desc": "最佳成绩记录正确",
                "type": "custom", "fn": "best_ok",
                "fail": "赢的那局用了 **3 次**。套路：先设 `best = 999`，"
                        "赢了之后 `if tries < best: best = tries`",
            },
            {
                "id": "report",
                "desc": "最后打印了战报",
                "type": "stdout_contains", "value": "战报",
                "fail": "退出游戏循环后，打印一段带「战报」两个字的统计",
            },
        ],
    },
    {
        "setup": SCRIPT,
        "stdin": ["9", "abc", "1",
                  "42",
                  "n", "n"],
        "checks": [
            {
                "id": "validate",
                "desc": "难度输错了会重问",
                "type": "stdout_contains", "value": "猜对",
                "fail": "玩家先输了 `9` 和 `abc`，要用 `while` 重问，"
                        "而不是崩掉或直接当成某个难度",
            },
        ],
    },
]
