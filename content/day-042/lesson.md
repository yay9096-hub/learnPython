# Day 42 · 整理你的工具箱 🧹

> 「你的代码能跑了。但『能跑』只是及格线。
>
> 今天做一件所有程序员每天都在做、却几乎没人教的事：
> **把能跑的代码，整理成一周后自己还看得懂的代码。**
>
> 这件事有个专门的名字，叫**重构**。」

---

## 📌 知识卡 1 · 先看一段「能跑但很糟」的代码

```python runnable 能跑，但读起来要命
def f(a, b):
    c = a - b
    if c < 1:
        c = 1
    if c > 999:
        c = 999
    return c

print(f(88, 25))
print(f(10, 99))
```

它完全正确。但是：

- `f` 是干嘛的？`a` `b` `c` 又是什么？
- `999` 是什么意思？为什么是 999 不是 1000？
- 一个月后你还记得吗？

整理之后：

```python runnable 一模一样的逻辑，但读得懂了
MIN_DAMAGE = 1
MAX_DAMAGE = 999


def deal_damage(atk, defense):
    """按「攻击力 - 防御力」算伤害，并夹在合法范围内。"""
    damage = atk - defense
    if damage < MIN_DAMAGE:
        damage = MIN_DAMAGE
    if damage > MAX_DAMAGE:
        damage = MAX_DAMAGE
    return damage


print(deal_damage(88, 25))
print(deal_damage(10, 99))
```

**逻辑一个字没改，可读性天差地别。**

---

## 📌 知识卡 2 · 消灭「魔法数字」⭐

代码里裸露的数字叫**魔法数字** —— 因为除了写的人，谁也不知道它从哪冒出来的。

```python runnable 魔法数字满天飞（不好）
def check(hp):
    if hp > 400:
        return "健康"
    if hp > 150:
        return "受伤"
    return "危险"

print(check(500))
```

```python runnable 提取成常量（好）
HEALTHY_HP = 400
WOUNDED_HP = 150


def check(hp):
    """按血量返回状态描述。"""
    if hp > HEALTHY_HP:
        return "健康"
    if hp > WOUNDED_HP:
        return "受伤"
    return "危险"


print(check(500))
```

好处有三个：

1. **看得懂** —— `HEALTHY_HP` 自带解释
2. **好改** —— 想调平衡性，只改文件顶部一行
3. **不会漏** —— 同一个数字在五处用到时，改常量就全改了

> 🧠 惯例：**常量全大写 + 下划线，写在文件最上面（import 之后）。**
> Python 不会阻止你改它，全大写只是在告诉人「这个别改」。

---

## 📌 知识卡 3 · docstring 写什么

```python runnable 三种质量的说明
def deal_damage(atk, defense):
    """伤害。"""
    return max(atk - defense, 1)


def deal_damage2(atk, defense):
    """这个函数用 atk 减去 defense 然后如果小于 1 就返回 1 否则返回结果。"""
    return max(atk - defense, 1)


def deal_damage3(atk, defense):
    """按「攻击力 - 防御力」算伤害，最低保底 1 点。"""
    return max(atk - defense, 1)


print(deal_damage3.__doc__)
```

- 第一个太短，等于没说
- 第二个是把代码翻译了一遍，**代码本身就能看出来**，没价值
- 第三个说的是**「为什么」和「规则」** —— 这才有用

> 💡 好的 docstring 回答的是「**这个函数解决什么问题**」，
> 而不是「这个函数的代码怎么写的」。

---

## 📌 知识卡 4 · 好名字胜过好注释

```python runnable 名字说清楚了就不用注释
def a(x):
    return x * 0.15


def calculate_crit_bonus(base_damage):
    """暴击加成 = 基础伤害的 15%。"""
    return base_damage * CRIT_RATE


CRIT_RATE = 0.15

print(calculate_crit_bonus(100))
```

命名的几条实用规矩：

| 场合 | 写法 | 例子 |
|---|---|---|
| 函数 | 小写 + 下划线，**动词开头** | `deal_damage`、`find_member` |
| 返回真假的函数 | `is_` / `has_` / `can_` 开头 | `is_alive`、`has_skill` |
| 变量 | 小写 + 下划线，**名词** | `total_hp`、`best_score` |
| 常量 | **全大写** | `MAX_HP`、`CRIT_RATE` |
| 循环里的临时变量 | 短的可以 | `for m in team`、`for i in range(5)` |

⚠️ 别用 `l`（小写 L）、`O`（大写 o）当变量名 —— 跟 1 和 0 分不清。

---

## 📌 知识卡 5 · 一个函数不该太长

一个函数超过 **20 行**，通常就是在干好几件事了。

```python runnable 长函数拆开（看拆之后多清爽）
MAX_ROUNDS = 3


def calc_damage(atk, defense):
    """算单次伤害，保底 1 点。"""
    return max(atk - defense, 1)


def show_round(n, damage, hp_left):
    """播报一个回合。"""
    print(f"  第 {n} 回合：造成 {damage} 点，敌人剩 {hp_left}")


def battle(atk, enemy_hp, enemy_def):
    """打 MAX_ROUNDS 个回合，返回敌人剩余血量。"""
    for i in range(MAX_ROUNDS):
        damage = calc_damage(atk, enemy_def)
        enemy_hp = enemy_hp - damage
        show_round(i + 1, damage, enemy_hp)
    return enemy_hp


left = battle(88, 500, 25)
print(f"战斗结束，敌人剩 {left} 血")
```

`battle` 只有 5 行，一眼看完 —— 因为细节都交给小函数了。

---

## 📌 知识卡 6 · 文件的组织顺序

一个整齐的 Python 文件，从上到下是这个顺序：

```
1. 文件说明（三引号）
2. import
3. 常量（全大写）
4. 函数定义（相关的放一起）
5. 主流程
```

```python runnable 一个整齐的文件长这样
"""伤害计算模块 · Day 42 示例。"""
import random

MIN_DAMAGE = 1
CRIT_RATE = 1.5


def deal_damage(atk, defense):
    """按「攻击力 - 防御力」算伤害，最低保底 1 点。"""
    return max(atk - defense, MIN_DAMAGE)


def deal_crit(atk, defense):
    """暴击伤害 = 普通伤害 × 倍率。"""
    return round(deal_damage(atk, defense) * CRIT_RATE, 1)


print(deal_damage(88, 25))
print(deal_crit(88, 25))
```

---

## 🛠 今天的任务 · 重构战斗系统

`starter.py` 里给了你一段**能跑但很糟**的代码。你的任务是**把它整理干净**，
功能一个字不能改。

要求：

| # | 要求 | 说明 |
|---|---|---|
| 1 | 文件开头写一句三引号说明 | 说明这个文件是干什么的 |
| 2 | 提取至少 4 个常量 | 全大写，放在文件上部 |
| 3 | 所有函数改成有意义的名字 | 动词开头，不许 `f` `g` `h` |
| 4 | 所有参数和变量改成有意义的名字 | 不许 `a` `b` `c` `x` `y` |
| 5 | 每个函数写 docstring | 说「解决什么问题」，不是翻译代码 |
| 6 | 返回真假的函数用 `is_` 开头 | 比如 `is_alive` |
| 7 | 代码里不许再有裸露的魔法数字 | 除了 0 和 1 |
| 8 | 输出结果和原来完全一致 | 功能不能变 |

> 💡 这是程序员的日常工作。**能跑的代码只是原材料，整理过的代码才是作品。**
