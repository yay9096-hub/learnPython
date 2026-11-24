import ast


def _classes(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.ClassDef)}


def _methods_of(ctx, name):
    cls = _classes(ctx).get(name)
    if cls is None:
        return {}
    return {f.name: f for f in cls.body if isinstance(f, ast.FunctionDef)}


def card_ok(ctx):
    C = ctx["ns"].get("Card")
    if not isinstance(C, type):
        return False
    c = C("测试卡", 20, 60)
    return (c.name == "测试卡" and c.atk == 20 and c.hp == 60
            and getattr(c, "max_hp", None) == 60
            and getattr(c, "cost", None) == 1)


def card_attack(ctx):
    C = ctx["ns"].get("Card")
    if not isinstance(C, type):
        return False
    a = C("甲", 20, 60)
    b = C("乙", 15, 100)
    dmg = a.attack(b)
    return dmg == 20 and b.hp == 80 and a.hp == 60


def card_floor(ctx):
    C = ctx["ns"].get("Card")
    if not isinstance(C, type):
        return False
    c = C("测试", 10, 30)
    got = c.take_damage(100)
    return c.hp == 0 and got == 30 and c.is_alive() is False


def card_str(ctx):
    C = ctx["ns"].get("Card")
    if not isinstance(C, type):
        return False
    s = str(C("小樱兵", 20, 60))
    return "小樱兵" in s and "20" in s and "60" in s and "object at" not in s


def magic_subclass(ctx):
    ns = ctx["ns"]
    M, C = ns.get("MagicCard"), ns.get("Card")
    if not isinstance(M, type) or not isinstance(C, type):
        return False
    return issubclass(M, C) and M is not C


def magic_super_init(ctx):
    init = _methods_of(ctx, "MagicCard").get("__init__")
    if init is None:
        return False
    for n in ast.walk(init):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "__init__":
                inner = n.func.value
                if isinstance(inner, ast.Call) and getattr(inner.func, "id", None) == "super":
                    return True
    return False


def magic_double(ctx):
    """魔法卡伤害翻倍，而且目标真的掉了双倍血。"""
    ns = ctx["ns"]
    M, C = ns.get("MagicCard"), ns.get("Card")
    if not isinstance(M, type) or not isinstance(C, type):
        return False
    m = M("术士", 20, 50)
    t = C("木桩", 5, 200)
    dmg = m.attack(t)
    return dmg == 40 and t.hp == 160


def magic_uses_super(ctx):
    fn = _methods_of(ctx, "MagicCard").get("attack")
    if fn is None:
        return False
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "attack":
                inner = n.func.value
                if isinstance(inner, ast.Call) and getattr(inner.func, "id", None) == "super":
                    return True
    return False


def magic_str_differs(ctx):
    ns = ctx["ns"]
    M, C = ns.get("MagicCard"), ns.get("Card")
    if not isinstance(M, type) or not isinstance(C, type):
        return False
    return str(M("术士", 20, 50)) != str(C("术士", 20, 50))


def magic_cost(ctx):
    M = ctx["ns"].get("MagicCard")
    if not isinstance(M, type):
        return False
    return M("术士", 20, 50).cost == 2


def _deck(ctx):
    ns = ctx["ns"]
    D, C, M = ns.get("Deck"), ns.get("Card"), ns.get("MagicCard")
    if not all(isinstance(x, type) for x in [D, C, M]):
        return None
    d = D("测试组")
    d.add(C("甲", 10, 30))
    d.add(C("乙", 20, 40))
    d.add(M("丙", 15, 20))
    return d


def deck_len(ctx):
    d = _deck(ctx)
    return d is not None and len(d) == 3


def deck_front_and_alive(ctx):
    d = _deck(ctx)
    if d is None:
        return False
    if d.front().name != "甲":
        return False
    d.cards[0].take_damage(999)
    if d.front().name != "乙":
        return False
    if len(d.alive_cards()) != 2 or d.is_defeated():
        return False
    for c in d.cards:
        c.take_damage(999)
    return d.is_defeated() is True and d.front() is None


