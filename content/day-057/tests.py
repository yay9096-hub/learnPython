import ast

METHODS = ["take_damage", "heal", "attack", "revive",
           "level_up", "hp_percent", "status"]


def _class_methods(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ClassDef) and n.name == "Role":
            return {f.name: f for f in n.body if isinstance(f, ast.FunctionDef)}
    return {}


def all_methods(ctx):
    fns = _class_methods(ctx)
    return all(m in fns for m in METHODS)


def _make(ctx, *a, **kw):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return None
    try:
        return cls(*a, **kw)
    except Exception:
        return None


def init_rejects_bad_hp(ctx):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    for bad in [0, -10]:
        try:
            cls("测试", bad)
            return False
        except ValueError:
            continue
        except Exception:
            return False
    return True


def damage_floors_at_zero(ctx):
    """过量伤害血量停在 0，不能变负。"""
    r = _make(ctx, "测试", 100)
    if r is None:
        return False
    r.take_damage(999)
    return r.hp == 0


def damage_returns_actual(ctx):
    """返回的是实际扣掉的血，不是请求值。"""
    r = _make(ctx, "测试", 100)
    if r is None:
        return False
    got = r.take_damage(999)
    return got == 100


def damage_syncs_alive(ctx):
    r = _make(ctx, "测试", 100)
    if r is None:
        return False
    r.take_damage(50)
    if r.alive is not True:
        return False
    r.take_damage(50)
    return r.alive is False


def damage_rejects_negative(ctx):
    r = _make(ctx, "测试", 100)
    if r is None:
        return False
    try:
        r.take_damage(-100)
        return False
    except ValueError:
        return True
    except Exception:
        return False


def heal_caps_at_max(ctx):
    """过量治疗停在满血。"""
    r = _make(ctx, "测试", 100)
    if r is None:
        return False
    r.take_damage(30)
    r.heal(9999)
    return r.hp == 100


def heal_returns_actual(ctx):
    """想治 50 但只差 30 血时，要返回 30。"""
    r = _make(ctx, "测试", 100)
    if r is None:
        return False
    r.take_damage(30)
    got = r.heal(50)
    return got == 30


def heal_blocked_when_dead(ctx):
    r = _make(ctx, "测试", 100)
    if r is None:
        return False
    r.take_damage(999)
    got = r.heal(50)
    return got == 0 and r.hp == 0


def heal_rejects_negative(ctx):
    r = _make(ctx, "测试", 100)
    if r is None:
        return False
    try:
        r.heal(-50)
        return False
    except ValueError:
        return True
    except Exception:
        return False


def attack_blocked_when_dead(ctx):
    a = _make(ctx, "甲", 100, 40)
    b = _make(ctx, "乙", 100, 30)
    if a is None or b is None:
        return False
    a.take_damage(999)
    got = a.attack(b)
    return got == 0 and b.hp == 100


def attack_works_when_alive(ctx):
    a = _make(ctx, "甲", 100, 40)
    b = _make(ctx, "乙", 100, 30)
    if a is None or b is None:
        return False
    got = a.attack(b)
    return got == 40 and b.hp == 60


def revive_only_when_dead(ctx):
    r = _make(ctx, "测试", 200)
    if r is None:
        return False
    if r.revive() is not False:
        return False
    r.take_damage(999)
    if r.revive() is not True:
        return False
    return r.alive is True and r.hp == 100


def revive_at_least_one(ctx):
    """比例太小也要至少 1 血，不然复活完还是死的。"""
    r = _make(ctx, "测试", 10)
    if r is None:
        return False
    r.take_damage(999)
    r.revive(0.01)
    return r.hp >= 1 and r.alive is True


def level_up_ok(ctx):
    r = _make(ctx, "测试", 100, 30)
    if r is None:
        return False
    r.take_damage(80)
    r.level_up()
    return (r.level == 2 and r.max_hp == 120
            and r.atk == 35 and r.hp == 120)


def percent_ok(ctx):
    r = _make(ctx, "测试", 200)
    if r is None:
        return False
    if r.hp_percent() != 100:
        return False
    r.take_damage(100)
    if r.hp_percent() != 50:
        return False
    r.take_damage(999)
    return r.hp_percent() == 0


def status_has_bar(ctx):
    """状态里要有血条。"""
    r = _make(ctx, "测试者", 100)
    if r is None:
        return False
    s = r.status()
    if not isinstance(s, str) or "测试者" not in s:
        return False
    return any(ch in s for ch in ["█", "░", "=", "#"])


def uses_clamp(ctx):
    """代码里用了 min/max 做夹取。"""
    src = ctx["code"]
    return "max(0" in src.replace(" ", "") or "min(" in src


def demos_overkill(ctx):
    """演示了过量伤害且血量停在 0。"""
    out = ctx["stdout"]
    return "0/" in out.replace(" ", "") or "0 /" in out


def demos_overheal(ctx):
    return "实际只回了" in ctx["stdout"] or "实际" in ctx["stdout"]


def demos_raise(ctx):
    """至少演示了两次被 raise 挡住。"""
    return ctx["stdout"].count("拦下") >= 2 or ctx["stdout"].count("不能是负数") >= 2


