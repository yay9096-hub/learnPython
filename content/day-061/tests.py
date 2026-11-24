import ast


def _methods_of(ctx, cls_name):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ClassDef) and n.name == cls_name:
            return {f.name: f for f in n.body if isinstance(f, ast.FunctionDef)}
    return {}


def role_dunders(ctx):
    fns = _methods_of(ctx, "Role")
    return all(m in fns for m in ["__str__", "__repr__", "__eq__", "__lt__"])


def team_dunders(ctx):
    fns = _methods_of(ctx, "Team")
    return all(m in fns for m in ["__str__", "__len__", "__contains__"])


def str_works(ctx):
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    r = R("测试者", 340, 88)
    s = str(r)
    return (isinstance(s, str) and "测试者" in s
            and "340" in s and "88" in s and "object at" not in s)


def repr_works(ctx):
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    r = R("测试者", 340, 88)
    s = repr(r)
    return (isinstance(s, str) and "Role" in s
            and "测试者" in s and "340" in s and "object at" not in s)


def repr_differs(ctx):
    """__repr__ 和 __str__ 应该给出不同的样子。"""
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    r = R("测试者", 340, 88)
    return str(r) != repr(r)


def eq_by_name(ctx):
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    a = R("星野樱", 340, 88)
    b = R("星野樱", 100, 20)
    c = R("月见琉璃", 340, 88)
    return (a == b) is True and (a == c) is False


def eq_guards_type(ctx):
    """跟非 Role 比较不能崩，要返回 False。"""
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    a = R("星野樱", 340, 88)
    try:
        return (a == "星野樱") is False and (a == 123) is False
    except Exception:
        return False


def eq_makes_in_work(ctx):
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    team = [R("星野樱", 340), R("月见琉璃", 280)]
    return (R("星野樱") in team) is True and (R("路人甲") in team) is False


def lt_sorts(ctx):
    """有了 __lt__，sorted / max / min 都不用 key。"""
    R = ctx["ns"].get("Role")
    if not isinstance(R, type):
        return False
    roles = [R("甲", 100, 88), R("乙", 100, 110), R("丙", 100, 72)]
    try:
        ordered = sorted(roles)
        best = max(roles)
        worst = min(roles)
    except Exception:
        return False
    return ([r.atk for r in ordered] == [72, 88, 110]
            and best.atk == 110 and worst.atk == 72)


def team_len(ctx):
    ns = ctx["ns"]
    T, R = ns.get("Team"), ns.get("Role")
    if not isinstance(T, type) or not isinstance(R, type):
        return False
    t = T("测试队")
    if len(t) != 0:
        return False
    t.add(R("甲"))
    t.add(R("乙"))
    return len(t) == 2


def team_contains(ctx):
    ns = ctx["ns"]
    T, R = ns.get("Team"), ns.get("Role")
    if not isinstance(T, type) or not isinstance(R, type):
        return False
    t = T("测试队")
    t.add(R("星野樱"))
    return ("星野樱" in t) is True and ("路人甲" in t) is False


def team_truthiness(ctx):
    """有了 __len__，空队伍在 if 里就是 False。"""
    ns = ctx["ns"]
    T, R = ns.get("Team"), ns.get("Role")
    if not isinstance(T, type) or not isinstance(R, type):
        return False
    empty = T("空队")
    full = T("满队")
    full.add(R("甲"))
    return (not empty) is True and bool(full) is True


def team_str(ctx):
    ns = ctx["ns"]
    T, R = ns.get("Team"), ns.get("Role")
    if not isinstance(T, type) or not isinstance(R, type):
        return False
    t = T("樱之队")
    t.add(R("甲"))
    s = str(t)
    return "樱之队" in s and "object at" not in s


def no_status_calls(ctx):
    """主流程不许再用 .status()，那是 print(对象) 该干的事。"""
    return ".status()" not in ctx["code"]


def no_members_in_main(ctx):
    """主流程里不许出现 .members —— 特殊方法就是用来藏它的。"""
    src = ctx["code"]
    # 类定义里的 self.members 不算
    lines = [l for l in src.splitlines()
             if ".members" in l and "self.members" not in l]
    return len(lines) == 0


def sorted_without_key(ctx):
    """sorted / max / min 都不带 key。"""
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) in ("sorted", "max", "min"):
            if any(k.arg == "key" for k in n.keywords):
                return False
    return True


def uses_sorted_max_min(ctx):
    names = set()
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) in ("sorted", "max", "min"):
            names.add(n.func.id)
    return {"sorted", "max", "min"} <= names


def printed_object_directly(ctx):
    """输出里要有 __str__ 的痕迹，而不是 <object at ...>。"""
    out = ctx["stdout"]
    return "object at" not in out and "星野樱" in out


def printed_repr_list(ctx):
    """打印列表时用的是 __repr__。"""
    return "Role(" in ctx["stdout"]


