# Day 60 · 各自的绝招 ✨

> 「昨天三个职业各有各的方法：`roar`、`cast`、`backstab`。
> 结果主流程里要写一堆 `if isinstance(...)` 才知道该调哪个 —— 很难看。
>
> 今天让它们**共用一个方法名 `attack`**，
> 但每个职业的 `attack` 表现不同。
>
> 这是面向对象里最漂亮的一招。」

---

## 📌 知识卡 1 · 先看看不重写有多别扭

```python runnable 到处都是 isinstance（不好）
class Role:
    def __init__(self, name, atk):
        self.name = name
        self.atk = atk

class Warrior(Role):
    def heavy_strike(self):
        return self.atk * 2

class Mage(Role):
    def cast(self):
        return self.atk * 3


team = [Warrior("铁壁", 40), Mage("琉璃", 25)]

for m in team:
    if isinstance(m, Warrior):
        print(f"{m.name} 重击 {m.heavy_strike()}")
    elif isinstance(m, Mage):
        print(f"{m.name} 施法 {m.cast()}")
```

每加一个职业，这个 `if` 链就要加一段。**加十个职业就是十段。**

---

## 📌 知识卡 2 · 重写：子类写一个同名方法 ⭐

```python runnable 同一个名字，不同的实现
class Role:
    def __init__(self, name, atk):
        self.name = name
        self.atk = atk

    def attack(self):
        """普通攻击。"""
        return self.atk


class Warrior(Role):
    def attack(self):
        """战士的重击：伤害翻倍。"""
        return self.atk * 2


class Mage(Role):
    def attack(self):
        """法师的魔法：伤害三倍。"""
        return self.atk * 3


team = [Role("路人", 30), Warrior("铁壁", 40), Mage("琉璃", 25)]

for m in team:
    print(f"  {m.name} 攻击，造成 {m.attack()} 点")
```

**`for` 循环里只有一句 `m.attack()`，三个职业却打出了三种伤害。**

Python 会自动找到「这个对象自己那一份」`attack`。
这叫**多态**（polymorphism）—— 同一句代码，不同表现。

> 🧠 一句话对比：
> **继承是「拿到父类的本事」，重写是「把某个本事改成自己的版本」。**

---

## 📌 知识卡 3 · `super()` —— 在父类基础上加料 ⭐

有时候你不想完全推翻父类的做法，只想**加点东西**：

```python runnable 先调父类，再加自己的
class Role:
    def __init__(self, name, atk):
        self.name = name
        self.atk = atk

    def attack(self, target):
        """基础攻击：造成 atk 点伤害。"""
        print(f"     {self.name} 攻击 {target}，造成 {self.atk} 点")
        return self.atk


class Warrior(Role):
    def attack(self, target):
        """战士：先照常打一下，再追加一次重击。"""
        base = super().attack(target)        # ← 先让父类打
        bonus = self.atk // 2
        print(f"     💥 追加重击 {bonus} 点！")
        return base + bonus


w = Warrior("铁壁", 40)
total = w.attack("木桩")
print(f"  共造成 {total} 点")
```

`super().attack(target)` —— **在子类里调用父类的同名方法**。

好处是：父类的攻击逻辑（播报、扣血、统计）只写一次，
子类只管「多做的那部分」。

⚠️ 别写成 `self.attack(target)` —— 那是调用**自己**，会无限递归。

---

## 📌 知识卡 4 · 重写的三种姿势

```python runnable 三种写法对比
class Role:
    def __init__(self, name, atk):
        self.name = name
        self.atk = atk

    def attack(self):
        return self.atk


class A(Role):
    """① 完全替换：不管父类怎么做。"""
    def attack(self):
        return 999


class B(Role):
    """② 扩展：在父类结果上加工。"""
    def attack(self):
        return super().attack() * 2


class C(Role):
    """③ 不重写：直接用父类的。"""
    pass


for cls in [A, B, C]:
    obj = cls("测试", 40)
    print(f"  {cls.__name__}: {obj.attack()}")
```

