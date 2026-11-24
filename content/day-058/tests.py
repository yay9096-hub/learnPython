import ast

METHODS = ["add", "size", "find", "remove", "total_hp", "avg_atk",
           "alive_members", "is_wiped", "strongest", "heal_all",
           "damage_all", "report"]


def _team_methods(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ClassDef) and n.name == "Team":
            return {f.name: f for f in n.body if isinstance(f, ast.FunctionDef)}
    return {}


def _build(ctx):
    """造一支固定的测试队伍。"""
    Role = ctx["ns"].get("Role")
    Team = ctx["ns"].get("Team")
    if not isinstance(Role, type) or not isinstance(Team, type):
        return None
    t = Team("测试队")
    t.add(Role("甲", 100, 40))
    t.add(Role("乙", 200, 60))
    t.add(Role("丙", 50, 20))
    return t


def all_methods(ctx):
    fns = _team_methods(ctx)
    return all(m in fns for m in METHODS)


def members_is_list(ctx):
    Team = ctx["ns"].get("Team")
    if not isinstance(Team, type):
        return False
    t = Team("空队")
    return isinstance(getattr(t, "members", None), list) and len(t.members) == 0


def add_and_size(ctx):
    t = _build(ctx)
    if t is None:
        return False
    return t.size() == 3


def add_returns_count(ctx):
    Role = ctx["ns"].get("Role")
    Team = ctx["ns"].get("Team")
    if not isinstance(Role, type) or not isinstance(Team, type):
        return False
    t = Team("测试")
    a = t.add(Role("甲"))
    b = t.add(Role("乙"))
    return a == 1 and b == 2


def find_ok(ctx):
    t = _build(ctx)
    if t is None:
        return False
    m = t.find("乙")
    return m is not None and m.hp == 200 and t.find("路人") is None


def remove_ok(ctx):
    t = _build(ctx)
    if t is None:
        return False
    ok = t.remove("乙")
    bad = t.remove("路人")
    return ok is True and bad is False and t.size() == 2 and t.find("乙") is None


def remove_reuses_find(ctx):
    """remove 里要调 self.find，不要把查找逻辑写两遍。"""
    fn = _team_methods(ctx).get("remove")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "find":
                return True
    return False


def total_hp_ok(ctx):
    t = _build(ctx)
    return t is not None and t.total_hp() == 350


def avg_atk_ok(ctx):
    t = _build(ctx)
    if t is None:
        return False
    return abs(t.avg_atk() - 40.0) < 0.05


def avg_atk_empty_safe(ctx):
    Team = ctx["ns"].get("Team")
    if not isinstance(Team, type):
        return False
    try:
        return Team("空队").avg_atk() == 0
    except Exception:
        return False


def alive_and_wiped(ctx):
    t = _build(ctx)
    if t is None:
        return False
    if len(t.alive_members()) != 3 or t.is_wiped():
        return False
    t.damage_all(9999)
    return len(t.alive_members()) == 0 and t.is_wiped() is True


def strongest_ok(ctx):
    t = _build(ctx)
    if t is None:
        return False
    best = t.strongest()
    if best is None or best.name != "乙":
        return False
    Team = ctx["ns"].get("Team")
    return Team("空队").strongest() is None


def damage_all_total(ctx):
    """丙只有 50 血，扣 100 只能扣 50 —— 总数要是实际值。"""
    t = _build(ctx)
    if t is None:
        return False
    got = t.damage_all(100)
    return got == 100 + 100 + 50


def heal_all_total(ctx):
    """满血的治不进去，倒下的治不了 —— 总数要反映实际。"""
    t = _build(ctx)
    if t is None:
        return False
    t.damage_all(60)          # 甲 40 / 乙 140 / 丙 0（倒下）
    got = t.heal_all(30)      # 甲 +30 / 乙 +30 / 丙 0
    return got == 60


def team_delegates(ctx):
    """Team 的方法里不许直接改 m.hp，要调 Role 的方法。"""
    fns = _team_methods(ctx)
    for name in ["heal_all", "damage_all"]:
        fn = fns.get(name)
        if fn is None:
            return False
        for n in ast.walk(fn):
            if isinstance(n, ast.Assign):
                for tgt in n.targets:
                    if isinstance(tgt, ast.Attribute) and tgt.attr == "hp":
                        return False
        called = {n.func.attr for n in ast.walk(fn)
                  if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        if not ({"heal", "take_damage"} & called):
            return False
    return True


def four_members(ctx):
    """主流程里造了至少 4 个角色。"""
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "Role")
    return n >= 4


def someone_died(ctx):
    return "倒下" in ctx["stdout"]


def reported(ctx):
    out = ctx["stdout"]
    return "总血量" in out and "平均攻击" in out


