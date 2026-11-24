# Day 59 · 战士与法师 🧙

> 「现在你想加职业：战士有护甲，法师有魔法值，盗贼有暴击率。
>
> 笨办法是复制三份 `Role`，各改各的 —— 然后你会发现：
> **改一个 bug 要改三个地方。**
>
> 今天学继承：**共同的写一次，不同的各写各的。**」

---

## 📌 知识卡 1 · 复制粘贴有多糟

```python runnable 三个类，90% 的代码一模一样
class Warrior:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.armor = 10

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)


class Mage:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.mp = 100

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)


w = Warrior("战士", 200)
m = Mage("法师", 120)
print(w.hp, m.hp)
```

`take_damage` 一模一样写了两遍。以后想加「血量不能变负」的保护？**改两处**。
再加个盗贼？**改三处**。这是 bug 的温床。

---

## 📌 知识卡 2 · `class 子类(父类)` ⭐

```python runnable 继承：一行就拿到全部本事
class Role:
    """所有职业的共同基础。"""

    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.alive = True

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        self.alive = self.hp > 0
        return amount

    def status(self):
        return f"{self.name}  HP {self.hp}/{self.max_hp}  ATK {self.atk}"


class Warrior(Role):
    """战士。目前什么都没加，但已经全都会了。"""
    pass


w = Warrior("铁壁", 200, 40)

print(w.status())
w.take_damage(50)
print(w.status())
print(w.is_alive())
```

`class Warrior(Role):` —— 括号里写父类。

**`Warrior` 什么方法都没写，却全都会了** ——
`status`、`take_damage`、`is_alive` 全是从 `Role` 继承来的。

> 🧠 术语：
> `Role` 叫**父类 / 基类**，`Warrior` 叫**子类 / 派生类**。
> 关系是「**Warrior 是一种 Role**」。

---

## 📌 知识卡 3 · 子类加自己的东西

```python runnable 子类可以加新方法
class Role:
    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk

    def status(self):
        return f"{self.name}  HP {self.hp}/{self.max_hp}"


class Warrior(Role):
    """战士，会怒吼。"""

    def roar(self):
        """怒吼，攻击力临时 +10。"""
        self.atk = self.atk + 10
        return f"{self.name} 发出怒吼！攻击力升到 {self.atk}"


w = Warrior("铁壁", 200, 40)
print(w.status())
print(w.roar())
print(w.atk)
```

**父类的都有，自己的还能加** —— 这就是继承的价值。

⚠️ 反过来不行：`Role` 没有 `roar`，父类不知道子类的存在。

---

## 📌 知识卡 4 · `super()` —— 调父类的 `__init__` ⭐

子类想加**属性**时，得先让父类把公共部分初始化好：

```python runnable super 的标准写法
class Role:
    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.alive = True


class Mage(Role):
    """法师，多一个魔法值。"""

    def __init__(self, name, hp=100, atk=30, mp=100):
        super().__init__(name, hp, atk)      # ← 先让父类初始化
        self.mp = mp                          # ← 再加自己的
        self.max_mp = mp


m = Mage("琉璃", 120, 25, 200)
print(m.name, m.hp, m.atk)
print(m.mp, m.max_mp)
print(m.alive)
```

`super().__init__(...)` 读作：「**先按父类的方式初始化**」。

⚠️ **忘了它会出大事**：

```python runnable 忘了 super 的下场
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp


class Mage(Role):
    def __init__(self, name, hp=100, mp=100):
        self.mp = mp          # 只设了自己的，父类的全没了


m = Mage("琉璃")
print(m.mp)
print(m.name)
```

`AttributeError` —— `name` 和 `hp` 根本没被设置。

> 🧠 铁律：**子类写了 `__init__`，第一句就应该是 `super().__init__(...)`。**

---

## 📌 知识卡 5 · 子类可以有自己的规则

```python runnable 战士的护甲
class Role:
    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.alive = True

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        self.alive = self.hp > 0
        return amount

    def status(self):
        return f"{self.name}  HP {self.hp}/{self.max_hp}"


class Warrior(Role):
    """战士。护甲能减免固定伤害。"""

    def __init__(self, name, hp=200, atk=40, armor=10):
        super().__init__(name, hp, atk)
        self.armor = armor

    def real_damage(self, amount):
        """算上护甲之后实际会受到多少伤害，最低 1 点。"""
        return max(1, amount - self.armor)


w = Warrior("铁壁")
print(w.status())
print(f"挨 50 点，实际受到 {w.real_damage(50)} 点")
print(f"挨 5 点，实际受到 {w.real_damage(5)} 点")
```

`real_damage` 是**战士独有的**，`Role` 和 `Mage` 都没有。

---

## 📌 知识卡 6 · `isinstance` —— 判断是哪一类

```python runnable 判断类型
class Role:
    def __init__(self, name):
        self.name = name

class Warrior(Role):
    pass

class Mage(Role):
    pass


team = [Warrior("铁壁"), Mage("琉璃"), Warrior("盾姬")]

for m in team:
    kind = type(m).__name__
    print(f"  {m.name} 是 {kind}")

print(isinstance(team[0], Warrior))
print(isinstance(team[0], Role))
print(isinstance(team[0], Mage))
```

⚠️ 注意第二行：**战士也是 Role** —— 因为 Warrior 继承自 Role。

`type(m).__name__` 拿到类名的文字，做职业显示很方便。

```python runnable 统计各职业人数
class Role:
    def __init__(self, name):
        self.name = name

class Warrior(Role):
    pass

class Mage(Role):
    pass


team = [Warrior("铁壁"), Mage("琉璃"), Warrior("盾姬"), Mage("星野")]

counts = {}
for m in team:
    kind = type(m).__name__
    counts[kind] = counts.get(kind, 0) + 1

print(counts)
```

`counts.get(kind, 0) + 1` —— Day 29 的 `.get(键, 默认值)` 在这里正好用上。

---

## 🛠 今天的任务 · 三个职业

| 类 | 说明 |
|---|---|
| `Role` | 父类。`__init__(self, name, hp=100, atk=30)`；方法：`is_alive` / `take_damage` / `heal` / `status` |
| `Warrior(Role)` | `__init__(..., armor=10)`。加 `armor` 属性；加方法 `real_damage(amount)`（护甲减免，最低 1）和 `roar()`（攻击 +10，返回一句话） |
| `Mage(Role)` | `__init__(..., mp=100)`。加 `mp` / `max_mp`；加方法 `cast(target, cost=20)` —— 魔法不够返回 0，够则扣 mp 并造成 `atk * 2` 伤害 |
| `Rogue(Role)` | `__init__(..., crit=2.0)`。加 `crit`；加方法 `backstab(target)` —— 造成 `atk * crit` 的伤害（取整） |

三个子类的 `__init__` **都要调 `super().__init__(...)`**。

主流程要求：

- 三个职业各造一个，装进一个列表
- 遍历打印每个人的**职业名**（用 `type(m).__name__`）和状态
- 演示战士的 `real_damage`（大伤害和小伤害各一次）
- 演示战士 `roar` 后攻击力变化
- 演示法师 `cast`：魔法够的时候和不够的时候各一次
- 演示盗贼 `backstab` 的伤害
- 用 `isinstance` 证明「战士也是 Role」
- 统计各职业人数（用字典）

> ⚠️ 子类里**不许重复写** `take_damage` / `heal` / `status` ——
> 那些是从父类继承来的。判题会检查。
