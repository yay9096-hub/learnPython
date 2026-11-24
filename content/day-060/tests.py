import ast

SUBCLASSES = ["Warrior", "Mage", "Rogue"]


def _classes(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.ClassDef)}


def _methods_of(ctx, name):
    cls = _classes(ctx).get(name)
    if cls is None:
        return {}
    return {f.name: f for f in cls.body if isinstance(f, ast.FunctionDef)}


def all_override(ctx):
    """三个子类都要重写 attack 和 skill_name。"""
    for name in SUBCLASSES:
        fns = _methods_of(ctx, name)
        if "attack" not in fns or "skill_name" not in fns:
            return False
    return True


def base_not_reoverridden(ctx):
    """take_damage / status 只写在 Role 里。"""
    for name in SUBCLASSES:
        fns = _methods_of(ctx, name)
        if "take_damage" in fns or "status" in fns:
            return False
    return True


def role_attack(ctx):
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    a = R("甲", 100, 30)
    t = R("木桩", 999)
    dmg = a.attack(t)
    return dmg == 30 and t.hp == 969


def role_skill_name(ctx):
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    return R("甲").skill_name() == "普通攻击"


def warrior_uses_super(ctx):
    """战士的 attack 必须调 super().attack，不许抄一遍父类逻辑。"""
    fn = _methods_of(ctx, "Warrior").get("attack")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "attack":
                inner = n.func.value
                if isinstance(inner, ast.Call) and getattr(inner.func, "id", None) == "super":
                    return True
    return False


def warrior_damage(ctx):
    """40 攻击：基础 40 + 额外 20 = 60，目标要真的掉 60。"""
    ns = ctx["ns"]
    W, R = ns.get("Warrior"), ns.get("Role")
    if not isinstance(W, type) or not isinstance(R, type):
        return False
    w = W("铁壁", 200, 40)
    t = R("木桩", 999)
    dmg = w.attack(t)
    return dmg == 60 and t.hp == 939


def mage_with_mp(ctx):
    ns = ctx["ns"]
    M, R = ns.get("Mage"), ns.get("Role")
    if not isinstance(M, type) or not isinstance(R, type):
        return False
    m = M("琉璃", 120, 25, 100)
    t = R("木桩", 999)
    dmg = m.attack(t)
    return dmg == 75 and t.hp == 924 and m.mp == 80


def mage_without_mp(ctx):
    """蓝不够要退回普通攻击（伤害等于 atk），而且不能扣蓝。"""
    ns = ctx["ns"]
    M, R = ns.get("Mage"), ns.get("Role")
    if not isinstance(M, type) or not isinstance(R, type):
        return False
    m = M("琉璃", 120, 25, 100)
    m.mp = 5
    t = R("木桩", 999)
    dmg = m.attack(t)
    return dmg == 25 and t.hp == 974 and m.mp == 5


def mage_fallback_uses_super(ctx):
    """退回普通攻击要调 super()，不是自己再写一遍。"""
    fn = _methods_of(ctx, "Mage").get("attack")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "attack":
                inner = n.func.value
                if isinstance(inner, ast.Call) and getattr(inner.func, "id", None) == "super":
                    return True
    return False


def mage_skill_name_switches(ctx):
    M = ctx["ns"].get("Mage")
    if not isinstance(M, type):
        return False
    m = M("琉璃", 120, 25, 100)
    if m.skill_name() != "奥术飞弹":
        return False
    m.mp = 5
    return m.skill_name() == "法杖敲击"


def rogue_damage(ctx):
    ns = ctx["ns"]
    Ro, R = ns.get("Rogue"), ns.get("Role")
    if not isinstance(Ro, type) or not isinstance(R, type):
        return False
    r = Ro("影", 140, 35)
    t = R("木桩", 999)
    dmg = r.attack(t)
    return dmg == 87 and t.hp == 912


def polymorphism_works(ctx):
    """同一句 m.attack(t)，四种不同伤害。"""
    ns = ctx["ns"]
    R, W, M, Ro = (ns.get("Role"), ns.get("Warrior"),
                   ns.get("Mage"), ns.get("Rogue"))
    if not all(isinstance(c, type) for c in [R, W, M, Ro]):
        return False
    results = []
    for cls in [R, W, M, Ro]:
        obj = cls("测试", 200, 40, 100)
        target = R("木桩", 9999)
        results.append(obj.attack(target))
    return len(set(results)) == 4


def no_isinstance_in_main(ctx):
    """主流程里不许用 isinstance 分派 —— 那就白写多态了。"""
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "isinstance":
            return False
    return True


def single_loop_attack(ctx):
    """全员攻击是一个 for 循环干的。"""
    for n in ast.walk(ctx["tree"]):
        if not isinstance(n, ast.For):
            continue
        for sub in ast.walk(n):
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                if sub.func.attr == "attack":
                    return True
    return False