def deck_total_atk(ctx):
    """只算活着的。"""
    d = _deck(ctx)
    if d is None:
        return False
    if d.total_atk() != 45:
        return False
    d.cards[0].take_damage(999)
    return d.total_atk() == 35


def deck_str(ctx):
    d = _deck(ctx)
    if d is None:
        return False
    s = str(d)
    return "测试组" in s and "object at" not in s


def shuffle_reproducible(ctx):
    """同一个种子洗两次，结果必须一样。"""
    ns = ctx["ns"]
    D, C = ns.get("Deck"), ns.get("Card")
    if not isinstance(D, type) or not isinstance(C, type):
        return False

    def build():
        d = D("测试")
        for i in range(6):
            d.add(C(f"卡{i}", i, 10))
        return d

    a = build()
    b = build()
    a.shuffle(123)
    b.shuffle(123)
    return [c.name for c in a.cards] == [c.name for c in b.cards]


def shuffle_actually_shuffles(ctx):
    ns = ctx["ns"]
    D, C = ns.get("Deck"), ns.get("Card")
    if not isinstance(D, type) or not isinstance(C, type):
        return False
    orders = set()
    for seed in range(12):
        d = D("测试")
        for i in range(6):
            d.add(C(f"卡{i}", i, 10))
        d.shuffle(seed)
        orders.add(tuple(c.name for c in d.cards))
    return len(orders) >= 3


def two_decks_five_cards(ctx):
    """主流程造了两副牌，加牌至少 10 次。"""
    n_deck = sum(1 for x in ast.walk(ctx["tree"])
                 if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "Deck")
    n_add = sum(1 for x in ast.walk(ctx["tree"])
                if isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute)
                and x.func.attr == "add")
    return n_deck >= 2 and n_add >= 10


def has_magic_cards(ctx):
    n = sum(1 for x in ast.walk(ctx["tree"])
            if isinstance(x, ast.Call) and getattr(x.func, "id", None) == "MagicCard")
    return n >= 4


def battle_loop(ctx):
    """至少打了 3 个回合。"""
    import re
    return len(re.findall(r"第\s*\d+\s*回合", ctx["stdout"])) >= 3


def has_round_cap(ctx):
    """循环里要有回合上限，防死循环。"""
    src = ctx["code"].replace(" ", "")
    return "MAX_ROUNDS" in src or "round_no<" in src or "round<" in src


def someone_died(ctx):
    return "击倒" in ctx["stdout"] or "💀" in ctx["stdout"]


def declares_result(ctx):
    out = ctx["stdout"]
    return "获胜" in out or "平局" in out


def battle_ended(ctx):
    """结束时至少一方全灭，或者到了回合上限。"""
    ns = ctx["ns"]
    a, b = ns.get("deck_a"), ns.get("deck_b")
    if a is None or b is None:
        return "战斗结束" in ctx["stdout"]
    return True


def survived(ctx):
    return ctx["error"] is None


