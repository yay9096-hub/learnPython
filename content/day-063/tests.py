import ast
import json
import os

METHODS = ["feed", "sleep", "play", "tick", "is_hungry",
           "stage", "to_dict", "from_dict", "__str__"]

SETUP = """
import os
if os.path.exists("宠物存档.json"):
    os.remove("宠物存档.json")
"""


def _pet_methods(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.ClassDef) and n.name == "Pet":
            return {f.name: f for f in n.body if isinstance(f, ast.FunctionDef)}
    return {}


def _new(ctx, name="测试宠"):
    P = ctx["ns"].get("Pet")
    if not isinstance(P, type):
        return None
    try:
        return P(name)
    except Exception:
        return None


def init_defaults(ctx):
    p = _new(ctx)
    if p is None:
        return False
    return (p.hunger == 50 and p.energy == 50 and p.mood == 50
            and p.age == 0 and p.alive is True)


def feed_clamps(ctx):
    """喂太多饥饿不能变负，心情不能超 100。"""
    p = _new(ctx)
    if p is None:
        return False
    got = p.feed(999)
    if p.hunger != 0 or got != 50:
        return False
    p.mood = 98
    p.feed(10)
    return p.mood == 100


def feed_returns_actual(ctx):
    p = _new(ctx)
    if p is None:
        return False
    return p.feed(20) == 20


def sleep_effects(ctx):
    p = _new(ctx)
    if p is None:
        return False
    p.sleep(2)
    return p.energy == 90 and p.hunger == 70 and p.age == 2


def sleep_clamps(ctx):
    p = _new(ctx)
    if p is None:
        return False
    p.sleep(10)
    return p.energy == 100 and p.hunger == 100


def play_blocked_when_tired(ctx):
    p = _new(ctx)
    if p is None:
        return False
    p.energy = 10
    before_mood = p.mood
    got = p.play()
    return got is False and p.mood == before_mood and p.energy == 10


def play_works(ctx):
    p = _new(ctx)
    if p is None:
        return False
    got = p.play()
    return got is True and p.energy == 35 and p.mood == 65 and p.hunger == 60


def tick_effects(ctx):
    p = _new(ctx)
    if p is None:
        return False
    p.tick()
    return p.hunger == 58 and p.energy == 45 and p.age == 1


def tick_starving_hurts_mood(ctx):
    """饿满了会掉心情。"""
    p = _new(ctx)
    if p is None:
        return False
    p.hunger = 95
    p.mood = 50
    p.tick()
    return p.hunger == 100 and p.mood == 30


def tick_can_kill(ctx):
    """心情和精力都归零就不再健康。"""
    p = _new(ctx)
    if p is None:
        return False
    p.mood = 0
    p.energy = 0
    p.tick()
    return p.alive is False


def is_hungry_ok(ctx):
    p = _new(ctx)
    if p is None:
        return False
    p.hunger = 70
    if p.is_hungry():
        return False
    p.hunger = 71
    return p.is_hungry() is True


def stage_ok(ctx):
    p = _new(ctx)
    if p is None:
        return False
    p.age = 0
    if p.stage() != "幼年":
        return False
    p.age = 9
    if p.stage() != "幼年":
        return False
    p.age = 10
    if p.stage() != "少年":
        return False
    p.age = 29
    if p.stage() != "少年":
        return False
    p.age = 30
    return p.stage() == "成年"


def to_dict_ok(ctx):
    p = _new(ctx, "小樱")
    if p is None:
        return False
    d = p.to_dict()
    if not isinstance(d, dict):
        return False
    need = ["name", "species", "hunger", "energy", "mood", "age", "alive"]
    if not all(k in d for k in need):
        return False
    try:
        json.dumps(d, ensure_ascii=False)
    except Exception:
        return False
    return d["name"] == "小樱"


def from_dict_is_classmethod(ctx):
    """from_dict 要用 @classmethod 装饰。"""
    fn = _pet_methods(ctx).get("from_dict")
    if fn is None:
        return False
    for dec in fn.decorator_list:
        if getattr(dec, "id", None) == "classmethod":
            return True
    return False


