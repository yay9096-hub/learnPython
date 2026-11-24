import ast

NEEDED = ["roll", "deal_damage", "is_alive", "grade", "battle_report"]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_return(ctx):
    """五个函数每个都要有 return，而且都不许 print。"""
    fns = _funcs(ctx)
    for name in NEEDED:
        fn = fns.get(name)
        if fn is None:
            return False
        has_return = any(isinstance(n, ast.Return) and n.value is not None
                         for n in ast.walk(fn))
        if not has_return:
            return False
    return True


def no_print_inside(ctx):
    fns = _funcs(ctx)
    for name in NEEDED:
        fn = fns.get(name)
        if fn is None:
            return False
        for n in ast.walk(fn):
            if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "print":
                return False
    return True


def roll_ok(ctx):
    fn = ctx["ns"].get("roll")
    if not callable(fn):
        return False
    seen = set()
    for _ in range(60):
        v = fn(6)
        if not isinstance(v, int) or not 1 <= v <= 6:
            return False
        seen.add(v)
    return len(seen) >= 3


def damage_ok(ctx):
    fn = ctx["ns"].get("deal_damage")
    if not callable(fn):
        return False
    return fn(88, 25) == 63 and fn(10, 99) == 1 and fn(100, 100) == 1


def alive_ok(ctx):
    fn = ctx["ns"].get("is_alive")
    if not callable(fn):
        return False
    return fn(100) is True and fn(0) is False and fn(-5) is False


def grade_ok(ctx):
    fn = ctx["ns"].get("grade")
    if not callable(fn):
        return False
    return (fn(95) == "优秀" and fn(90) == "优秀"
            and fn(72) == "及格" and fn(60) == "及格"
            and fn(30) == "再努力一下")


def report_returns_str(ctx):
    fn = ctx["ns"].get("battle_report")
    if not callable(fn):
        return False
    r = fn("测试者", 123)
    return isinstance(r, str) and "测试者" in r and "123" in r


def dice_summed(ctx):
    """主流程里把三次点数加起来了。"""
    import re
    return re.search(r"\d+\s*\+\s*\d+\s*\+\s*\d+\s*=\s*\d+", ctx["stdout"]) is not None \
        or "合计" in ctx["stdout"] or "总和" in ctx["stdout"]


def hp_dropped(ctx):
    """连续扣血：输出里剩余血量至少出现 3 次且递减。"""
    import re
    nums = [int(x) for x in re.findall(r"剩余\s*(\d+)", ctx["stdout"])]
    if len(nums) < 3:
        return False
    return all(nums[i] > nums[i + 1] for i in range(len(nums) - 1))


def grades_shown(ctx):
    out = ctx["stdout"]
    return "优秀" in out and "及格" in out and "再努力一下" in out


def report_printed(ctx):
    return "战报" in ctx["stdout"]


CHECKS = [
    {
        "id": "returns",
        "desc": "五个函数都用 return 交回结果",
        "type": "custom", "fn": "all_return",
        "fail": "roll / deal_damage / is_alive / grade / battle_report 每个都要有 `return`",
    },
    {
        "id": "no-print",
        "desc": "函数内部没有 print",
        "type": "custom", "fn": "no_print_inside",
        "fail": "这五个函数只负责**算和返回**，打印全部交给主流程 —— "
                "函数里一个 `print` 都不要写",
    },
    {
        "id": "roll",
        "desc": "roll 返回范围内的随机整数",
        "type": "custom", "fn": "roll_ok",
        "fail": "`return random.randint(1, sides)` —— 要真的随机，而且范围是 1 到 sides",
    },
    {
        "id": "damage",
        "desc": "deal_damage 算对且保底 1",
        "type": "custom", "fn": "damage_ok",
        "fail": "88 打 25 应返回 63；10 打 99 应返回 **1**（保底）。"
                "可以用 `return max(atk - defense, 1)`",
    },
    {
        "id": "alive",
        "desc": "is_alive 返回真正的布尔值",
        "type": "custom", "fn": "alive_ok",
        "fail": "`return hp > 0` —— 比较本身就是 True/False，不用写 if-else",
    },
    {
        "id": "grade",
        "desc": "grade 三档都对（边界也对）",
        "type": "custom", "fn": "grade_ok",
        "fail": "90 分要算「优秀」、60 分要算「及格」—— 用 `>=` 不是 `>`。"
                "而且分档要从高到低写",
    },
    {
        "id": "report",
        "desc": "battle_report 返回字符串",
        "type": "custom", "fn": "report_returns_str",
        "fail": "它要 `return` 一个字符串（里面带上名字和血量），**不是 print**",
    },
    {
        "id": "dice-sum",
        "desc": "主流程把三次点数加起来了",
        "type": "custom", "fn": "dice_summed",
        "fail": "掷 3 次并把点数相加 —— 这正是 `return` 才能做到的事",
    },
    {
        "id": "hp-drop",
        "desc": "用返回值真的扣了血（连续 3 次递减）",
        "type": "custom", "fn": "hp_dropped",
        "fail": "`enemy_hp = enemy_hp - deal_damage(...)`，每次打印「剩余 xxx」，"
                "血量应该一次比一次少",
    },
    {
        "id": "grades",
        "desc": "三种等第都出现了",
        "type": "custom", "fn": "grades_shown",
        "fail": "用 3 个不同分数调用 `grade`，让三档都显示一次",
    },
    {
        "id": "report-printed",
        "desc": "打印了战报",
        "type": "custom", "fn": "report_printed",
        "fail": "`print(battle_report(\"星野樱\", 340))` —— 函数返回字符串，主流程负责打印",
    },
]