CHECKS = [
    {"id": "card", "desc": "Card 属性齐全",
     "type": "custom", "fn": "card_ok",
     "fail": "`__init__(self, name, atk, hp, cost=1)`，另外要设 `max_hp`"},
    {"id": "card-atk", "desc": "Card.attack 扣对方的血",
     "type": "custom", "fn": "card_attack",
     "fail": "调 `other.take_damage(self.atk)` 并返回伤害；自己不掉血"},
    {"id": "card-floor", "desc": "血量不低于 0",
     "type": "custom", "fn": "card_floor",
     "fail": "`max(0, self.hp - amount)`，返回**实际**扣掉的血"},
    {"id": "card-str", "desc": "Card 有 __str__",
     "type": "custom", "fn": "card_str",
     "fail": "返回 `名字(攻/血)` 这种紧凑格式"},
    {"id": "magic-sub", "desc": "MagicCard 继承自 Card",
     "type": "class_defined", "name": "MagicCard", "base": "Card",
     "fail": "`class MagicCard(Card):`"},
    {"id": "magic-super", "desc": "MagicCard 的 __init__ 调了 super",
     "type": "custom", "fn": "magic_super_init",
     "fail": "第一句 `super().__init__(name, atk, hp, cost)`"},
    {"id": "magic-cost", "desc": "魔法卡默认费用是 2",
     "type": "custom", "fn": "magic_cost",
     "fail": "`def __init__(self, name, atk, hp, cost=2):`"},
    {"id": "magic-double", "desc": "魔法卡伤害翻倍",
     "type": "custom", "fn": "magic_double",
     "fail": "20 攻击的魔法卡应造成 **40** 点，目标要真的掉 40 血"},
    {"id": "magic-uses-super", "desc": "翻倍用的是 super()",
     "type": "custom", "fn": "magic_uses_super",
     "fail": "`base = super().attack(other)` 拿到基础伤害，"
             "再 `other.take_damage(base)` 补一次"},
    {"id": "magic-str", "desc": "魔法卡显示得跟普通卡不一样",
     "type": "custom", "fn": "magic_str_differs",
     "fail": "重写 `__str__`，名字前加个 ✨ 之类的标记"},
    {"id": "deck-len", "desc": "len(牌组) 可用",
     "type": "custom", "fn": "deck_len",
     "fail": "`__len__` 返回 `len(self.cards)`"},
    {"id": "deck-front", "desc": "front / alive_cards / is_defeated 正确",
     "type": "custom", "fn": "deck_front_and_alive",
     "fail": "`front()` 返回**第一张活着的**牌；全灭时返回 `None` 且 "
             "`is_defeated()` 为 True"},
    {"id": "deck-atk", "desc": "total_atk 只算活着的",
     "type": "custom", "fn": "deck_total_atk",
     "fail": "遍历 `alive_cards()` 而不是 `cards`"},
    {"id": "deck-str", "desc": "Deck 有 __str__",
     "type": "custom", "fn": "deck_str",
     "fail": "返回队名和剩余牌数"},
    {"id": "shuffle-repro", "desc": "同种子洗牌结果可复现",
     "type": "custom", "fn": "shuffle_reproducible",
     "fail": "`shuffle` 里先 `random.seed(seed)` 再 `random.shuffle(self.cards)`"},
    {"id": "shuffle-real", "desc": "不同种子会洗出不同顺序",
     "type": "custom", "fn": "shuffle_actually_shuffles",
     "fail": "要真的调 `random.shuffle(...)`，不能什么都不做"},
    {"id": "two-decks", "desc": "造了两副各 5 张的牌",
     "type": "custom", "fn": "two_decks_five_cards",
     "fail": "两个 `Deck`，一共至少 `add` 10 次"},
    {"id": "magic-count", "desc": "每副至少 2 张魔法卡",
     "type": "custom", "fn": "has_magic_cards",
     "fail": "一共至少造 4 张 `MagicCard`"},
    {"id": "battle", "desc": "打了至少 3 个回合",
     "type": "custom", "fn": "battle_loop",
     "fail": "用 `while` 循环，每回合打印「第 N 回合」"},
    {"id": "cap", "desc": "循环有回合上限",
     "type": "custom", "fn": "has_round_cap",
     "fail": "⚠️ 加一个 `round_no < MAX_ROUNDS` 的保险丝，"
             "万一双方伤害太低也不会变成死循环"},
    {"id": "died", "desc": "有卡牌被击倒",
     "type": "custom", "fn": "someone_died",
     "fail": "卡牌血量归零时要打印一句「被击倒」"},
    {"id": "result", "desc": "宣布了胜负",
     "type": "custom", "fn": "declares_result",
     "fail": "根据 `is_defeated()` 判断哪一方赢了"},
    {"id": "survive", "desc": "全程没有崩溃",
     "type": "custom", "fn": "survived",
     "fail": "注意 `front()` 可能返回 `None` —— 攻击前要确认双方都还有牌"},
]
