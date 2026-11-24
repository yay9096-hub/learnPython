import ast

SUBCLASSES = ["Warrior", "Mage", "Rogue"]
INHERITED = ["take_damage", "heal", "status", "is_alive"]


def _classes(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.ClassDef)}


def _methods_of(ctx, name):
    cls = _classes(ctx).get(name)
    if cls is None:
        return {}
    return {f.name: f for f in cls.body if isinstance(f, ast.FunctionDef)}


def all_subclass(ctx):
    """三个子类都要继承自 Role。"""
    ns = ctx["ns"]
    base = ns.get("Role")
    if not isinstance(base, type):
        return False
    for name in SUBCLASSES:
        cls = ns.get(name)
        if not isinstance(cls, type) or not issubclass(cls, base) or cls is base:
            return False
    return True


def calls_super(ctx):
    """三个子类的 __init__ 第一件事都该是 super().__init__(...)。"""
    for name in SUBCLASSES:
        init = _methods_of(ctx, name).get("__init__")
        if init is None:
            return False
        found = False
        for n in ast.walk(init):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
                if n.func.attr == "__init__":
                    inner = n.func.value
                    if isinstance(inner, ast.Call) and getattr(inner.func, "id", None) == "super":
                        found = True
        if not found:
            return False
    return True


def no_redefine(ctx):
    """子类不许重写父类已有的通用方法 —— 那就白继承了。"""
    for name in SUBCLASSES:
        fns = _methods_of(ctx, name)
        for m in INHERITED:
            if m in fns:
                return False
    return True


def inherits_work(ctx):
    """子类实例能直接用父类的方法。"""
    ns = ctx["ns"]
    W = ns.get("Warrior")
    if not isinstance(W, type):
        return False
    w = W("测试战士")
    if not hasattr(w, "status") or not hasattr(w, "take_damage"):
        return False
    before = w.hp
    w.take_damage(30)
    return w.hp == before - 30 and isinstance(w.status(), str)


def warrior_attrs(ctx):
    W = ctx["ns"].get("Warrior")
    if not isinstance(W, type):
        return False
    w = W("测试战士")
    return (getattr(w, "armor", None) == 10 and w.hp == 200
            and w.atk == 40 and w.name == "测试战士"
            and getattr(w, "alive", None) is True)


def warrior_real_damage(ctx):
    W = ctx["ns"].get("Warrior")
    if not isinstance(W, type):
        return False
    w = W("测试", 200, 40, 10)
    return w.real_damage(50) == 40 and w.real_damage(5) == 1 and w.real_damage(10) == 1


def warrior_roar(ctx):
    W = ctx["ns"].get("Warrior")
    if not isinstance(W, type):
        return False
    w = W("测试", 200, 40, 10)
    r = w.roar()
    return w.atk == 50 and isinstance(r, str) and "测试" in r


def mage_attrs(ctx):
    M = ctx["ns"].get("Mage")
    if not isinstance(M, type):
        return False
    m = M("测试法师")
    return (getattr(m, "mp", None) == 100 and getattr(m, "max_mp", None) == 100
            and m.hp == 120 and m.atk == 25)


def mage_cast_ok(ctx):
    ns = ctx["ns"]
    M, R = ns.get("Mage"), ns.get("Role")
    if not isinstance(M, type) or not isinstance(R, type):
        return False
    m = M("测试", 120, 25, 100)
    t = R("木桩", 999)
    dmg = m.cast(t)
    return dmg == 50 and m.mp == 80 and t.hp == 949


def mage_cast_blocked(ctx):
    ns = ctx["ns"]
    M, R = ns.get("Mage"), ns.get("Role")
    if not isinstance(M, type) or not isinstance(R, type):
        return False
    m = M("测试", 120, 25, 100)
    t = R("木桩", 999)
    m.mp = 5
    dmg = m.cast(t)
    return dmg == 0 and t.hp == 999 and m.mp == 5


def rogue_backstab(ctx):
    ns = ctx["ns"]
    Ro, R = ns.get("Rogue"), ns.get("Role")
    if not isinstance(Ro, type) or not isinstance(R, type):
        return False
    r = Ro("测试", 140, 35, 2.0)
    t = R("木桩", 999)
    dmg = r.backstab(t)
    return dmg == 70 and t.hp == 929


def shows_class_names(ctx):
    out = ctx["stdout"]
    return "Warrior" in out and "Mage" in out and "Rogue" in out


def uses_type_name(ctx):
    return "__name__" in ctx["code"]


def uses_isinstance(ctx):
    return any(isinstance(n, ast.Call) and getattr(n.func, "id", None) == "isinstance"
               for n in ast.walk(ctx["tree"]))


def isinstance_demo(ctx):
    """输出里既有 True 也有 False，说明两种情况都演示了。"""
    out = ctx["stdout"]
    return "True" in out and "False" in out


def demo_armor(ctx):
    """护甲演示：50 点打成 40，5 点打成 1。"""
    out = ctx["stdout"]
    return "40" in out and "1" in out


def demo_mp_out(ctx):
    return "魔力不足" in ctx["stdout"] or "不足" in ctx["stdout"]


