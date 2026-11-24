# Day 55 · 你的第一个类 🏗

> 「Day 29 你用字典存角色，Day 41 又写了一堆函数处理它：
>
> ```python
> role = {"name": "星野樱", "hp": 340}
> show_role(role)
> deal_damage(role, 50)
> ```
>
> 数据在这儿、处理它的函数在那儿，两边靠**约定**连着。
> 一旦有人往字典里塞了个 `hp` 拼错的键，全线崩溃。
>
> 今天学会把**数据和本事装进同一个盒子**。」

---

## 📌 知识卡 1 · 字典版的三个毛病

```python runnable 字典版：能用，但脆
role = {"name": "星野樱", "hp": 340}

print(role["name"])
print(role["hpp"])
```

毛病一：**键名打错了才发现**，而且报错发生在很远的地方。

```python runnable 毛病二：谁也拦不住你造个残废角色
role = {"nmae": "星野樱"}
print(role)
```

毛病三：**处理它的函数散落各处**，新人不知道有哪些能用。

---

## 📌 知识卡 2 · `class` —— 造一个新「类型」⭐

```python runnable 你的第一个类
class Role:
    """一个游戏角色。"""

    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


sakura = Role("星野樱", 340)

print(sakura)
print(sakura.name)
print(sakura.hp)
print(type(sakura))
```

三件事发生了：

1. `class Role:` —— 定义了一个**新类型**，叫 Role
2. `Role("星野樱", 340)` —— 造出一个**实例**（一个具体的角色）
3. `sakura.name` —— 用**点号**取属性，不用方括号和引号了

> 🧠 打个比方：
> **类是「饼干模具」，实例是「用模具压出来的饼干」。**
> 一个模具能压出无数块饼干，每块都独立。

---

## 📌 知识卡 3 · `__init__` 和 `self` ⭐

这是今天最需要理解的两个东西。

```python runnable 看清楚 __init__ 什么时候跑
class Role:
    def __init__(self, name, hp):
        print(f"  正在造一个角色：{name}")
        self.name = name
        self.hp = hp


print("造第一个：")
a = Role("星野樱", 340)

print("造第二个：")
b = Role("月见琉璃", 280)
```

**`__init__` 在每次 `Role(...)` 时自动执行**，用来「初始化」这个新对象。

（前后各两个下划线，是 Python 的特殊方法约定，读作「dunder init」。）

### `self` 是什么

```python runnable self 就是「这个对象自己」
class Role:
    def __init__(self, name, hp):
        self.name = name        # 把参数 name 存进「这个对象」
        self.hp = hp


a = Role("星野樱", 340)
b = Role("月见琉璃", 280)

print(a.name, a.hp)
print(b.name, b.hp)
```

造 `a` 的时候，`self` 就是 `a`；造 `b` 的时候，`self` 就是 `b`。

**所以两个角色的血量互不影响** —— 各存各的。

⚠️ `self` 必须是**第一个参数**，而且调用时**不用你传**：

```python runnable 忘了 self 会报错
class Role:
    def __init__(name, hp):
        pass

r = Role("樱", 340)
```

> 🧠 一句话：
> **`self.xxx` 是「这个对象的 xxx」，`xxx` 是「函数里的临时变量」。**

---

## 📌 知识卡 4 · 每个实例都是独立的

```python runnable 改一个不影响另一个
class Role:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


a = Role("星野樱", 340)
b = Role("月见琉璃", 280)

a.hp = a.hp - 100

print(f"{a.name}: {a.hp}")
print(f"{b.name}: {b.hp}")
```

属性可以**直接改**，用点号赋值就行。

---

## 📌 知识卡 5 · 默认参数一样能用

```python runnable 类也能有默认值
class Role:
    """一个游戏角色。除了名字，其余都有默认值。"""

    def __init__(self, name, hp=100, mp=50, atk=30, element="无"):
        self.name = name
        self.hp = hp
        self.max_hp = hp          # 顺手记下满血值
        self.mp = mp
        self.atk = atk
        self.element = element
        self.alive = True


passerby = Role("路人甲")
hero = Role("星野樱", 340, 180, 88, "火")

print(f"{passerby.name}: HP {passerby.hp} ATK {passerby.atk}")
print(f"{hero.name}: HP {hero.hp} ATK {hero.atk} [{hero.element}]")
```

Day 38 学的默认参数、关键字参数，在 `__init__` 里**完全一样**用。

注意 `self.max_hp = hp` —— **属性不一定都来自参数**，
可以在 `__init__` 里现算、现设。

---

## 📌 知识卡 6 · 一堆对象放进列表

```python runnable 对象也能装进列表
class Role:
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk


team = [
    Role("星野樱", 340, 88),
    Role("月见琉璃", 280, 95),
    Role("天野灯", 310, 72),
]

for r in team:
    print(f"  {r.name}  HP {r.hp}  ATK {r.atk}")

print(f"总血量：{sum(r.hp for r in team)}")

strongest = max(team, key=lambda r: r.atk)
print(f"最强：{strongest.name}")
```

**第三章学的排序、统计、筛选，对对象列表完全一样用** ——
唯一的区别是 `r["hp"]` 变成了 `r.hp`。

---

## 📌 知识卡 7 · 字典 vs 类，什么时候用哪个

| | 字典 | 类 |
|---|---|---|
| 结构固定吗 | 随便加键 | **固定**，一眼看清有哪些属性 |
| 带不带本事 | 只有数据 | **数据 + 方法**（明天学） |
| 写起来 | 快 | 要先定义 |
| 适合 | 临时数据、配置、json | **反复出现的、有行为的东西** |

> 💡 一条实用判断：
> **如果你为某个字典写了三个以上的专用函数，它就该变成类了。**

---

## 🛠 今天的任务 · 角色类

| 要求 | 说明 |
|---|---|
| 定义 `Role` 类 | 带 docstring |
| `__init__(self, name, hp=100, mp=50, atk=30, element="无")` | 参数和默认值照抄 |
| 属性至少 7 个 | `name` `hp` `max_hp` `mp` `atk` `element` `alive` |
| `max_hp` 等于初始 hp | 在 `__init__` 里设 |
| `alive` 初始为 `True` | |
| 造至少 4 个角色 | 一个只给名字、一个全给、一个用关键字参数 |
| 全部装进列表遍历打印 | 一行一个，含名字/HP/ATK/属性 |
| 用 `sum` 算总血量 | |
| 用 `max(..., key=...)` 找最强 | |
| 直接改一个角色的 hp | 改完再打印，证明只影响它自己 |

> ⚠️ 今天**先不写方法**（明天学）。`Role` 里只有 `__init__`。
> 打印、统计都在类外面用普通代码做。
