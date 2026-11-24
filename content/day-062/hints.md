## 提示 1 · Card 和 MagicCard

`Card` 就是 Day 56~57 的翻版：

```python
class Card:
    def __init__(self, name, atk, hp, cost=1):
        self.name = name
        self.atk = atk
        self.max_hp = hp
        self.hp = hp
        self.cost = cost

    def take_damage(self, amount):
        before = self.hp
        self.hp = max(0, self.hp - amount)
        return before - self.hp

    def attack(self, other):
        other.take_damage(self.atk)
        return self.atk

    def __str__(self):
        return f"{self.name}({self.atk}/{self.hp})"

    def __repr__(self):
        return self.__str__()
```

魔法卡用 `super()` 扩展（Day 60 学的）：

```python
class MagicCard(Card):
    def __init__(self, name, atk, hp, cost=2):
        super().__init__(name, atk, hp, cost)

    def attack(self, other):
        """在普通攻击基础上再补一次同样的伤害。"""
        base = super().attack(other)     # 已经打了一次
        other.take_damage(base)          # 再补一次
        return base * 2

    def __str__(self):
        return f"✨{self.name}({self.atk}/{self.hp})"
```

⚠️ `super().attack(other)` **已经打出去一次了**，所以只需要再补一次，
返回值是 `base * 2`。

## 提示 2 · Deck 的关键方法

```python
    def alive_cards(self):
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
        return len(self.alive_cards()) == 0

    def shuffle(self, seed=None):
        """洗牌。给了 seed 就固定随机，保证结果可复现。"""
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
        return self.cards
```

⚠️ `total_atk` 要遍历 **`alive_cards()`** 而不是 `cards` —— 死掉的不算战力。

⚠️ `random.shuffle(列表)` **直接打乱原列表**，不返回新的。

## 提示 3 · 战斗循环的三个保险

```python
round_no = 0
while (not deck_a.is_defeated() and not deck_b.is_defeated()
       and round_no < MAX_ROUNDS):          # ← 保险丝
    round_no = round_no + 1
    a = deck_a.front()
    b = deck_b.front()

    print(f"\n第 {round_no} 回合：{a}  VS  {b}")

    damage = a.attack(b)
    print(f"  {a.name} 造成 {damage} 点")
    if not b.is_alive():
        print(f"  💀 {b.name} 被击倒")

    if b.is_alive():                         # ← 死了就别还手了
        damage = b.attack(a)
        print(f"  {b.name} 造成 {damage} 点")
        if not a.is_alive():
            print(f"  💀 {a.name} 被击倒")
```

三个必须有的保险：

1. **`round_no < MAX_ROUNDS`** —— 万一双方伤害都很低，不会死循环
2. **`while` 条件里检查两边都没全灭** —— 保证 `front()` 不会返回 `None`
3. **`if b.is_alive():` 才还手** —— 死掉的卡不能反击

打印牌组内容直接 `print(deck.cards)` —— 因为写了 `__repr__`，
列表会自动显示成漂亮的样子（Day 61 学的）。