def counts_by_class(ctx):
    """统计了各职业人数。"""
    for k, v in ctx["ns"].items():
        if k.startswith("__") or not isinstance(v, dict):
            continue
        if set(v.keys()) & {"Warrior", "Mage", "Rogue"}:
            return True
    return False


CHECKS = [
    {"id": "warrior", "desc": "Warrior 继承自 Role",
     "type": "class_defined", "name": "Warrior", "base": "Role",
     "methods": ["real_damage", "roar"],
     "fail": "`class Warrior(Role):`，并且有 `real_damage` 和 `roar` 两个方法"},
    {"id": "mage", "desc": "Mage 继承自 Role",
     "type": "class_defined", "name": "Mage", "base": "Role", "methods": ["cast"],
     "fail": "`class Mage(Role):`，并且有 `cast` 方法"},
    {"id": "rogue", "desc": "Rogue 继承自 Role",
     "type": "class_defined", "name": "Rogue", "base": "Role", "methods": ["backstab"],
     "fail": "`class Rogue(Role):`，并且有 `backstab` 方法"},
    {"id": "subclass", "desc": "三个都是 Role 的子类",
     "type": "custom", "fn": "all_subclass",
     "fail": "类名后面的括号里要写 `Role`"},
    {"id": "super", "desc": "三个 __init__ 都调了 super()",
     "type": "custom", "fn": "calls_super",
     "fail": "⚠️ 子类 `__init__` 的第一句应该是 "
             "`super().__init__(name, hp, atk)` —— "
             "忘了它，父类设的属性全都不存在"},
    {"id": "no-redefine", "desc": "子类没有重复写父类的方法",
     "type": "custom", "fn": "no_redefine",
     "fail": "`take_damage` / `heal` / `status` / `is_alive` 是继承来的，"
             "**子类里不要再写一遍** —— 那就白继承了"},
    {"id": "inherit", "desc": "子类能直接用父类的方法",
     "type": "custom", "fn": "inherits_work",
     "fail": "战士没写 `take_damage` 也应该能用 —— 这就是继承"},
    {"id": "w-attrs", "desc": "战士的属性和默认值都对",
     "type": "custom", "fn": "warrior_attrs",
     "fail": "`Warrior(\"名字\")` 之后：hp=200 / atk=40 / armor=10，"
             "而且 `alive` 这些父类属性也要有"},
    {"id": "w-armor", "desc": "护甲减免正确且最低 1 点",
     "type": "custom", "fn": "warrior_real_damage",
     "fail": "50 - 10 = 40；但 5 点伤害减完是负数，要用 `max(1, ...)` 保底"},
    {"id": "w-roar", "desc": "怒吼加攻击并返回文字",
     "type": "custom", "fn": "warrior_roar",
     "fail": "攻击力 +10，并 `return` 一句带名字的话"},
    {"id": "m-attrs", "desc": "法师的 mp 和 max_mp 都对",
     "type": "custom", "fn": "mage_attrs",
     "fail": "`super()` 之后加 `self.mp = mp` 和 `self.max_mp = mp`"},
    {"id": "m-cast", "desc": "施法扣蓝并造成双倍伤害",
     "type": "custom", "fn": "mage_cast_ok",
     "fail": "扣 20 蓝，造成 `atk * 2` = 50 点伤害，返回伤害值"},
    {"id": "m-blocked", "desc": "魔力不够时放不出来",
     "type": "custom", "fn": "mage_cast_blocked",
     "fail": "`if self.mp < cost: return 0` —— "
             "而且**不能扣蓝、不能扣对方的血**"},
    {"id": "r-backstab", "desc": "背刺伤害正确",
     "type": "custom", "fn": "rogue_backstab",
     "fail": "`int(self.atk * self.crit)` = 35 × 2.0 = 70"},
    {"id": "type-name", "desc": "用 type().__name__ 显示职业",
     "type": "custom", "fn": "uses_type_name",
     "fail": "`type(m).__name__` 能拿到类名的文字"},
    {"id": "names-shown", "desc": "三个职业名都打印了",
     "type": "custom", "fn": "shows_class_names",
     "fail": "遍历队伍时把职业名一起打印出来"},
    {"id": "isinstance", "desc": "用了 isinstance",
     "type": "custom", "fn": "uses_isinstance",
     "fail": "用 `isinstance(warrior, Role)` 证明「战士也是 Role」"},
    {"id": "isinstance-demo", "desc": "isinstance 两种结果都演示了",
     "type": "custom", "fn": "isinstance_demo",
     "fail": "既要有 True（是 Warrior、是 Role），也要有 False（不是 Mage）"},
    {"id": "armor-demo", "desc": "演示了护甲的两种情况",
     "type": "custom", "fn": "demo_armor",
     "fail": "大伤害和小伤害各演示一次，看得出「最低 1 点」的保底"},
    {"id": "mp-demo", "desc": "演示了魔力不足",
     "type": "custom", "fn": "demo_mp_out",
     "fail": "把 mp 调低再施法一次，验证放不出来"},
    {"id": "counts", "desc": "按职业统计了人数",
     "type": "custom", "fn": "counts_by_class",
     "fail": "用字典统计：`counts[kind] = counts.get(kind, 0) + 1`"},
]