def demos_revive(ctx):
    return "复活了" in ctx["stdout"]


def survived(ctx):
    return ctx["error"] is None


CHECKS = [
    {"id": "methods", "desc": "八个方法都定义了",
     "type": "class_defined", "name": "Role", "methods": METHODS,
     "fail": "take_damage / heal / attack / revive / level_up / hp_percent / status"},
    {"id": "init-guard", "desc": "初始血量 <= 0 会被拒绝",
     "type": "custom", "fn": "init_rejects_bad_hp",
     "fail": "`__init__` 里 `if hp <= 0: raise ValueError(...)`"},
    {"id": "clamp", "desc": "用了 min / max 夹取",
     "type": "custom", "fn": "uses_clamp",
     "fail": "`max(0, self.hp - amount)` 和 `min(self.max_hp, self.hp + amount)`"},
    {"id": "dmg-floor", "desc": "过量伤害血量停在 0",
     "type": "custom", "fn": "damage_floors_at_zero",
     "fail": "打 999 点也只能扣到 0，**不能变成负数**"},
    {"id": "dmg-actual", "desc": "take_damage 返回实际扣血",
     "type": "custom", "fn": "damage_returns_actual",
     "fail": "100 血挨 999 点，实际只扣了 **100** —— 返回实际值不是请求值。"
             "套路：先记 before，改完算差"},
    {"id": "dmg-alive", "desc": "扣血时同步了 alive",
     "type": "custom", "fn": "damage_syncs_alive",
     "fail": "`self.alive = self.hp > 0` —— "
             "两个属性有关联，改一个就要同步另一个"},
    {"id": "dmg-neg", "desc": "负数伤害被拒绝",
     "type": "custom", "fn": "damage_rejects_negative",
     "fail": "负数伤害等于偷偷治疗，要 `raise ValueError`"},
    {"id": "heal-cap", "desc": "过量治疗停在满血",
     "type": "custom", "fn": "heal_caps_at_max",
     "fail": "`min(self.max_hp, self.hp + amount)`"},
    {"id": "heal-actual", "desc": "heal 返回实际回血量",
     "type": "custom", "fn": "heal_returns_actual",
     "fail": "只差 30 血时想治 50，实际只回 **30**"},
    {"id": "heal-dead", "desc": "倒下的角色治不了",
     "type": "custom", "fn": "heal_blocked_when_dead",
     "fail": "`if not self.alive: return 0` —— 而且血量不能被治回来"},
    {"id": "heal-neg", "desc": "负数治疗被拒绝",
     "type": "custom", "fn": "heal_rejects_negative",
     "fail": "同样要 `raise ValueError`"},
    {"id": "atk-alive", "desc": "活着时攻击正常",
     "type": "custom", "fn": "attack_works_when_alive",
     "fail": "40 攻击力打过去，对方掉 40，返回 40"},
    {"id": "atk-dead", "desc": "倒下的角色打不动",
     "type": "custom", "fn": "attack_blocked_when_dead",
     "fail": "自己倒下时返回 0，而且**不能真的扣到对方的血**"},
    {"id": "revive", "desc": "复活只对倒下的有效",
     "type": "custom", "fn": "revive_only_when_dead",
     "fail": "活着时返回 False；倒下时复活到 max_hp 的一半并返回 True"},
    {"id": "revive-min", "desc": "复活后至少 1 血",
     "type": "custom", "fn": "revive_at_least_one",
     "fail": "`max(1, int(self.max_hp * ratio))` —— "
             "不然血少的角色复活完还是 0 血，等于没复活"},
    {"id": "levelup", "desc": "升级四项变化都对",
     "type": "custom", "fn": "level_up_ok",
     "fail": "等级+1、max_hp+20、atk+5，而且 hp 回满"},
    {"id": "percent", "desc": "血量百分比算对",
     "type": "custom", "fn": "percent_ok",
     "fail": "满血 100、半血 50、空血 0"},
    {"id": "bar", "desc": "status 里有血条",
     "type": "custom", "fn": "status_has_bar",
     "fail": "用 `\"█\" * (percent // 10)` 画一个 10 格的血条"},
    {"id": "demo-overkill", "desc": "演示了过量伤害",
     "type": "custom", "fn": "demos_overkill",
     "fail": "打一次超额伤害，让血条停在 0"},
    {"id": "demo-overheal", "desc": "演示了过量治疗",
     "type": "custom", "fn": "demos_overheal",
     "fail": "治一次 9999，打印出「实际只回了 N 点」"},
    {"id": "demo-revive", "desc": "演示了复活",
     "type": "custom", "fn": "demos_revive",
     "fail": "倒下之后调一次 `revive()`"},
    {"id": "demo-raise", "desc": "演示了非法参数被挡住",
     "type": "custom", "fn": "demos_raise",
     "fail": "至少用 `try` 演示两次负数参数被 `raise` 拦下"},
    {"id": "survive", "desc": "全程没有崩溃",
     "type": "custom", "fn": "survived",
     "fail": "演示 raise 的地方要用 `try` 接住"},
]