def healed_shown(ctx):
    return "回复" in ctx["stdout"]


def removed_shown(ctx):
    out = ctx["stdout"]
    return "True" in out and "False" in out


def strongest_shown(ctx):
    return "最强" in ctx["stdout"]


CHECKS = [
    {"id": "methods", "desc": "Team 的十二个方法都定义了",
     "type": "class_defined", "name": "Team", "methods": METHODS,
     "fail": "对照任务表检查方法名，一个都不能少"},
    {"id": "members", "desc": "members 初始是空列表",
     "type": "custom", "fn": "members_is_list",
     "fail": "`__init__` 里 `self.members = []`"},
    {"id": "add", "desc": "add 能加成员且 size 正确",
     "type": "custom", "fn": "add_and_size",
     "fail": "`self.members.append(role)`"},
    {"id": "add-return", "desc": "add 返回现在的人数",
     "type": "custom", "fn": "add_returns_count",
     "fail": "加完 `return len(self.members)`"},
    {"id": "find", "desc": "find 找到 / 找不到都正确",
     "type": "custom", "fn": "find_ok",
     "fail": "找到就立刻 return，跑完还没有就 `return None`"},
    {"id": "remove", "desc": "remove 返回成功与否",
     "type": "custom", "fn": "remove_ok",
     "fail": "移除成功返回 `True`，没这个人返回 `False`"},
    {"id": "remove-reuse", "desc": "remove 复用了 find",
     "type": "custom", "fn": "remove_reuses_find",
     "fail": "`member = self.find(name)` —— 别把查找逻辑写两遍"},
    {"id": "total", "desc": "total_hp 算对（350）",
     "type": "custom", "fn": "total_hp_ok",
     "fail": "100 + 200 + 50 = 350"},
    {"id": "avg", "desc": "avg_atk 算对（40.0）",
     "type": "custom", "fn": "avg_atk_ok",
     "fail": "(40 + 60 + 20) / 3 = 40.0，记得 `round(..., 1)`"},
    {"id": "avg-empty", "desc": "空队求平均不崩",
     "type": "custom", "fn": "avg_atk_empty_safe",
     "fail": "空队要先 `return 0`，别除以零"},
    {"id": "alive", "desc": "alive_members 和 is_wiped 正确",
     "type": "custom", "fn": "alive_and_wiped",
     "fail": "全员倒下时 `is_wiped()` 要返回 True"},
    {"id": "strongest", "desc": "strongest 找对且空队返回 None",
     "type": "custom", "fn": "strongest_ok",
     "fail": "返回攻击力最高的那个**对象**；空队返回 `None`"},
    {"id": "dmg-total", "desc": "damage_all 返回实际总扣血",
     "type": "custom", "fn": "damage_all_total",
     "fail": "只有 50 血的成员挨 100 点，实际只扣 50。"
             "把每个 `take_damage` 的**返回值**加起来"},
    {"id": "heal-total", "desc": "heal_all 返回实际总回血",
     "type": "custom", "fn": "heal_all_total",
     "fail": "满血的治不进去、倒下的治不了 —— 总数要反映实际发生的"},
    {"id": "delegate", "desc": "Team 把具体操作委托给 Role",
     "type": "custom", "fn": "team_delegates",
     "fail": "⚠️ `heal_all` / `damage_all` 里**不许直接写 `m.hp = ...`**，"
             "要调 `m.heal(...)` 和 `m.take_damage(...)` —— "
             "规则只写在 Role 里一处"},
    {"id": "four", "desc": "队伍至少 4 人",
     "type": "custom", "fn": "four_members",
     "fail": "主流程里造至少 4 个 Role 加进队伍"},
    {"id": "report", "desc": "报告含总血量和平均攻击",
     "type": "custom", "fn": "reported",
     "fail": "`report()` 要打印人数、存活数、总血量、平均攻击和每个成员"},
    {"id": "died", "desc": "全体伤害让至少一人倒下",
     "type": "custom", "fn": "someone_died",
     "fail": "`damage_all` 的伤害要够大，至少打倒一个成员"},
    {"id": "healed", "desc": "打印了实际总回复量",
     "type": "custom", "fn": "healed_shown",
     "fail": "`heal_all` 的返回值要打印出来"},
    {"id": "removed", "desc": "演示了移除成功和失败",
     "type": "custom", "fn": "removed_shown",
     "fail": "移除一个存在的（True）和一个不存在的（False），两次都打印"},
    {"id": "best", "desc": "打印了最强成员",
     "type": "custom", "fn": "strongest_shown",
     "fail": "用 `team.strongest()` 拿到对象，再 `.name` 取名字"},
]