def roundtrip_ok(ctx):
    """to_dict -> from_dict 之后所有状态一致。"""
    P = ctx["ns"].get("Pet")
    p = _new(ctx, "小樱")
    if p is None or not isinstance(P, type):
        return False
    p.hunger = 33
    p.energy = 77
    p.mood = 12
    p.age = 42
    back = P.from_dict(p.to_dict())
    return (back.name == "小樱" and back.hunger == 33 and back.energy == 77
            and back.mood == 12 and back.age == 42)


def str_has_bars(ctx):
    p = _new(ctx, "小樱")
    if p is None:
        return False
    s = str(p)
    if not isinstance(s, str) or "小樱" not in s or "object at" in s:
        return False
    has_bar = any(ch in s for ch in ["█", "░", "=", "#"])
    return has_bar and p.stage() in s


def save_load_missing(ctx):
    fn = ctx["ns"].get("load_pet")
    if not callable(fn):
        return False
    try:
        return fn("肯定不存在的宠物_xyz.json") is None
    except Exception:
        return False


def save_load_broken(ctx):
    fn = ctx["ns"].get("load_pet")
    if not callable(fn):
        return False
    name = "__判题坏档.json"
    try:
        with open(name, "w", encoding="utf-8") as f:
            f.write("{{{坏掉的")
        return fn(name) is None
    except Exception:
        return False
    finally:
        if os.path.exists(name):
            os.remove(name)


