import ast


def _funcs_in_class(ctx, cls_name):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ClassDef) and n.name == cls_name:
            return {f.name: f for f in n.body if isinstance(f, ast.FunctionDef)}
    return {}


def has_docstring(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ClassDef) and n.name == "Role":
            return ast.get_docstring(n) is not None
    return False


def init_signature(ctx):
    """__init__ 的参数和默认值要照抄。"""
    fn = _funcs_in_class(ctx, "Role").get("__init__")
    if fn is None:
        return False
    names = [a.arg for a in fn.args.args]
    if names[:6] != ["self", "name", "hp", "mp", "atk", "element"]:
        return False
    defaults = fn.args.defaults
    try:
        vals = [ast.literal_eval(d) for d in defaults]
    except Exception:
        return False
    return vals == [100, 50, 30, "无"]


def only_init(ctx):
    """今天只写 __init__，别的方法明天再学。"""
    fns = _funcs_in_class(ctx, "Role")
    return list(fns.keys()) == ["__init__"]


def defaults_work(ctx):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("测试者")
    return (r.name == "测试者" and r.hp == 100 and r.mp == 50
            and r.atk == 30 and r.element == "无")


def max_hp_and_alive(ctx):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("测试者", 340)
    return (getattr(r, "max_hp", None) == 340
            and getattr(r, "alive", None) is True)


def all_args_work(ctx):
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    r = cls("樱", 340, 180, 88, "火")
    ok1 = (r.hp == 340 and r.mp == 180 and r.atk == 88 and r.element == "火")
    r2 = cls("琉璃", element="水", atk=95)
    ok2 = (r2.element == "水" and r2.atk == 95 and r2.hp == 100)
    return ok1 and ok2


def instances_independent(ctx):
    """两个实例的属性互不影响 —— 今天的核心概念。"""
    cls = ctx["ns"].get("Role")
    if not isinstance(cls, type):
        return False
    a = cls("甲", 100)
    b = cls("乙", 100)
    a.hp = 50
    return b.hp == 100


def four_created(ctx):
    """主流程里造了至少 4 个 Role。"""
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "Role")
    return n >= 4


def used_defaults_and_keywords(ctx):
    """既有只给名字的，也有用关键字参数的。"""
    only_name = False
    with_kw = False
    for x in ast.walk(ctx["tree"]):
        if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "Role":
            if len(x.args) == 1 and not x.keywords:
                only_name = True
            if x.keywords:
                with_kw = True
    return only_name and with_kw


def uses_dot_access(ctx):
    """用点号取属性，不是方括号。"""
    return any(isinstance(n, ast.Attribute) for n in ast.walk(ctx["tree"]))


def listed_all(ctx):
    out = ctx["stdout"]
    return all(x in out for x in ["路人甲", "星野樱", "月见琉璃", "水城凛"])


def used_sum(ctx):
    return any(isinstance(n, ast.Call) and getattr(n.func, "id", None) == "sum"
               for n in ast.walk(ctx["tree"]))


def used_max_key(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "max":
            if any(k.arg == "key" for k in n.keywords):
                return True
    return False


def strongest_shown(ctx):
    """攻击最强的是水城凛（110）。"""
    import re
    return re.search(r"水城凛[^\n]*110|110[^\n]*水城凛", ctx["stdout"]) is not None


def damage_applied(ctx):
    """星野樱掉了 100 血，输出里应该出现 240。"""
    return "240" in ctx["stdout"]


CHECKS = [
    {"id": "class", "desc": "定义了 Role 类",
     "type": "class_defined", "name": "Role",
     "fail": "`class Role:` —— 类名首字母大写是惯例"},
    {"id": "doc", "desc": "类有 docstring",
     "type": "custom", "fn": "has_docstring",
     "fail": "`class Role:` 下面第一行写一句三引号说明"},
    {"id": "sig", "desc": "__init__ 参数和默认值都对",
     "type": "custom", "fn": "init_signature",
     "fail": "签名照抄：`def __init__(self, name, hp=100, mp=50, atk=30, element=\"无\"):`。"
             "⚠️ `self` 必须是第一个参数"},
    {"id": "only-init", "desc": "今天只写 __init__",
     "type": "custom", "fn": "only_init",
     "fail": "方法明天才学，今天类里只放 `__init__` 一个",
     },
    {"id": "defaults", "desc": "只给名字时用默认值",
     "type": "custom", "fn": "defaults_work",
     "fail": "`Role(\"测试者\")` 之后 hp=100 / mp=50 / atk=30 / element=无"},
    {"id": "extra-attrs", "desc": "max_hp 和 alive 设对了",
     "type": "custom", "fn": "max_hp_and_alive",
     "fail": "`self.max_hp = hp`（等于初始血量）、`self.alive = True`。"
             "**属性不一定都来自参数**"},
    {"id": "all-args", "desc": "全参数和关键字参数都能用",
     "type": "custom", "fn": "all_args_work",
     "fail": "既要支持 `Role(\"樱\", 340, 180, 88, \"火\")`，"
             "也要支持 `Role(\"琉璃\", element=\"水\", atk=95)`"},
    {"id": "independent", "desc": "两个实例互不影响",
     "type": "custom", "fn": "instances_independent",
     "fail": "改一个角色的 hp 不该影响另一个 —— "
             "属性要写成 `self.hp = hp`，存在**每个对象自己**身上"},
    {"id": "four", "desc": "造了至少 4 个角色",
     "type": "custom", "fn": "four_created",
     "fail": "主流程里 `Role(...)` 至少 4 次"},
    {"id": "styles", "desc": "用了默认值和关键字参数两种写法",
     "type": "custom", "fn": "used_defaults_and_keywords",
     "fail": "一个只给名字 `Role(\"路人甲\")`，"
             "一个用关键字 `Role(\"月见琉璃\", element=\"水\")`"},
    {"id": "dot", "desc": "用点号取属性",
     "type": "custom", "fn": "uses_dot_access",
     "fail": "对象用 `r.name`，不是 `r[\"name\"]` —— 那是字典的写法"},
    {"id": "listed", "desc": "四个角色都打印了",
     "type": "custom", "fn": "listed_all",
     "fail": "装进列表遍历打印，一行一个"},
    {"id": "sum", "desc": "用 sum 算了总血量",
     "type": "custom", "fn": "used_sum",
     "fail": "`sum(r.hp for r in team)` —— 第三章的本事对对象列表一样管用"},
    {"id": "max", "desc": "用 max(key=...) 找最强",
     "type": "custom", "fn": "used_max_key",
     "fail": "`max(team, key=lambda r: r.atk)`"},
    {"id": "strongest", "desc": "找对了最强的角色",
     "type": "custom", "fn": "strongest_shown",
     "fail": "攻击力最强的是水城凛（110）"},
    {"id": "damage", "desc": "改属性后只有那个角色变了",
     "type": "custom", "fn": "damage_applied",
     "fail": "星野樱 340 扣 100 应该剩 **240**，改完再打印全队确认别人没变"},
]
