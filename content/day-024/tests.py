def uses_append_in_loop(ctx):
    """append 写在 for 循环里，不是一件件手写。"""
    import ast
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.For):
            for child in ast.walk(node):
                if (isinstance(child, ast.Call)
                        and isinstance(child.func, ast.Attribute)
                        and child.func.attr == "append"):
                    return True
    return False


def uses_in_check(ctx):
    """扔之前先检查 —— 代码里要有 in 判断。"""
    import ast
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Compare):
            for op in n.ops:
                if isinstance(op, (ast.In, ast.NotIn)):
                    return True
    return False


def bag_is_list(ctx):
    return isinstance(ctx["ns"].get("bag"), list)


def final_count(ctx):
    """捡 4 + 玩家捡 1 = 5，扔掉 1 剩 4，再 pop 掏走 1 -> 最终 3 件。"""
    bag = ctx["ns"].get("bag")
    return isinstance(bag, list) and len(bag) == 3


CASES = [
    {
        "stdin": ["屠龙刀", "面包"],
        "checks": [
            {
                "id": "bag",
                "desc": "背包是一个列表",
                "type": "custom", "fn": "bag_is_list",
                "fail": "背包要从 `bag = []` 开始",
            },
            {
                "id": "loop-append",
                "desc": "用循环批量捡装备",
                "type": "custom", "fn": "uses_append_in_loop",
                "fail": "把 `bag.append(item)` 写在 `for item in loot:` 里面，别一件件手写",
            },
            {
                "id": "picked",
                "desc": "四件初始装备都捡到了",
                "type": "stdout_contains", "value": ["铁剑", "护符", "红药水", "面包"],
                "fail": "loot 里的四件都要 append 进去，并各打印一句",
            },
            {
                "id": "user-pick",
                "desc": "玩家捡的东西进背包了",
                "type": "stdout_contains", "value": "屠龙刀",
                "fail": "把 `input()` 拿到的东西也 `append` 进背包",
            },
            {
                "id": "in-check",
                "desc": "扔之前先用 in 检查",
                "type": "custom", "fn": "uses_in_check",
                "fail": "用 `if drop in bag:` 先确认有没有，直接 remove 不存在的会报错",
            },
            {
                "id": "removed",
                "desc": "扔掉了背包里有的东西",
                "type": "stdout_contains", "value": "扔掉",
                "fail": "「面包」在背包里，应该能扔掉并提示一句",
            },
            {
                "id": "pop",
                "desc": "用 pop() 掏出了最后一件",
                "type": "stdout_contains", "value": "掏出",
                "fail": "用 `last = bag.pop()` 掏出最后一件，并打印「掏出了 xxx」",
            },
            {
                "id": "final",
                "desc": "最终背包剩 3 件",
                "type": "custom", "fn": "final_count",
                "fail": "数一数：捡 4 件 + 玩家捡 1 件 = 5，扔掉 1 件剩 4，"
                        "再 pop 掏走 1 件 —— 最终应该剩 **3 件**",
            },
        ],
    },
    {
        "stdin": ["盾牌", "不存在的东西"],
        "checks": [
            {
                "id": "not-found",
                "desc": "扔不存在的东西不会崩",
                "type": "stdout_contains", "value": "没有",
                "fail": "背包里没有这件东西时，要走 `else` 提示「背包里没有」，"
                        "而不是直接 remove 导致报错",
            },
        ],
    },
]
