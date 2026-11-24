import ast


def roll_returns_three(ctx):
    fn = ctx["ns"].get("roll_stats")
    if not callable(fn):
        return False
    r = fn(10)
    if not isinstance(r, tuple) or len(r) != 3:
        return False
    return all(isinstance(x, int) for x in r)


def roll_scales(ctx):
    """等级越高整体越强 —— 多跑几次取平均，避开随机波动。"""
    fn = ctx["ns"].get("roll_stats")
    if not callable(fn):
        return False
    low = sum(sum(fn(1)) for _ in range(30)) / 30
    high = sum(sum(fn(20)) for _ in range(30)) / 30
    return high > low * 1.5


def roll_random(ctx):
    fn = ctx["ns"].get("roll_stats")
    if not callable(fn):
        return False
    seen = {fn(5) for _ in range(20)}
    return len(seen) >= 3


def judge_returns_two(ctx):
    fn = ctx["ns"].get("judge_stats")
    if not callable(fn):
        return False
    r = fn(200, 150, 100)
    return isinstance(r, tuple) and len(r) == 2


def judge_ranks(ctx):
    fn = ctx["ns"].get("judge_stats")
    if not callable(fn):
        return False
    a, ta = fn(200, 150, 100)      # 450 -> 优秀
    b, tb = fn(150, 100, 60)       # 310 -> 普通
    c, tc = fn(100, 50, 30)        # 180 -> 偏弱
    d, td = fn(200, 150, 50)       # 400 -> 优秀（边界）
    e, te = fn(150, 100, 50)       # 300 -> 普通（边界）
    return (a == "优秀" and ta == 450 and b == "普通" and tb == 310
            and c == "偏弱" and tc == 180 and d == "优秀" and e == "普通")


def make_role_dict(ctx):
    fn = ctx["ns"].get("make_role")
    if not callable(fn):
        return False
    r = fn("测试者", 5)
    if not isinstance(r, dict):
        return False
    need = ["name", "level", "hp", "mp", "atk", "rank"]
    return all(k in r for k in need) and r["name"] == "测试者" and r["level"] == 5


def make_role_uses_others(ctx):
    """make_role 内部要调用另外两个函数，而不是重写一遍逻辑。"""
    fns = {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}
    fn = fns.get("make_role")
    if fn is None:
        return False
    called = {getattr(n.func, "id", None) for n in ast.walk(fn)
              if isinstance(n, ast.Call)}
    return "roll_stats" in called and "judge_stats" in called


def make_role_consistent(ctx):
    """字典里的 rank 要跟它自己的三围对得上。"""
    mk = ctx["ns"].get("make_role")
    jd = ctx["ns"].get("judge_stats")
    if not callable(mk) or not callable(jd):
        return False
    for _ in range(10):
        r = mk("测试者", 10)
        rank, _total = jd(r["hp"], r["mp"], r["atk"])
        if r["rank"] != rank:
            return False
    return True


def check_name_returns_two(ctx):
    fn = ctx["ns"].get("check_name")
    if not callable(fn):
        return False
    r = fn("星野樱")
    return isinstance(r, tuple) and len(r) == 2 and isinstance(r[0], bool)


def check_name_logic(ctx):
    fn = ctx["ns"].get("check_name")
    if not callable(fn):
        return False
    short_ok, _ = fn("樱")
    long_ok, _ = fn("超级无敌宇宙第一魔法少女")
    good_ok, _ = fn("星野樱")
    edge2, _ = fn("小樱")
    edge8, _ = fn("一二三四五六七八")
    return (short_ok is False and long_ok is False and good_ok is True
            and edge2 is True and edge8 is True)


def unpacked_three(ctx):
    """主流程里有 a, b, c = roll_stats(...) 这样的解包。"""
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Tuple):
            if len(n.targets[0].elts) == 3:
                return True
    return False


def unpacked_two(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Tuple):
            if len(n.targets[0].elts) == 2:
                return True
    return False


def three_roles(ctx):
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "make_role")
    return n >= 3


def names_checked(ctx):
    out = ctx["stdout"]
    return "太短" in out and "太长" in out


CHECKS = [
    {
        "id": "roll-three",
        "desc": "roll_stats 返回三个整数",
        "type": "custom", "fn": "roll_returns_three",
        "fail": "`return hp, mp, atk` —— 逗号隔开就是返回多个",
    },
    {
        "id": "roll-random",
        "desc": "属性是随机的",
        "type": "custom", "fn": "roll_random",
        "fail": "用 `random.randint(...)` 生成，不要写死数字",
    },
    {
        "id": "roll-scale",
        "desc": "等级越高属性越强",
        "type": "custom", "fn": "roll_scales",
        "fail": "公式里要带上 level，比如 `hp = random.randint(50, 100) + level * 20`",
    },
    {
        "id": "judge-two",
        "desc": "judge_stats 返回两个值",
        "type": "custom", "fn": "judge_returns_two",
        "fail": "`return rank, total` —— 评级和总和一起交回来",
    },
    {
        "id": "judge-rank",
        "desc": "三档评级都对（含边界）",
        "type": "custom", "fn": "judge_ranks",
        "fail": "总和 400 要算「优秀」、300 要算「普通」—— 用 `>=`，"
                "而且分档要从高到低写",
    },
    {
        "id": "role-dict",
        "desc": "make_role 返回带六个字段的字典",
        "type": "custom", "fn": "make_role_dict",
        "fail": "要含 name / level / hp / mp / atk / rank 六个键",
    },
    {
        "id": "role-reuse",
        "desc": "make_role 内部调用了另外两个函数",
        "type": "custom", "fn": "make_role_uses_others",
        "fail": "在 `make_role` 里调 `roll_stats` 和 `judge_stats`，"
                "别把逻辑再抄一遍 —— 小零件拼大零件",
    },
    {
        "id": "role-consistent",
        "desc": "字典里的评级跟三围对得上",
        "type": "custom", "fn": "make_role_consistent",
        "fail": "rank 要用**这个角色自己的**三围算出来，不能随便填",
    },
    {
        "id": "name-two",
        "desc": "check_name 返回 (布尔, 说明)",
        "type": "custom", "fn": "check_name_returns_two",
        "fail": "`return False, \"名字太短了\"` —— 结果和原因一起交回来",
    },
    {
        "id": "name-logic",
        "desc": "名字长度判断正确（2~8 合法）",
        "type": "custom", "fn": "check_name_logic",
        "fail": "长度小于 2 或大于 8 都不合法；2 和 8 本身**算合法**",
    },
    {
        "id": "unpack3",
        "desc": "主流程用三变量解包接住了",
        "type": "custom", "fn": "unpacked_three",
        "fail": "`hp, mp, atk = roll_stats(10)` —— 左边写三个变量",
    },
    {
        "id": "unpack2",
        "desc": "主流程用两变量解包接住了",
        "type": "custom", "fn": "unpacked_two",
        "fail": "`rank, total = judge_stats(hp, mp, atk)`",
    },
    {
        "id": "three-roles",
        "desc": "造了至少 3 个角色",
        "type": "custom", "fn": "three_roles",
        "fail": "用 `make_role` 造三个不同的角色，再遍历打印",
    },
    {
        "id": "name-output",
        "desc": "三种名字的校验说明都打印了",
        "type": "custom", "fn": "names_checked",
        "fail": "验一个太短的、一个太长的、一个正常的，把说明文字都打出来",
    },
]