| 姿势 | 什么时候用 |
|---|---|
| **完全替换** | 子类的做法跟父类毫无关系 |
| **`super()` 扩展** | 父类做的大部分对，只想加料（**最常用**） |
| **不重写** | 父类的完全够用 |

---

## 📌 知识卡 5 · `__init__` 其实也是重写

回头看昨天的代码：

```python runnable __init__ 也遵循同样的规则
class Role:
    def __init__(self, name, hp=100):
        print("     Role 的 __init__ 跑了")
        self.name = name
        self.hp = hp


class Mage(Role):
    def __init__(self, name, hp=120, mp=100):
        print("     Mage 的 __init__ 开始")
        super().__init__(name, hp)       # ← 就是在调父类的 __init__
        self.mp = mp
        print("     Mage 的 __init__ 结束")


m = Mage("琉璃")
print(f"  {m.name} HP {m.hp} MP {m.mp}")
```

**昨天写的 `super().__init__(...)` 就是「重写 + 扩展」的一个例子** ——
只不过重写的是 `__init__` 而已。

---

## 📌 知识卡 6 · 多态让主流程变干净 ⭐

```python runnable 一个循环搞定所有职业
class Role:
    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.hp = hp
        self.atk = atk

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def attack(self, target):
        """基础攻击。"""
        damage = self.atk
        target.take_damage(damage)
        return damage

    def skill_name(self):
        """技能名字。"""
        return "普通攻击"


class Warrior(Role):
    def attack(self, target):
        damage = super().attack(target) + self.atk // 2
        target.take_damage(self.atk // 2)
        return damage

    def skill_name(self):
        return "狂暴重击"


class Mage(Role):
    def attack(self, target):
        damage = self.atk * 3
        target.take_damage(damage)
        return damage

    def skill_name(self):
        return "奥术飞弹"


enemy = Role("魔王", 999)
team = [Role("路人", 100, 30), Warrior("铁壁", 200, 40), Mage("琉璃", 120, 25)]

for m in team:
    dmg = m.attack(enemy)
    print(f"  {m.name} 使用「{m.skill_name()}」，造成 {dmg} 点")

print(f"  魔王剩余 {enemy.hp}")
```

**主流程里一个 `isinstance` 都没有** —— 每个对象自己知道该怎么打。

以后要加第十个职业？**主流程一个字都不用改。**

> 💡 这就是面向对象最有价值的地方：
> **新增功能靠「加一个类」，而不是「改一堆 if」。**

---

## 🛠 今天的任务 · 技能系统

`Role` 是父类，三个子类各自重写：

| 类 | `attack(self, target)` | `skill_name(self)` | 备注 |
|---|---|---|---|
| `Role` | 造成 `atk` 点伤害，返回伤害 | 返回 `"普通攻击"` | 基础实现 |
| `Warrior(Role)` | **用 `super()` 扩展**：父类伤害 + 额外 `atk // 2` | `"狂暴重击"` | 额外伤害也要真的打出去 |
| `Mage(Role)` | 完全替换：伤害 = `atk * 3`，但**要扣 20 点 mp**；mp 不够时**退回普通攻击**（调 `super()`） | 够蓝 `"奥术飞弹"`，不够 `"法杖敲击"` | |
| `Rogue(Role)` | 完全替换：伤害 = `int(atk * 2.5)` | `"背刺"` | |

另外每个类都要有：

- `take_damage(self, amount)` —— 只写在 `Role` 里，子类不重写
- `status(self)` —— 只写在 `Role` 里

主流程要求：

- 造一个敌人（血厚一点）和四个角色（含一个纯 `Role`）
- **用一个 `for` 循环**让全员攻击敌人，打印技能名和伤害
- **主流程里不许出现 `isinstance`**
- 演示法师蓝不够时会退回普通攻击（把 `mp` 调低再打一次）
- 打印每个角色的类名和技能名对照表
- 最后打印敌人剩余血量

> ⚠️ 战士的 `attack` **必须用 `super().attack(target)`**，
> 不许把父类的逻辑抄一遍。判题会检查。
