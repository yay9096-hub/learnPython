# Day 39 · 属性生成器 📦

> 「`return` 只能交回**一个**东西？
> 那生成角色属性怎么办 —— 血量、魔力、攻击力，一次要三个。
>
> 好消息：Python 的 `return` 后面**可以跟好几个值**。」

---

## 📌 知识卡 1 · 逗号隔开就能返回多个

```python runnable 一次返回三个
def make_stats():
    """随便生成一组属性。"""
    return 340, 180, 88

result = make_stats()
print(result)
print(type(result))
```

看清楚 —— 返回的其实是**一个元组** `(340, 180, 88)`。

Day 33 学的元组，今天派上用场了。

---

## 📌 知识卡 2 · 用解包接住 ⭐

```python runnable 左边写同样多的变量
def make_stats():
    return 340, 180, 88

hp, mp, atk = make_stats()

print(f"HP {hp} · MP {mp} · ATK {atk}")
```

这正是 Day 33 的**解包**：右边有几个值，左边就写几个变量。

⚠️ 个数必须对上：

```python runnable 个数不对会报错
def make_stats():
    return 340, 180, 88

hp, mp = make_stats()
```

只想要其中一个？用下划线 `_` 占位（约定俗成的「我不关心这个」）：

```python runnable 用 _ 跳过不要的
def make_stats():
    return 340, 180, 88

hp, _, _ = make_stats()
print(f"我只关心血量：{hp}")
```

---

## 📌 知识卡 3 · 配合随机数

```python runnable 随机属性生成器
import random

def roll_stats(level):
    """按等级随机生成三围。"""
    hp = random.randint(50, 100) + level * 20
    mp = random.randint(20, 60) + level * 10
    atk = random.randint(10, 30) + level * 5
    return hp, mp, atk

hp, mp, atk = roll_stats(10)
print(f"10 级角色：HP {hp} · MP {mp} · ATK {atk}")

hp2, mp2, atk2 = roll_stats(1)
print(f"1 级角色：HP {hp2} · MP {mp2} · ATK {atk2}")
```

多跑几次 —— 每次属性都不一样，但等级高的整体更强。

---

## 📌 知识卡 4 · 返回值可以拿去继续算

```python runnable 接住之后接着用
import random

def roll_stats(level):
    hp = random.randint(50, 100) + level * 20
    mp = random.randint(20, 60) + level * 10
    atk = random.randint(10, 30) + level * 5
    return hp, mp, atk

hp, mp, atk = roll_stats(10)
total = hp + mp + atk

print(f"三围总和：{total}")
if total > 400:
    print("这是个不错的角色！")
else:
    print("有点弱，要不要重骰？")
```

---

## 📌 知识卡 5 · ⚠️ 超过三个就该用字典了

```python runnable 五个返回值：数不清了
def make_role():
    return "星野樱", 340, 180, 88, "火"

name, hp, mp, atk, element = make_role()
print(name, hp, mp, atk, element)
```

能用，但有两个毛病：

1. 调用的人**必须记住顺序** —— 第三个到底是 mp 还是 atk？
2. 想加一个属性，**所有调用点都要改**

字典版就没这问题：

```python runnable 字典版：自带标签
def make_role():
    """返回一个角色字典，字段名自带说明。"""
    return {
        "name": "星野樱",
        "hp": 340,
        "mp": 180,
        "atk": 88,
        "element": "火",
    }

role = make_role()
print(role["name"], role["hp"])
print(role)
```

> 🧠 经验法则：
> **2~3 个值 → 直接返回多个**（`return hp, mp`）
> **4 个以上，或者以后可能会加 → 返回字典**

---

## 📌 知识卡 6 · 常见搭配：返回「结果 + 说明」

一个特别实用的模式 —— 同时返回「成功没成功」和「为什么」：

```python runnable 结果 + 原因
def check_login(name, password):
    """返回 (是否通过, 说明文字)。"""
    if len(name) < 2:
        return False, "名字太短了"
    if password != "sakura":
        return False, "口令不对"
    return True, "验证通过，欢迎回来"

ok, msg = check_login("樱", "sakura")
print(ok, msg)

ok, msg = check_login("星野樱", "banana")
print(ok, msg)

ok, msg = check_login("星野樱", "sakura")
print(ok, msg)

if ok:
    print("→ 放行")
```

只返回 `True/False` 的话，出了问题**不知道为什么**。
带上一句说明，调用的人就能给出有用的提示。

---

## 🛠 今天的任务 · 角色属性生成器

| 函数 | 返回什么 |
|---|---|
| `roll_stats(level)` | **三个值**：hp、mp、atk（跟等级挂钩的随机数） |
| `judge_stats(hp, mp, atk)` | **两个值**：`(评级文字, 总和)`，总和 ≥400「优秀」、≥300「普通」、其余「偏弱」 |
| `make_role(name, level)` | **一个字典**，至少含 name / level / hp / mp / atk / rank 六个字段，内部要调用上面两个函数 |
| `check_name(name)` | **两个值**：`(是否合法, 说明文字)`，名字长度 2~8 算合法 |

主流程要求：

- 用解包接住 `roll_stats` 的三个返回值并打印
- 用解包接住 `judge_stats` 的两个返回值并打印
- 用 `make_role` 造**至少 3 个**角色，遍历打印它们的字典
- 用 `check_name` 验 3 个名字：一个太短、一个太长、一个正常，把说明都打出来

> 💡 判题会直接调你的函数检查返回的**个数和类型**，所以返回几个要严格照表格。