def demo_eq(ctx):
    out = ctx["stdout"]
    return "True" in out and "False" in out


def demo_empty_team(ctx):
    return "空" in ctx["stdout"]


CHECKS = [
    {"id": "role-dunders", "desc": "Role 有四个特殊方法",
     "type": "custom", "fn": "role_dunders",
     "fail": "`__str__` / `__repr__` / `__eq__` / `__lt__`"},
    {"id": "team-dunders", "desc": "Team 有三个特殊方法",
     "type": "custom", "fn": "team_dunders",
     "fail": "`__str__` / `__len__` / `__contains__`"},
    {"id": "str", "desc": "print(角色) 显示漂亮卡片",
     "type": "custom", "fn": "str_works",
     "fail": "`__str__` 要返回含名字、HP、ATK 的一行文字"},
    {"id": "repr", "desc": "__repr__ 像能重建对象的代码",
     "type": "custom", "fn": "repr_works",
     "fail": "返回 `Role('星野樱', 340, 88)` 这种样子，"
             "可以用 `{self.name!r}` 让字符串自带引号"},
    {"id": "repr-diff", "desc": "__str__ 和 __repr__ 不一样",
     "type": "custom", "fn": "repr_differs",
     "fail": "一个给用户看（漂亮），一个给程序员看（准确）"},
    {"id": "eq", "desc": "同名角色相等",
     "type": "custom", "fn": "eq_by_name",
     "fail": "`return self.name == other.name`"},
    {"id": "eq-guard", "desc": "跟非 Role 比较返回 False",
     "type": "custom", "fn": "eq_guards_type",
     "fail": "⚠️ 开头要 `if not isinstance(other, Role): return False`，"
             "否则跟字符串比会 AttributeError"},
    {"id": "eq-in", "desc": "__eq__ 让 in 也变聪明",
     "type": "custom", "fn": "eq_makes_in_work",
     "fail": "`Role('星野樱') in 角色列表` 应该是 True —— "
             "`in` 内部用的就是 `==`"},
    {"id": "lt", "desc": "__lt__ 让排序不用 key",
     "type": "custom", "fn": "lt_sorts",
     "fail": "`return self.atk < other.atk`，"
             "之后 `sorted` / `max` / `min` 全都能直接用"},
    {"id": "len", "desc": "len(team) 返回人数",
     "type": "custom", "fn": "team_len",
     "fail": "`return len(self.members)`"},
    {"id": "contains", "desc": "「名字 in team」可用",
     "type": "custom", "fn": "team_contains",
     "fail": "`__contains__` 里遍历成员比名字"},
    {"id": "truthy", "desc": "空队伍在 if 里是 False",
     "type": "custom", "fn": "team_truthiness",
     "fail": "有了 `__len__`，Python 会用「长度是不是 0」判断真假 —— 不用额外写"},
    {"id": "team-str", "desc": "print(team) 显示队名和人数",
     "type": "custom", "fn": "team_str",
     "fail": "`__str__` 返回带队名的文字"},
    {"id": "no-status", "desc": "主流程不再用 .status()",
     "type": "custom", "fn": "no_status_calls",
     "fail": "直接 `print(角色)` 就行 —— 这正是 `__str__` 的意义"},
    {"id": "no-members", "desc": "主流程不碰 .members",
     "type": "custom", "fn": "no_members_in_main",
     "fail": "用 `len(team)` 和 `\"名字\" in team`，"
             "别写 `team.members` —— 特殊方法就是用来藏它的"},
    {"id": "no-key", "desc": "sorted/max/min 都不写 key=",
     "type": "custom", "fn": "sorted_without_key",
     "fail": "有了 `__lt__` 就不需要 `key=` 了"},
    {"id": "uses-three", "desc": "三个内置函数都用了",
     "type": "custom", "fn": "uses_sorted_max_min",
     "fail": "`sorted()` 排序、`max()` 找最强、`min()` 找最弱"},
    {"id": "printed", "desc": "直接打印了对象",
     "type": "custom", "fn": "printed_object_directly",
     "fail": "输出里不该出现 `<... object at 0x...>`"},
    {"id": "repr-list", "desc": "打印列表时看到 __repr__",
     "type": "custom", "fn": "printed_repr_list",
     "fail": "`print(roles)` 打印整个列表 —— 里面用的是 `__repr__`"},
    {"id": "demo-eq", "desc": "演示了相等和不等",
     "type": "custom", "fn": "demo_eq",
     "fail": "同名相等、异名不等、跟字符串比 False，三种都演示一下"},
    {"id": "demo-empty", "desc": "演示了空队伍的真假判断",
     "type": "custom", "fn": "demo_empty_team",
     "fail": "造一个空队伍，用 `if not empty:` 验证它是 False"},
]
