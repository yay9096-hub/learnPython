# Day 62 · 卡牌对战
import random

SEED = 2026
MAX_ROUNDS = 30


class Card:
    """一张普通卡牌。"""

    def __init__(self, name, atk, hp, cost=1):
        self.name = name
        self.atk = atk
        self.max_hp = hp
        self.hp = hp
        self.cost = cost

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        """扣血，血量不低于 0，返回实际扣掉的血。"""
        before = self.hp
        self.hp = max(0, self.hp - amount)
        return before - self.hp

    def attack(self, other):
        """攻击另一张卡，返回造成的伤害。"""
        other.take_damage(self.atk)
        return self.atk

    def __str__(self):
        return f"{self.name}({self.atk}/{self.hp})"

    def __repr__(self):
        return self.__str__()


class MagicCard(Card):
    """魔法卡。费用更高，但伤害翻倍。"""

    def __init__(self, name, atk, hp, cost=2):
        super().__init__(name, atk, hp, cost)

    def attack(self, other):
        """重写：在普通攻击基础上再补一次同样的伤害。"""
        base = super().attack(other)
        other.take_damage(base)
        return base * 2

    def __str__(self):
        return f"✨{self.name}({self.atk}/{self.hp})"


class Deck:
    """一副牌组。"""

    def __init__(self, name):
        self.name = name
        self.cards = []

    def add(self, card):
        """加一张牌，返回现在的牌数。"""
        self.cards.append(card)
        return len(self.cards)

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"《{self.name}》剩 {len(self.alive_cards())}/{len(self.cards)} 张"

    def alive_cards(self):
        """还活着的牌。"""
        result = []
        for c in self.cards:
            if c.is_alive():
                result.append(c)
        return result

    def front(self):
        """第一张活着的牌。全灭返回 None。"""
        alive = self.alive_cards()
        if len(alive) == 0:
            return None
        return alive[0]

    def is_defeated(self):
        """全灭了吗。"""
        return len(self.alive_cards()) == 0

    def shuffle(self, seed=None):
        """洗牌。给了 seed 就固定随机，保证结果可复现。"""
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
        return self.cards

    def total_atk(self):
        """存活卡牌的攻击力总和。"""
        total = 0
        for c in self.alive_cards():
            total += c.atk
        return total


# ---------- 主流程 ----------
print("🎴 === 卡牌对战 === 🎴")

deck_a = Deck("樱之队")
deck_a.add(Card("小樱兵", 20, 60))
deck_a.add(Card("盾卫", 15, 100))
deck_a.add(MagicCard("樱花术士", 18, 50))
deck_a.add(Card("弓手", 25, 45))
deck_a.add(MagicCard("结界师", 15, 55))

deck_b = Deck("暗影军团")
deck_b.add(Card("暗影兵", 22, 55))
deck_b.add(Card("石像鬼", 12, 110))
deck_b.add(MagicCard("咒术师", 20, 45))
deck_b.add(Card("刺客", 30, 35))
deck_b.add(MagicCard("亡灵法师", 16, 50))

deck_a.shuffle(SEED)
deck_b.shuffle(SEED + 1)

print(f"\n{deck_a}")
print(f"  {deck_a.cards}")
print(f"  总攻击力 {deck_a.total_atk()}")

print(f"\n{deck_b}")
print(f"  {deck_b.cards}")
print(f"  总攻击力 {deck_b.total_atk()}")

print("\n--- 开战 ---")
round_no = 0
while (not deck_a.is_defeated() and not deck_b.is_defeated()
       and round_no < MAX_ROUNDS):
    round_no = round_no + 1
    a = deck_a.front()
    b = deck_b.front()

    print(f"\n第 {round_no} 回合：{a}  VS  {b}")

    damage = a.attack(b)
    print(f"  {a.name} 造成 {damage} 点")
    if not b.is_alive():
        print(f"  💀 {b.name} 被击倒")

    if b.is_alive():
        damage = b.attack(a)
        print(f"  {b.name} 造成 {damage} 点")
        if not a.is_alive():
            print(f"  💀 {a.name} 被击倒")

print("\n=== 战斗结束 ===")
print(f"  {deck_a}  {deck_a.alive_cards()}")
print(f"  {deck_b}  {deck_b.alive_cards()}")

if deck_b.is_defeated() and not deck_a.is_defeated():
    print(f"\n🎉 {deck_a.name} 获胜！")
elif deck_a.is_defeated() and not deck_b.is_defeated():
    print(f"\n💀 {deck_b.name} 获胜！")
else:
    print("\n🤝 平局")
