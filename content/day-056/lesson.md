# Day 56 · 角色的技能 ⚔️

> 「昨天的 `Role` 只有数据，跟字典比没强多少。
>
> 今天把**本事**也装进去 —— 让角色自己会攻击、会治疗、会升级。
> 这才是类真正的价值。」

---

## 📌 知识卡 1 · 方法 = 写在类里的函数 ⭐

```python runnable 第一个方法
class Role:
    """一个会打招呼的角色。"""

    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp

    def greet(self):
        """打个招呼。"""
        print(f"我是 {self.name}，血量 {self.hp}！")


sakura = Role("星野樱", 340)
sakura.greet()

ruri = Role("月见琉璃", 280)
ruri.greet()
```

三件事：

1. **方法定义在 `class` 里面**，缩进一层
2. **第一个参数还是 `self`**
3. **调用时不用传 self** —— `sakura.greet()`，Python 自动把 `sakura` 塞进去

> 🧠 `sakura.greet()` 其实就是 `Role.greet(sakura)` 的简写。
> 这就是 `self` 的来历 —— **它就是点号前面那个对象**。

---

## 📌 知识卡 2 · 方法可以改自己的属性 ⭐

```python runnable 会掉血的角色
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp

    def take_damage(self, amount):
        """受到伤害，扣血。"""
        self.hp = self.hp - amount
        print(f"  {self.name} 受到 {amount} 点伤害，剩余 {self.hp}")


sakura = Role("星野樱", 340)
print(sakura.hp)

sakura.take_damage(88)
sakura.take_damage(110)

print(sakura.hp)
```

对比 Day 40 的痛苦 —— 那时候你要写 `hp = damage(hp, 88)` 再接住返回值。
现在 **`self.hp` 改了就是改了**，因为对象是可变的。

---

## 📌 知识卡 3 · 方法可以接收别的对象

```python runnable 两个角色互相打
class Role:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def take_damage(self, amount):
        """受到伤害。"""
        self.hp = self.hp - amount

    def attack(self, target):
        """攻击另一个角色。"""
        print(f"  ⚔️ {self.name} 攻击 {target.name}，造成 {self.atk} 点伤害")
        target.take_damage(self.atk)


sakura = Role("星野樱", 340, 88)
enemy = Role("暗影魔像", 500, 66)

sakura.attack(enemy)
print(f"  {enemy.name} 剩余 {enemy.hp}")

enemy.attack(sakura)
print(f"  {sakura.name} 剩余 {sakura.hp}")
```

看清楚 `attack` 里的两个角色：

- **`self`** 是攻击者（点号前面那个）
- **`target`** 是被攻击者（括号里传进来的）

`target.take_damage(...)` —— **一个对象调用另一个对象的方法**。
真实游戏的战斗系统就是这么写的。

---

## 📌 知识卡 4 · 方法可以调用自己的别的方法

```python runnable 方法之间互相调用
class Role:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp
        self.max_hp = hp

    def is_alive(self):
        """还活着吗。"""
        return self.hp > 0

    def take_damage(self, amount):
        """受伤。死了就报一句。"""
        self.hp = self.hp - amount
        if not self.is_alive():          # ← 调用自己的另一个方法
            print(f"  💀 {self.name} 倒下了")

    def status(self):
        """当前状态。"""
        state = "存活" if self.is_alive() else "倒下"
        return f"{self.name}  HP {self.hp}/{self.max_hp}  [{state}]"


r = Role("星野樱", 100)
print(r.status())
r.take_damage(120)
print(r.status())
```

⚠️ **调用自己的方法也要写 `self.`** —— 直接写 `is_alive()` 会报 NameError。

---

## 📌 知识卡 5 · 有返回值的方法

```python runnable 方法也能 return
class Role:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

    def deal_damage(self, target):
        """攻击目标，返回实际造成的伤害。"""
        damage = self.atk
        target.hp = target.hp - damage
        return damage


a = Role("星野樱", 340, 88)
b = Role("魔像", 500, 66)

total = 0
for i in range(3):
    dmg = a.deal_damage(b)
    total = total + dmg
    print(f"  第 {i + 1} 回合：造成 {dmg}，敌人剩 {b.hp}")

print(f"三回合共造成 {total} 点伤害")
```

Day 37 学的 `return`，在方法里完全一样用。

---

## 📌 知识卡 6 · 方法让代码读起来像句子

对比一下这两段：

```python runnable 函数版（Day 41 的写法）
def take_damage(role, amount):
    role["hp"] = role["hp"] - amount

def is_alive(role):
    return role["hp"] > 0

r = {"name": "樱", "hp": 100}
take_damage(r, 120)
print(is_alive(r))
```

```python runnable 方法版
class Role:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def take_damage(self, amount):
        self.hp = self.hp - amount

    def is_alive(self):
        return self.hp > 0

r = Role("樱", 100)
r.take_damage(120)
print(r.is_alive())
```

`r.take_damage(120)` 读起来就是「**r 受到 120 点伤害**」——
主语在前，动作在后，跟说话一样。

而且**所有能对角色做的事，都挂在角色身上** ——
打个点，编辑器就会列出来给你看。

---

## 🛠 今天的任务 · 会战斗的角色

给 `Role` 加上方法：

| 方法 | 说明 |
|---|---|
| `__init__(self, name, hp=100, mp=50, atk=30)` | 还要设 `max_hp` 和 `alive` |
| `is_alive(self)` | 返回 `True` / `False` |
| `take_damage(self, amount)` | 扣血。血量 ≤ 0 时把 `alive` 设为 `False` 并打印倒下。**返回实际扣的血** |
| `attack(self, target)` | 攻击另一个角色。调用 `target.take_damage(...)`，**返回造成的伤害** |
| `heal(self, amount)` | 回血。**返回实际回了多少** |
| `level_up(self)` | 等级 +1，`max_hp` +20，`atk` +5，并且回满血 |
| `status(self)` | **返回**一行状态文字（不是 print） |

主流程要求：

- 造两个角色（我方 + 敌方）
- 打印双方初始状态
- 打一个至少 3 回合的循环，双方互相攻击，每回合打印状态
- 中途用一次 `heal`
- 用一次 `level_up`
- 用 `is_alive` 判断战斗该不该继续
- 最后宣布谁赢了

> ⚠️ `status` 要**返回**字符串，主流程负责 print（Day 37 的原则）。
> 其余方法可以自己打印战斗播报。
