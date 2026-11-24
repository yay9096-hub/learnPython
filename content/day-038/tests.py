import ast


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def _defaults(fn):
    """返回 {参数名: 默认值}，只取能静态求值的。"""
    out = {}
    args = fn.args.args
    defaults = fn.args.defaults
    named = [a.arg for a in args[len(args) - len(defaults):]]
    for name, node in zip(named, defaults):
        try:
            out[name] = ast.literal_eval(node)
        except Exception:
            out[name] = "<非字面量>"
    return out


def create_signature(ctx):
    fn = _funcs(ctx).get("create_role")
    if fn is None:
        return False
    names = [a.arg for a in fn.args.args]
    if names[:6] != ["name", "hp", "mp", "atk", "element", "level"]:
        return False
    d = _defaults(fn)
    return (d.get("hp") == 100 and d.get("mp") == 50 and d.get("atk") == 30
            and d.get("element") == "无" and d.get("level") == 1)


def create_returns_dict(ctx):
    fn = ctx["ns"].get("create_role")
    if not callable(fn):
        return False
    r = fn("测试者")
    if not isinstance(r, dict):
        return False
    return (r.get("name") == "测试者" and r.get("hp") == 100
            and r.get("mp") == 50 and r.get("atk") == 30
            and r.get("element") == "无" and r.get("level") == 1)


def create_overrides(ctx):
    fn = ctx["ns"].get("create_role")
    if not callable(fn):
        return False
    r = fn("樱", 340, 180, 88, "火", 12)
    ok1 = r.get("hp") == 340 and r.get("element") == "火" and r.get("level") == 12
    r2 = fn("琉璃", element="水", level=8)
    ok2 = (r2.get("element") == "水" and r2.get("level") == 8
           and r2.get("hp") == 100 and r2.get("atk") == 30)
    return ok1 and ok2


def show_signature(ctx):
    fn = _funcs(ctx).get("show_role")
    if fn is None:
        return False
    names = [a.arg for a in fn.args.args]
    d = _defaults(fn)
    return (names[:3] == ["role", "width", "char"]
            and d.get("width") == 20 and d.get("char") == "█")


def _capture(fn, *a, **kw):
    import io
    import sys
    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        fn(*a, **kw)
    except Exception:
        return None
    finally:
        sys.stdout = real
    return buf.getvalue()


def show_respects_char(ctx):
    fn = ctx["ns"].get("show_role")
    mk = ctx["ns"].get("create_role")
    if not callable(fn) or not callable(mk):
        return False
    out = _capture(fn, mk("测试者", 400), width=10, char="@")
    return out is not None and "@" in out


def add_skill_none_default(ctx):
    """默认值必须是 None，不能是可变的 [] —— 这是今天的重点坑。"""
    fn = _funcs(ctx).get("add_skill")
    if fn is None:
        return False
    d = _defaults(fn)
    return "skills" in d and d["skills"] is None


def add_skill_works(ctx):
    fn = ctx["ns"].get("add_skill")
    mk = ctx["ns"].get("create_role")
    if not callable(fn) or not callable(mk):
        return False
    r = mk("测试者")
    try:
        fn(r, "技能A")
        fn(r, "技能B")
    except Exception:
        return False
    sk = r.get("skills")
    return isinstance(sk, list) and "技能A" in sk and "技能B" in sk


def no_shared_state(ctx):
    """两个不同角色的技能不能串台（可变默认值的经典症状）。"""
    fn = ctx["ns"].get("add_skill")
    mk = ctx["ns"].get("create_role")
    if not callable(fn) or not callable(mk):
        return False
    a = mk("甲")
    b = mk("乙")
    try:
        fn(a, "只属于甲")
    except Exception:
        return False
    return "只属于甲" not in (b.get("skills") or [])


def used_defaults(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "create_role":
            if len(n.args) == 1 and not n.keywords:
                return True
    return False


def used_keywords(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "create_role":
            if n.keywords:
                return True
    return False


def show_called_thrice(ctx):
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "show_role")
    return n >= 3


CHECKS = [
    {
        "id": "create-sig",
        "desc": "create_role 的参数和默认值都对",
        "type": "custom", "fn": "create_signature",
        "fail": "签名照抄：`create_role(name, hp=100, mp=50, atk=30, element=\"无\", level=1)`",
    },
    {
        "id": "create-dict",
        "desc": "只给名字时全部用默认值",
        "type": "custom", "fn": "create_returns_dict",
        "fail": "`create_role(\"测试者\")` 要返回字典，且 hp=100 / mp=50 / atk=30 / "
                "element=无 / level=1",
    },
    {
        "id": "create-override",
        "desc": "给了值就用给的值",
        "type": "custom", "fn": "create_overrides",
        "fail": "既要支持全部按顺序给，也要支持 "
                "`create_role(\"琉璃\", element=\"水\", level=8)` 这种只改两项的写法",
    },
    {
        "id": "show-sig",
        "desc": "show_role 的默认值对",
        "type": "custom", "fn": "show_signature",
        "fail": "签名照抄：`show_role(role, width=20, char=\"█\")`",
    },
    {
        "id": "show-char",
        "desc": "换了 char 血条真的会变",
        "type": "custom", "fn": "show_respects_char",
        "fail": "血条要用参数里的 `char` 画，不能写死成 █",
    },
    {
        "id": "none-default",
        "desc": "add_skill 用 None 当默认值",
        "type": "custom", "fn": "add_skill_none_default",
        "fail": "⚠️ 今天的重点坑：默认值**不能写 `[]`**，必须写 `skills=None`，"
                "进函数后再 `if skills is None:`",
    },
    {
        "id": "skill-works",
        "desc": "加技能真的生效",
        "type": "custom", "fn": "add_skill_works",
        "fail": "连加两个技能后，角色的 `skills` 里应该有这两个",
    },
    {
        "id": "no-shared",
        "desc": "两个角色的技能不串台",
        "type": "custom", "fn": "no_shared_state",
        "fail": "给甲加的技能跑到乙身上了 —— 这正是可变默认值 `[]` 的经典症状",
    },
    {
        "id": "use-default",
        "desc": "主流程有「只给名字」的调用",
        "type": "custom", "fn": "used_defaults",
        "fail": "造一个路人：`create_role(\"路人甲\")`，其余全用默认值",
    },
    {
        "id": "use-keyword",
        "desc": "主流程用了关键字参数",
        "type": "custom", "fn": "used_keywords",
        "fail": "用 `create_role(\"月见琉璃\", element=\"水\", level=8)` 这种点名写法造一个",
    },
    {
        "id": "show-thrice",
        "desc": "show_role 至少调用 3 次",
        "type": "custom", "fn": "show_called_thrice",
        "fail": "三个角色各打印一次，其中一次改 `width` 或 `char`",
    },
]
