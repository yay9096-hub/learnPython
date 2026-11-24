# Day 38 · 角色生成器 🎛

> 「`create_role(name, hp, mp, atk, defense, element, level)` ——
> 七个参数，每次调用都要全写一遍，太累了。
>
> 可大部分时候血量就是 100、等级就是 1。
> 今天学会：**常用的值给个默认，不写就用默认的**。」

---

## 📌 知识卡 1 · 给参数一个默认值

```python runnable 有默认值就能省着不写
def greet(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet("星野樱")
greet("月见琉璃", "早上好")
```

`greeting="你好"` 的意思是：**不给就用「你好」，给了就用你给的**。

多个参数都能有默认值：

```python runnable 一堆默认值
def create_role(name, hp=100, atk=50, element="无"):
    print(f"{name} · HP {hp} · ATK {atk} · {element}属性")

create_role("路人甲")
create_role("星野樱", 340, 88, "火")
create_role("小史莱姆", 30)
```

第一次只给了名字，其余三个全用默认值 —— **一行搞定一个路人角色**。

---

## 📌 知识卡 2 · ⚠️ 有默认值的必须放后面

```python runnable 顺序错了会报错（跑一下看）
def f(hp=100, name):
    print(name, hp)
```

`SyntaxError` —— Python 拦得很死。

想想为什么：如果允许 `f(hp=100, name)`，那 `f("星野樱")` 里的
「星野樱」到底是给 `hp` 还是给 `name`？**说不清，所以直接禁止。**

规矩：**没默认值的在前，有默认值的在后。**

```python runnable 正确的顺序
def f(name, hp=100):
    print(name, hp)

f("星野樱")
```

---

## 📌 知识卡 3 · 关键字参数：点名给值 ⭐

参数一多，按顺序数就容易错。可以**点名给**：

```python runnable 点名传参
def create_role(name, hp=100, atk=50, element="无"):
    print(f"{name} · HP {hp} · ATK {atk} · {element}属性")

create_role("星野樱", element="火")
create_role("水城凛", atk=110, hp=250)
```

第一次：只想改属性，中间的 `hp` `atk` 保持默认 —— **不点名根本做不到**。

第二次：`atk` 写在 `hp` 前面也没问题 —— **点名之后顺序就不重要了**。

其实你早就见过它：

```python runnable 这些都是关键字参数
print("a", "b", sep=" | ")
print("加载中", end="")
print()
nums = [3, 1, 2]
nums.sort(reverse=True)
print(nums)
```

`sep=` `end=` `reverse=` —— **全是关键字参数**，从 Day 6 用到现在。

---

## 📌 知识卡 4 · 混着用的规矩

```python runnable 位置参数在前，关键字参数在后
def create_role(name, hp=100, atk=50, element="无"):
    print(f"{name} · HP {hp} · ATK {atk} · {element}属性")

create_role("星野樱", 340, element="火")
```

⚠️ 反过来会报错：

```python runnable 关键字参数后面不能再跟位置参数
def create_role(name, hp=100, atk=50):
    print(name, hp, atk)

create_role(name="星野樱", 340)
```

**记住：点名的都放最后。**

---

## 📌 知识卡 5 · ⚠️ 默认值别用列表

这是 Python 一个非常有名的坑：

```python runnable 可变默认值的陷阱（跑两次看看）
def add_member(name, team=[]):
    team.append(name)
    return team

print(add_member("星野樱"))
print(add_member("月见琉璃"))
print(add_member("天野灯"))
```

**第二次调用居然带着第一次的人！**

原因：默认值 `[]` 在**函数定义时只创建一次**，之后每次调用都是同一个列表。

正确写法 —— 默认值用 `None`，进函数再造新的：

```python runnable 正确的写法
def add_member(name, team=None):
    if team is None:
        team = []
    team.append(name)
    return team

print(add_member("星野樱"))
print(add_member("月见琉璃"))
```

> 🧠 记住一条：**默认值只用不可变的东西**（数字、文字、`True`/`False`、`None`）。
> 想默认给个空列表或空字典，一律用 `None` + `if` 的写法。

---

## 📌 知识卡 6 · 默认值让函数好用得多

```python runnable 一个函数，多种用法
def show_bar(value, width=20, char="█", label=""):
    """画一条进度条。"""
    filled = int(value / 100 * width)
    bar = char * filled + "░" * (width - filled)
    print(f"{label}{bar} {value}%")

show_bar(70)
show_bar(45, label="HP ")
show_bar(90, width=30, char="=", label="加载 ")
```

同一个函数，三种完全不同的效果 —— **默认值负责「大多数情况」，
关键字参数负责「特殊情况」**。

---

## 🛠 今天的任务 · 角色生成器

做一个能应付各种情况的角色生成器：

| 函数 | 签名 | 说明 |
|---|---|---|
| `create_role` | `(name, hp=100, mp=50, atk=30, element="无", level=1)` | 返回一个**字典** |
| `show_role` | `(role, width=20, char="█")` | 打印角色卡，血条宽度可调 |
| `add_skill` | `(role, skill, skills=None)` | 给角色加技能，**必须用 None 默认值** |

主流程要求：

- 用**只给名字**的方式造一个路人角色
- 用**全部参数**造一个主角
- 用**关键字参数**造一个只改 `element` 和 `level` 的角色
- 至少给一个角色加 2 个技能
- `show_role` 至少调 3 次，其中一次改 `width` 或 `char`

> 💡 判题会直接调你的函数，检查默认值到底对不对。
> 参数名和默认值要**照表格来**。
