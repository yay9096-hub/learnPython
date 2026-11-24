# Day 62 · 卡牌对战 🎴

> 「今天把这一章学的全部用上，做一个**能自己打完一整局**的卡牌游戏。
>
> 三个类：卡牌、牌组、对战。它们互相配合 ——
> 这才是面向对象真正的样子。」

---

## 🔍 第六章到目前为止的武器

| 天 | 学到的 |
|---|---|
| D55 | `class` / `__init__` / `self` |
| D56 | 方法 / 对象之间互相调用 |
| D57 | 属性保护 / 不变量 / 夹取 |
| D58 | 类的组合（Team 装着一堆 Role） |
| D59 | 继承 / `super().__init__` |
| D60 | 方法重写 / 多态 |
| D61 | 特殊方法 `__str__` / `__len__` / `__eq__` |

**今天七样全用上。**

---

## 📌 知识卡 · 让随机可控 ⭐

今天唯一的新技巧。游戏要随机，但**判题需要结果稳定**。

```python runnable 固定种子，随机就可复现
import random

random.seed(42)
print([random.randint(1, 100) for _ in range(5)])

random.seed(42)
print([random.randint(1, 100) for _ in range(5)])

random.seed(1)
print([random.randint(1, 100) for _ in range(5)])
```

**同一个种子，每次跑出来一模一样。**

`random.seed(数字)` 相当于告诉随机数生成器「从这个起点开始」。
换个种子就是另一串数。

游戏开发里这招很常用：

- 调试时固定种子，**bug 能稳定复现**
- 「每日挑战」用日期当种子，**全世界玩家拿到同一副牌**

```python runnable 洗牌也能复现
import random

cards = ["A", "B", "C", "D", "E"]

random.seed(7)
random.shuffle(cards)
print(cards)

cards = ["A", "B", "C", "D", "E"]
random.seed(7)
random.shuffle(cards)
print(cards)
```

⚠️ `random.shuffle(列表)` **直接打乱原列表**，不返回新的（又是 Day 24 那个坑）。

---

## 🎯 今天的作品 · 卡牌对战

### 三个类

**`Card`（卡牌）**

| 成员 | 说明 |
|---|---|
| `__init__(self, name, atk, hp, cost=1)` | 四个属性，另加 `max_hp` |
| `is_alive(self)` | 血量 > 0 |
| `take_damage(self, amount)` | 扣血，不低于 0，返回实际扣血 |
| `attack(self, other)` | 攻击另一张卡，返回造成的伤害 |
| `__str__(self)` | `名字(攻/血)` 这种紧凑格式 |
| `__repr__(self)` | 同上即可 |

**`MagicCard(Card)`（魔法卡，继承）**

| 成员 | 说明 |
|---|---|
| `__init__(self, name, atk, hp, cost=2)` | 调 `super()` |
| `attack(self, other)` | **重写**：伤害翻倍（用 `super()` 拿基础伤害再补一次） |
| `__str__(self)` | 名字前加个 `✨` 区分开 |

**`Deck`（牌组）**

| 成员 | 说明 |
|---|---|
| `__init__(self, name)` | `name` 和空的 `cards` |
| `add(self, card)` | 加一张牌 |
| `__len__(self)` | 牌数 |
| `__str__(self)` | 队名 + 剩余牌数 |
| `alive_cards(self)` | 还活着的牌 |
| `front(self)` | **第一张活着的牌**（前排），全死返回 `None` |
| `is_defeated(self)` | 全灭了吗 |
| `shuffle(self, seed=None)` | 洗牌。给了 seed 就先 `random.seed(seed)` |
| `total_atk(self)` | 全部存活卡牌的攻击力总和 |

### 主流程

- 用**固定种子**造两副牌，每副至少 5 张，其中**至少 2 张魔法卡**
- 洗牌（用固定 seed，保证结果可复现）
- 打印两副牌的完整内容
- **回合循环**：每回合双方 `front()` 互相攻击一次
  - 打印回合数、双方前排、造成的伤害
  - 有卡倒下要打印
  - 任意一方 `is_defeated()` 就结束
  - **加一个回合上限**（比如 30）防死循环
- 结束后打印双方剩余卡牌和胜负

> 💡 判题会用固定种子跑，所以结果是确定的。
> **`random.seed(...)` 一定要写在洗牌之前。**
