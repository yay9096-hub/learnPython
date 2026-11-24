# Day 57 · 给属性上保险 🛡

> 「昨天的 `Role` 能打架了，但它太老实 ——
>
> 血量能变成 **-500**，治疗能治到 **9999**，
> 甚至有人能给 `take_damage` 传个负数来「反向治疗」。
>
> 今天让这个类**自己守规矩**。」

---

## 📌 知识卡 1 · 先看看有多离谱

```python runnable 没有保险的类
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp
        self.max_hp = hp

    def take_damage(self, amount):
        self.hp = self.hp - amount

    def heal(self, amount):
        self.hp = self.hp + amount


r = Role("星野樱", 100)

r.take_damage(500)
print(f"挨了 500 点：{r.hp}")

r.heal(9999)
print(f"治疗 9999：{r.hp} / {r.max_hp}")

r.take_damage(-100)
print(f"挨了 -100 点：{r.hp}")
```

三个荒唐的结果：**负血量、超过上限、挨打反而加血**。

> 🧠 这里有个重要概念叫**不变量**（invariant）——
> 「无论发生什么，都必须成立的规则」。
>
> 对 `Role` 来说，不变量是：**`0 <= hp <= max_hp`**。
>
> **类的一大价值，就是替你守住不变量。**

---

## 📌 知识卡 2 · `min` 和 `max` 夹取 ⭐

```python runnable 一行把值夹进范围
print(min(150, 100))
print(max(-50, 0))

hp = 150
max_hp = 100
print(max(0, min(hp, max_hp)))

hp = -50
print(max(0, min(hp, max_hp)))
```

念一遍 `max(0, min(hp, max_hp))`：

- `min(hp, max_hp)` —— **不许超过上限**
- `max(0, ...)` —— **不许低于 0**

这个「夹取」写法非常常用，记住它。

```python runnable 加上保险的版本
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.max_hp = hp
        self.hp = hp

    def take_damage(self, amount):
        """受伤。血量最低到 0，不会变负。"""
        self.hp = max(0, self.hp - amount)

    def heal(self, amount):
        """回血。最多回到满血。"""
        self.hp = min(self.max_hp, self.hp + amount)


r = Role("星野樱", 100)

r.take_damage(500)
print(f"挨了 500 点：{r.hp}")

r.heal(9999)
print(f"治疗 9999：{r.hp} / {r.max_hp}")
```

---

## 📌 知识卡 3 · 挡住非法参数 ⭐

夹取解决了「结果越界」，但**参数本身不合法**还得单独挡：

```python runnable 负数伤害 = 偷偷治疗
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.max_hp = hp
        self.hp = hp

    def take_damage(self, amount):
        """受伤。伤害必须是正数。"""
        if amount < 0:
            raise ValueError(f"伤害不能是负数（收到 {amount}）")
        self.hp = max(0, self.hp - amount)


r = Role("星野樱", 100)
r.take_damage(30)
print(r.hp)

try:
    r.take_damage(-100)
except ValueError as e:
    print(f"  被挡住了：{e}")
```

Day 46 学的 `raise`，在方法里一样用。

> 💡 什么时候夹取、什么时候抛错？
>
> | 情况 | 怎么办 |
> |---|---|
> | **结果**超出范围（治疗溢出） | **夹取** —— 这是正常游戏逻辑 |
> | **参数**本身荒谬（负数伤害） | **抛错** —— 这是调用者写错了 |

---

## 📌 知识卡 4 · 返回「实际发生了多少」

夹取之后有个新问题：**说好治 100，实际只治了 20**。

```python runnable 返回实际值，而不是请求值
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.max_hp = hp
        self.hp = hp

    def heal(self, amount):
        """回血，返回**实际**回复量。"""
        if amount < 0:
            raise ValueError("治疗量不能是负数")
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before          # ← 实际变化了多少


r = Role("星野樱", 100)
r.hp = 80

healed = r.heal(50)
print(f"想治 50，实际治了 {healed}，现在 {r.hp}")

healed = r.heal(50)
print(f"又想治 50，实际治了 {healed}（已经满血了）")
```

**「先记下 before，改完再算差值」** —— 这是返回实际变化量的标准套路。

游戏里的「治疗溢出」提示、伤害统计，全靠它。

---

## 📌 知识卡 5 · 状态要一起维护

```python runnable alive 要跟着 hp 走
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.alive = True

    def take_damage(self, amount):
        """受伤，顺带更新存活状态。"""
        if amount < 0:
            raise ValueError("伤害不能是负数")
        self.hp = max(0, self.hp - amount)
        self.alive = self.hp > 0          # ← 每次改血量都同步
        return amount

    def heal(self, amount):
        """回血。⚠️ 倒下的角色不能自己回血。"""
        if not self.alive:
            print(f"  {self.name} 已经倒下了，治不了")
            return 0
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before


r = Role("星野樱", 100)
r.take_damage(150)
print(f"HP {r.hp}，活着吗：{r.alive}")
print(f"试着治疗：回了 {r.heal(50)} 点")
```

⚠️ **两个属性有关联时，改一个就要同步另一个** ——
否则会出现「血量 0 但 alive 还是 True」这种矛盾状态。

---

## 📌 知识卡 6 · 复活也要守规矩

```python runnable 复活方法
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.alive = True

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        self.alive = self.hp > 0
        return amount

    def revive(self, ratio=0.5):
        """复活，恢复到 max_hp 的一定比例。只对倒下的角色有效。"""
        if self.alive:
            print(f"  {self.name} 还活着，不用复活")
            return False
        self.hp = max(1, int(self.max_hp * ratio))
        self.alive = True
        print(f"  ✨ {self.name} 复活了！HP {self.hp}/{self.max_hp}")
        return True


r = Role("星野樱", 200)
r.revive()
r.take_damage(999)
r.revive()
print(r.hp, r.alive)
```

`max(1, ...)` 保证复活后至少有 1 血 —— **不然复活完还是死的**。

---

## 🛠 今天的任务 · 守规矩的角色类

在 `Role` 里实现这些方法，**每一个都要守住不变量**：

| 方法 | 保险要求 |
|---|---|
| `__init__(self, name, hp=100, atk=30)` | `hp` ≤ 0 时抛 `ValueError`；设 `max_hp` / `alive` / `level=1` |
| `take_damage(self, amount)` | 负数抛 `ValueError`；血量**不低于 0**；同步 `alive`；**返回实际扣血** |
| `heal(self, amount)` | 负数抛 `ValueError`；**不超过 max_hp**；倒下的不能治（返回 0）；**返回实际回血** |
| `attack(self, target)` | 自己倒下了不能攻击（返回 0）；返回造成的伤害 |
| `revive(self, ratio=0.5)` | 只对倒下的有效；复活后**至少 1 血**；返回 `True` / `False` |
| `level_up(self)` | 等级+1、max_hp+20、atk+5、**回满血**；返回新等级 |
| `hp_percent(self)` | 返回血量百分比（0~100 的整数） |
| `status(self)` | 返回一行状态，**含血条**（用 `hp_percent` 画） |

主流程要求：

- 造一个角色，打印初始状态
- 演示**过量伤害**（血量停在 0，不是负数）
- 演示**过量治疗**（停在满血，并打印「实际只回了 N 点」）
- 演示**倒下后治疗无效**
- 演示**复活**
- 演示**负数参数被 `raise` 挡住**（用 `try` 接住并打印）
- 演示**倒下的角色攻击无效**
- 用 `level_up` 升一级

> 💡 血条可以用 `"█" * (percent // 10)` 画，10 格。
