import ast


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def wrong_has_no_return(ctx):
    """damage_wrong 必须不 return —— 这是它「错」的关键。"""
    fn = _funcs(ctx).get("damage_wrong")
    if fn is None:
        return False
    return not any(isinstance(n, ast.Return) and n.value is not None
                   for n in ast.walk(fn))


def wrong_really_wrong(ctx):
    """调用它之后外面的数字不该变。"""
    fn = ctx["ns"].get("damage_wrong")
    if not callable(fn):
        return False
    hp = 500
    try:
        fn(hp, 63)
    except Exception:
        return False
    return hp == 500


def right_returns(ctx):
    fn = ctx["ns"].get("damage_right")
    if not callable(fn):
        return False
    return fn(500, 63) == 437 and fn(100, 30) == 70


def dict_mutates(ctx):
    """damage_dict 改的是传进来的那个字典本身。"""
    fn = ctx["ns"].get("damage_dict")
    if not callable(fn):
        return False
    role = {"name": "测试者", "hp": 500}
    try:
        fn(role, 63)
    except Exception:
        return False
    return role["hp"] == 437


def dict_no_return_needed(ctx):
    """damage_dict 不该靠 return 生效。"""
    fn = _funcs(ctx).get("damage_dict")
    if fn is None:
        return False
    return not any(isinstance(n, ast.Return) and n.value is not None
                   for n in ast.walk(fn))


def heal_works(ctx):
    fn = ctx["ns"].get("heal_team")
    if not callable(fn):
        return False
    team = [{"name": "甲", "hp": 100}, {"name": "乙", "hp": 200}]
    try:
        fn(team, 50)
    except Exception:
        return False
    return team[0]["hp"] == 150 and team[1]["hp"] == 250


def rename_no_effect(ctx):
    fn = ctx["ns"].get("rename_wrong")
    if not callable(fn):
        return False
    name = "原名"
    try:
        fn(name)
    except Exception:
        return False
    return name == "原名"


def shows_before_after(ctx):
    """输出里要能看出「前后对比」：调用前后各打印一次。"""
    out = ctx["stdout"]
    return out.count("调用前") >= 3 and out.count("调用后") >= 3


def shows_unchanged(ctx):
    """① 的前后两个 500 都出现了。"""
    import re
    lines = ctx["stdout"].splitlines()
    for i, line in enumerate(lines):
        if "调用前" in line and "500" in line:
            for after in lines[i:i + 4]:
                if "调用后" in after and "500" in after:
                    return True
    return False


def shows_changed(ctx):
    """② 或 ③ 出现了 437。"""
    return "437" in ctx["stdout"]


def team_healed(ctx):
    """整队加血前后的数字都出现了。"""
    out = ctx["stdout"]
    return "340" in out and "390" in out


def has_conclusion(ctx):
    return "return" in ctx["stdout"].lower()


def no_global(ctx):
    """今天不该用 global —— 讲解里明说了不推荐。"""
    return not any(isinstance(n, ast.Global) for n in ast.walk(ctx["tree"]))


CHECKS = [
    {
        "id": "wrong-noreturn",
        "desc": "damage_wrong 故意不写 return",
        "type": "custom", "fn": "wrong_has_no_return",
        "fail": "这个函数就是用来演示「错在哪」的，**不要**给它加 return",
    },
    {
        "id": "wrong-effect",
        "desc": "damage_wrong 确实改不动外面",
        "type": "custom", "fn": "wrong_really_wrong",
        "fail": "函数里 `hp = hp - dmg` 只改了局部变量，外面的数字应该纹丝不动",
    },
    {
        "id": "right",
        "desc": "damage_right 返回正确的新血量",
        "type": "custom", "fn": "right_returns",
        "fail": "`return hp - dmg` —— 500 扣 63 应该返回 437",
    },
    {
        "id": "dict-mutate",
        "desc": "damage_dict 直接改到了字典",
        "type": "custom", "fn": "dict_mutates",
        "fail": "`role[\"hp\"] = role[\"hp\"] - dmg` —— 字典是可变对象，改内容外面就能看见",
    },
    {
        "id": "dict-noreturn",
        "desc": "damage_dict 不靠 return 生效",
        "type": "custom", "fn": "dict_no_return_needed",
        "fail": "字典版不需要 return，这正是它和数字版的区别",
    },
    {
        "id": "heal",
        "desc": "heal_team 给全队加了血",
        "type": "custom", "fn": "heal_works",
        "fail": "遍历列表，给每个 `member[\"hp\"]` 加上 amount",
    },
    {
        "id": "rename",
        "desc": "rename_wrong 确实改不动字符串",
        "type": "custom", "fn": "rename_no_effect",
        "fail": "字符串跟数字一样是不可变的，函数里改了外面看不见",
    },
    {
        "id": "compare",
        "desc": "三种做法都打印了前后对比",
        "type": "custom", "fn": "shows_before_after",
        "fail": "每种做法都要打印「调用前」和「调用后」的血量，才看得出差别",
    },
    {
        "id": "unchanged",
        "desc": "第 ① 种前后都是 500（没变）",
        "type": "custom", "fn": "shows_unchanged",
        "fail": "不 return 的那次，调用前后都应该是 500 —— 这就是今天要看见的现象",
    },
    {
        "id": "changed",
        "desc": "第 ② / ③ 种真的变成了 437",
        "type": "custom", "fn": "shows_changed",
        "fail": "用 return 接住、或者改字典，血量应该变成 437",
    },
    {
        "id": "team",
        "desc": "整队加血前后都打印了",
        "type": "custom", "fn": "team_healed",
        "fail": "队伍里有人 340 血，加 50 之后应该变成 390，前后都要打印出来",
    },
    {
        "id": "no-global",
        "desc": "没有用 global",
        "type": "custom", "fn": "no_global",
        "fail": "`global` 能用但不推荐 —— 今天用 return 和可变对象两种正道就够了",
    },
    {
        "id": "conclusion",
        "desc": "写了自己的结论",
        "type": "custom", "fn": "has_conclusion",
        "fail": "最后打印一句你自己的总结，里面要提到 `return`",
    },
]
