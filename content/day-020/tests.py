# 伤害固定成 37，双方 200 血。正确的战斗过程应该是：
#   回合 1~5 双方互砍（各扣 37×5 = 185）
#   回合 6   A 先出手，B 掉到 -22 倒下 -> break，B 不该再反击
# 所以：回合数 6、A 总伤害 222、B 总伤害 185、A 获胜
#
# 如果漏了 break，B 会在死后反击一次 -> A 也归零 -> 变成「同归于尽」，
# 而且 B 的总伤害会变成 222。这两点都能查出来。
SCRIPT = """
import random
random.randint = lambda a, b: 37
random.randrange = lambda *a, **k: 37
"""


def uses_while(ctx):
    import ast
    return any(isinstance(n, ast.While) for n in ast.walk(ctx["tree"]))


def uses_and(ctx):
    import ast
    return any(isinstance(n.op, ast.And)
               for n in ast.walk(ctx["tree"]) if isinstance(n, ast.BoolOp))


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


def turns_ok(ctx):
    return _has(ctx, 6)


def total_a_ok(ctx):
    return _has(ctx, 222)


def total_b_ok(ctx):
    return _has(ctx, 185)


CASES = [
    {
        "setup": SCRIPT,
        "checks": [
            {
                "id": "while",
                "desc": "用 while 打到一方倒下",
                "type": "custom", "fn": "uses_while",
                "fail": "战斗要用 `while hp_a > 0 and hp_b > 0:`",
            },
            {
                "id": "and",
                "desc": "循环条件用 and 连了两边血量",
                "type": "custom", "fn": "uses_and",
                "fail": "「两个都还活着」就是 `hp_a > 0 and hp_b > 0`",
            },
            {
                "id": "break",
                "desc": "用 break 修掉了「死人反击」",
                "type": "custom", "fn": "uses_break",
                "fail": "A 打完之后要 `if hp_b <= 0: break`，不然 B 死了还能还手",
            },
            {
                "id": "turns",
                "desc": "回合数算对了",
                "type": "custom", "fn": "turns_ok",
                "fail": "固定伤害 37、双方 200 血，正确答案是 **6 个回合**。"
                        "`turn += 1` 要放在循环最开头",
            },
            {
                "id": "total-a",
                "desc": "A 的总伤害算对了",
                "type": "custom", "fn": "total_a_ok",
                "fail": "A 出手 6 次，总伤害应该是 6 × 37 = **222**。"
                        "累加器要在循环外归零、循环内累加",
            },
            {
                "id": "total-b",
                "desc": "B 的总伤害算对了",
                "type": "custom", "fn": "total_b_ok",
                "fail": "B 只出手 5 次（第 6 回合它已经倒下了），"
                        "总伤害应该是 5 × 37 = **185**。是不是漏了 `break`？",
            },
            {
                "id": "log",
                "desc": "每回合都打印了战况",
                "type": "stdout_lines_min", "value": 12,
                "fail": "每次出手都要打印一行：谁打的、多少伤害、对方剩多少血",
            },
            {
                "id": "winner",
                "desc": "宣布了获胜方",
                "type": "stdout_contains", "value": "获胜",
                "fail": "循环结束后要判断谁赢，输出里带上「获胜」两个字",
            },
            {
                "id": "not-draw",
                "desc": "不该判成同归于尽",
                "type": "stdout_not_contains", "value": "同归于尽",
                "fail": "这一局 A 应该干净利落地赢。判成平局说明 B 死后还反击了一次 —— "
                        "检查 `break` 的位置",
            },
        ],
    }
]
