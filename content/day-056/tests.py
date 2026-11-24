import ast

METHODS = ["is_alive", "take_damage", "attack", "heal", "level_up", "status"]


def _class_methods(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ClassDef) and n.name == "Role":
            return {f.name: f for f in n.body if isinstance(f, ast.FunctionDef)}
    return {}


def all_methods(ctx):
    fns = _class_methods(ctx)
    return all(m in fns for m in METHODS)


def methods_have_self(ctx):
    fns = _class_methods(ctx)
    for name, fn in fns.items():
        if not fn.args.args or fn.args.args[0].arg != "self":
            return False
    return True


def is_alive_ok(ctx):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("测试", 100)
    if r.is_alive() is not True:
        return False
    r.hp = 0
    if r.is_alive() is not False:
        return False
    r.hp = -5
    return r.is_alive() is False


def take_damage_ok(ctx):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("测试", 100)
    got = r.take_damage(30)
    return r.hp == 70 and got == 30


def take_damage_sets_alive(ctx):
    """血量掉到 0 以下要把 alive 设成 False。"""
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("测试", 50)
    r.take_damage(80)
    return getattr(r, "alive", True) is False


def attack_hits_target(ctx):
    """攻击要真的扣掉对方的血，而不是自己的。"""
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    a = cls("甲", 200, 50, 40)
    b = cls("乙", 200, 50, 30)
    got = a.attack(b)
    return b.hp == 160 and a.hp == 200 and got == 40


def attack_uses_take_damage(ctx):
    """attack 里要调用 target.take_damage，不要自己改 target.hp。"""
    fn = _class_methods(ctx).get("attack")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "take_damage":
                return True
    return False


def heal_ok(ctx):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("测试", 100)
    r.hp = 40
    got = r.heal(30)
    return r.hp == 70 and got == 30


def level_up_ok(ctx):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("测试", 100, 50, 30)
    r.hp = 20
    r.level_up()
    return (r.level == 2 and r.max_hp == 120
            and r.atk == 35 and r.hp == 120)


def status_returns_string(ctx):
    """status 要 return，不是 print。"""
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("测试者", 100)
    s = r.status()
    return isinstance(s, str) and "测试者" in s and len(s) > 5


def status_no_print(ctx):
    fn = _class_methods(ctx).get("status")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "print":
            return False
    return True


def calls_own_method(ctx):
    """某个方法里用 self.xxx() 调了自己的别的方法。"""
    fns = _class_methods(ctx)
    for name, fn in fns.items():
        for n in ast.walk(fn):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                if (isinstance(n.func.value, ast.Name)
                        and n.func.value.id == "self"
                        and n.func.attr in METHODS):
                    return True
    return False


def two_roles(ctx):
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "Role")
    return n >= 2


def battle_rounds(ctx):
    """至少打了 3 个回合。"""
    import re
    return len(re.findall(r"第\s*\d+\s*回合", ctx["stdout"])) >= 3


def used_heal_and_levelup(ctx):
    out = ctx["stdout"]
    return "恢复" in out and "升到" in out


def declares_winner(ctx):
    out = ctx["stdout"]
    return "获胜" in out or "平手" in out


def loop_uses_is_alive(ctx):
    """主流程用 is_alive 控制战斗。"""
    src = ctx["code"]
    return "is_alive()" in src.replace(" ", "")


CHECKS = [
    {"id": "class", "desc": "Role 类带全部六个方法",
     "type": "class_defined", "name": "Role",
     "methods": METHODS,
     "fail": "is_alive / take_damage / attack / heal / level_up / status，方法名照抄"},
    {"id": "self", "desc": "每个方法第一个参数都是 self",
     "type": "custom", "fn": "methods_have_self",
     "fail": "方法的第一个参数永远是 `self`，调用时不用你传"},
    {"id": "alive", "desc": "is_alive 判断正确",
     "type": "custom", "fn": "is_alive_ok",
     "fail": "`return self.hp > 0`。血量 0 和负数都算倒下"},
    {"id": "damage", "desc": "take_damage 扣血且有返回值",
     "type": "custom", "fn": "take_damage_ok",
     "fail": "`self.hp = self.hp - amount`，并且 `return amount`"},
    {"id": "damage-alive", "desc": "血掉光时 alive 变成 False",
     "type": "custom", "fn": "take_damage_sets_alive",
     "fail": "扣完血检查一下，`if not self.is_alive(): self.alive = False`"},
    {"id": "attack", "desc": "attack 扣的是对方的血",
     "type": "custom", "fn": "attack_hits_target",
     "fail": "`self` 是攻击者、`target` 是挨打的。"
             "40 攻击力打过去，对方掉 40，自己不掉血"},
    {"id": "attack-reuse", "desc": "attack 调用了 target.take_damage",
     "type": "custom", "fn": "attack_uses_take_damage",
     "fail": "别在 attack 里直接改 `target.hp` —— "
             "调 `target.take_damage(damage)`，倒下判断才不会漏掉"},
    {"id": "heal", "desc": "heal 回血且有返回值",
     "type": "custom", "fn": "heal_ok",
     "fail": "回血之后 `return amount`"},
    {"id": "levelup", "desc": "level_up 五项变化都对",
     "type": "custom", "fn": "level_up_ok",
     "fail": "等级 +1、max_hp +20、atk +5，而且 **hp 要回满**（等于新的 max_hp）"},
    {"id": "status-return", "desc": "status 返回字符串",
     "type": "custom", "fn": "status_returns_string",
     "fail": "`status` 要 `return` 一行文字，里面带上名字"},
    {"id": "status-no-print", "desc": "status 里没有 print",
     "type": "custom", "fn": "status_no_print",
     "fail": "Day 37 的原则：算的只算，打印交给主流程"},
    {"id": "self-call", "desc": "方法里调用了自己的别的方法",
     "type": "custom", "fn": "calls_own_method",
     "fail": "比如 `take_damage` 里调 `self.is_alive()` —— "
             "⚠️ 调自己的方法也要写 `self.`"},
    {"id": "two", "desc": "造了两个角色",
     "type": "custom", "fn": "two_roles",
     "fail": "我方一个、敌方一个"},
    {"id": "rounds", "desc": "打了至少 3 个回合",
     "type": "custom", "fn": "battle_rounds",
     "fail": "用循环打回合，每回合打印「第 N 回合」"},
    {"id": "loop-alive", "desc": "用 is_alive 控制战斗",
     "type": "custom", "fn": "loop_uses_is_alive",
     "fail": "`while hero.is_alive() and enemy.is_alive():` —— 有人倒下就该停"},
    {"id": "heal-level", "desc": "用过 heal 和 level_up",
     "type": "custom", "fn": "used_heal_and_levelup",
     "fail": "战斗中途各用一次，输出里要看得到「恢复」和「升到」"},
    {"id": "winner", "desc": "宣布了胜负",
     "type": "custom", "fn": "declares_winner",
     "fail": "最后根据 `is_alive()` 判断谁赢了"},
]