def four_skills_shown(ctx):
    out = ctx["stdout"]
    return all(s in out for s in ["普通攻击", "狂暴重击", "奥术飞弹", "背刺"])


def fallback_demo(ctx):
    return "法杖敲击" in ctx["stdout"]


def class_table(ctx):
    out = ctx["stdout"]
    return "Warrior" in out and "Mage" in out and "Rogue" in out


def boss_hp_shown(ctx):
    return "剩余" in ctx["stdout"]


CHECKS = [
    {"id": "override", "desc": "三个子类都重写了 attack 和 skill_name",
     "type": "custom", "fn": "all_override",
     "fail": "Warrior / Mage / Rogue 里都要有自己的 `attack` 和 `skill_name`"},
    {"id": "no-recopy", "desc": "take_damage 和 status 只写在 Role 里",
     "type": "custom", "fn": "base_not_reoverridden",
     "fail": "这两个所有职业都一样，**不要在子类里重写**"},
    {"id": "role-atk", "desc": "Role 的普通攻击正确",
     "type": "custom", "fn": "role_attack",
     "fail": "造成 `self.atk` 点伤害，要真的调 `target.take_damage(...)`，并返回伤害值"},
    {"id": "role-name", "desc": "Role 的技能名是「普通攻击」",
     "type": "custom", "fn": "role_skill_name",
     "fail": "父类的 `skill_name` 返回 `\"普通攻击\"`"},
    {"id": "w-super", "desc": "战士用 super() 扩展父类",
     "type": "custom", "fn": "warrior_uses_super",
     "fail": "⚠️ 战士的 attack 里必须写 `super().attack(target)` —— "
             "不许把父类的逻辑抄一遍"},
    {"id": "w-damage", "desc": "战士总伤害 = 基础 + atk//2",
     "type": "custom", "fn": "warrior_damage",
     "fail": "40 攻击：基础 40 + 追加 20 = **60**。"
             "追加那部分也要真的 `target.take_damage(bonus)`"},
    {"id": "m-with-mp", "desc": "法师有蓝时三倍伤害并扣蓝",
     "type": "custom", "fn": "mage_with_mp",
     "fail": "25 攻击 × 3 = **75** 伤害，MP 从 100 扣到 80"},
    {"id": "m-fallback", "desc": "法师没蓝时退回普通攻击",
     "type": "custom", "fn": "mage_without_mp",
     "fail": "MP 只有 5 时伤害应该是 **25**（等于 atk），"
             "而且**不能再扣蓝**"},
    {"id": "m-super", "desc": "退回普通攻击用的是 super()",
     "type": "custom", "fn": "mage_fallback_uses_super",
     "fail": "`return super().attack(target)` —— 复用父类的实现"},
    {"id": "m-name", "desc": "法师技能名会随蓝量切换",
     "type": "custom", "fn": "mage_skill_name_switches",
     "fail": "蓝够返回「奥术飞弹」，不够返回「法杖敲击」"},
    {"id": "r-damage", "desc": "盗贼伤害 = int(atk * 2.5)",
     "type": "custom", "fn": "rogue_damage",
     "fail": "35 × 2.5 = 87.5，取整是 **87**"},
    {"id": "poly", "desc": "四个职业打出四种不同伤害",
     "type": "custom", "fn": "polymorphism_works",
     "fail": "同样的攻击力，四个类应该给出四个不同的结果 —— 这才叫多态"},
    {"id": "no-isinstance", "desc": "主流程里没有 isinstance",
     "type": "custom", "fn": "no_isinstance_in_main",
     "fail": "⚠️ 用了 `isinstance` 分派就白写多态了 —— "
             "让每个对象自己知道该怎么打",
     },
    {"id": "one-loop", "desc": "全员攻击用一个 for 循环",
     "type": "custom", "fn": "single_loop_attack",
     "fail": "`for m in team: m.attack(boss)` —— 一句话搞定所有职业"},
    {"id": "skills", "desc": "四种技能名都出现了",
     "type": "custom", "fn": "four_skills_shown",
     "fail": "普通攻击 / 狂暴重击 / 奥术飞弹 / 背刺，四个都要打印出来"},
    {"id": "fallback-demo", "desc": "演示了法师没蓝的情况",
     "type": "custom", "fn": "fallback_demo",
     "fail": "把 `mage.mp` 调低再打一次，技能名会变成「法杖敲击」"},
    {"id": "table", "desc": "打印了类名对照表",
     "type": "custom", "fn": "class_table",
     "fail": "用 `type(m).__name__` 打印每个角色的职业名"},
    {"id": "boss", "desc": "打印了敌人剩余血量",
     "type": "custom", "fn": "boss_hp_shown",
     "fail": "打完之后报一下 boss 还剩多少血"},
]