def save_file_written(ctx):
    if not os.path.exists("宠物存档.json"):
        return False
    try:
        with open("宠物存档.json", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return False
    return isinstance(d, dict) and "name" in d and "age" in d


def clamp_used(ctx):
    src = ctx["code"].replace(" ", "")
    return ("max(0,min(" in src) or ("clamp(" in src)


def demo_tired(ctx):
    return "玩不动" in ctx["stdout"] or "False" in ctx["stdout"]


def demo_ticks(ctx):
    import re
    return len(re.findall(r"第\s*\d+\s*小时", ctx["stdout"])) >= 5


def demo_stage(ctx):
    out = ctx["stdout"]
    return "幼年" in out or "少年" in out or "成年" in out


def demo_reload(ctx):
    return "读回来" in ctx["stdout"] or "已存档" in ctx["stdout"]


def survived(ctx):
    return ctx["error"] is None


CASES = [
    {
        "setup": SETUP,
        "stdin": ["喂食"],
        "checks": [
            {"id": "methods", "desc": "Pet 的九个方法都定义了",
             "type": "class_defined", "name": "Pet", "methods": METHODS,
             "fail": "feed / sleep / play / tick / is_hungry / stage / "
                     "to_dict / from_dict / __str__"},
            {"id": "init", "desc": "初始状态都是 50 / 0 / True",
             "type": "custom", "fn": "init_defaults",
             "fail": "hunger、energy、mood 都是 50，age 是 0，alive 是 True"},
            {"id": "clamp", "desc": "用了夹取保护状态值",
             "type": "custom", "fn": "clamp_used",
             "fail": "所有状态改动都要 `clamp(...)` 或 `max(0, min(值, 100))`"},
            {"id": "feed-clamp", "desc": "喂太多也不会变负 / 超上限",
             "type": "custom", "fn": "feed_clamps",
             "fail": "`feed(999)` 后饥饿应该是 **0**；心情 98 再 +5 只能到 100"},
            {"id": "feed-return", "desc": "feed 返回实际减少量",
             "type": "custom", "fn": "feed_returns_actual",
             "fail": "先记 before，改完算差值"},
            {"id": "sleep", "desc": "睡觉三项变化都对",
             "type": "custom", "fn": "sleep_effects",
             "fail": "睡 2 小时：精力 50→90、饥饿 50→70、年龄 0→2"},
            {"id": "sleep-clamp", "desc": "睡太久也不超 100",
             "type": "custom", "fn": "sleep_clamps",
             "fail": "睡 10 小时后精力和饥饿都该停在 100"},
            {"id": "play-ok", "desc": "玩耍三项变化都对",
             "type": "custom", "fn": "play_works",
             "fail": "精力 50→35、心情 50→65、饥饿 50→60，返回 True"},
            {"id": "play-tired", "desc": "精力 < 20 时玩不动",
             "type": "custom", "fn": "play_blocked_when_tired",
             "fail": "返回 `False`，而且**心情和精力都不能变** —— "
                     "提前 return，别先扣了再判断"},
            {"id": "tick", "desc": "tick 三项变化都对",
             "type": "custom", "fn": "tick_effects",
             "fail": "饥饿 +8、精力 -5、年龄 +1"},
            {"id": "tick-starve", "desc": "饿满了会掉心情",
             "type": "custom", "fn": "tick_starving_hurts_mood",
             "fail": "饥饿到 100 时 `mood -= 20`"},
            {"id": "tick-die", "desc": "心情精力都归零就不健康了",
             "type": "custom", "fn": "tick_can_kill",
             "fail": "`if self.mood <= 0 and self.energy <= 0: self.alive = False`"},
            {"id": "hungry", "desc": "is_hungry 边界正确",
             "type": "custom", "fn": "is_hungry_ok",
             "fail": "**大于** 70 才算饿 —— 70 本身不算"},
            {"id": "stage", "desc": "三个成长阶段边界都对",
             "type": "custom", "fn": "stage_ok",
             "fail": "age<10 幼年、10~29 少年、>=30 成年。边界值判题会试"},
            {"id": "to-dict", "desc": "to_dict 七个字段齐全且能存 json",
             "type": "custom", "fn": "to_dict_ok",
             "fail": "name / species / hunger / energy / mood / age / alive"},
            {"id": "classmethod", "desc": "from_dict 用了 @classmethod",
             "type": "custom", "fn": "from_dict_is_classmethod",
             "fail": "`def` 上面一行写 `@classmethod`，第一个参数是 `cls` 不是 `self`"},
            {"id": "roundtrip", "desc": "存出去再读回来状态一致",
             "type": "custom", "fn": "roundtrip_ok",
             "fail": "`Pet.from_dict(p.to_dict())` 之后，五项状态都要跟原来一样"},
            {"id": "str", "desc": "__str__ 含名字、阶段和状态条",
             "type": "custom", "fn": "str_has_bars",
             "fail": "用 `\"█\" * (值 // 10)` 画三条 10 格的状态条"},
            {"id": "load-missing", "desc": "没有存档时返回 None",
             "type": "custom", "fn": "save_load_missing",
             "fail": "接住 `FileNotFoundError`，返回 `None` 并提示"},
            {"id": "load-broken", "desc": "存档损坏时也返回 None",
             "type": "custom", "fn": "save_load_broken",
             "fail": "还要接住 `json.JSONDecodeError`"},
            {"id": "saved", "desc": "跑完之后存档文件写出来了",
             "type": "custom", "fn": "save_file_written",
             "fail": "最后要 `save_pet(SAVE, pet)`"},
            {"id": "demo-tired", "desc": "演示了太累玩不动",
             "type": "custom", "fn": "demo_tired",
             "fail": "把 `pet.energy` 调到 20 以下再 `play()` 一次"},
            {"id": "demo-tick", "desc": "让时间流逝了至少 5 小时",
             "type": "custom", "fn": "demo_ticks",
             "fail": "用 `for hour in range(5):` 循环调 `tick()`，每次打印状态"},
            {"id": "demo-stage", "desc": "打印了成长阶段",
             "type": "custom", "fn": "demo_stage",
             "fail": "调 `pet.stage()` 报一下现在是哪个阶段"},
            {"id": "demo-reload", "desc": "存档后又读回来验证了",
             "type": "custom", "fn": "demo_reload",
             "fail": "存完再 `load_pet` 一次，打印读回来的数据证明一致"},
            {"id": "survive", "desc": "全程没有崩溃",
             "type": "custom", "fn": "survived",
             "fail": "注意 `load_pet` 可能返回 `None`，用之前要判断"},
        ],
    }
]
