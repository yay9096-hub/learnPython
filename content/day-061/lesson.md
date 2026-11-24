# Day 61 · 让它好看点 🎴

> 「你写的类现在很能干，但用起来还是很别扭：
>
> - `print(角色)` 打出一串 `<__main__.Role object at 0x000001>`
> - 想知道队伍几个人，得写 `len(team.members)` 而不是 `len(team)`
> - 想判断两个角色是不是同一个，`==` 完全不好使
>
> 今天学**特殊方法**，让你的类用起来像 Python 自带的一样。」

---

## 📌 知识卡 1 · `print(对象)` 的惨状

```python runnable 默认打印出来是天书
class Role:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


r = Role("星野樱", 340)
print(r)
```

`<__main__.Role object at 0x...>` —— 完全没用。

以前你的对策是写个 `status()` 方法，每次 `print(r.status())`。
但为什么不能直接 `print(r)` 呢？

---

## 📌 知识卡 2 · `__str__` ⭐

```python runnable 让 print 变好看
class Role:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def __str__(self):
        """print(对象) 时会调用这个。必须返回字符串。"""
        return f"【{self.name}】HP {self.hp}"


r = Role("星野樱", 340)
print(r)
print(f"角色是：{r}")
print(str(r))
```

**`print(r)`、`f"{r}"`、`str(r)` 三种情况都会调用 `__str__`。**

⚠️ 它**必须返回字符串**：

```python runnable 返回别的会报错
class Role:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 123


print(Role("樱"))
```

> 🧠 前后两个下划线的方法叫**特殊方法**（也叫魔术方法）。
> 你不直接调用它们，**Python 在特定场合自动调用**。
>
> `__init__` 你早就在用了 —— 它就是「造对象时自动调用」。

---

## 📌 知识卡 3 · `__len__` 和 `__contains__`

```python runnable 让队伍支持 len() 和 in
class Team:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, role_name):
        self.members.append(role_name)

    def __len__(self):
        """len(队伍) 时调用。必须返回非负整数。"""
        return len(self.members)

    def __contains__(self, name):
        """「x in 队伍」时调用。返回 True / False。"""
        return name in self.members


t = Team("樱之队")
t.add("星野樱")
t.add("月见琉璃")

print(len(t))
print("星野樱" in t)
print("路人甲" in t)

if t:
    print("队伍不是空的")
```

对比一下：

| 有特殊方法 | 没有的话 |
|---|---|
| `len(t)` | `len(t.members)` |
| `"星野樱" in t` | `"星野樱" in t.members` |
| `if t:` | `if len(t.members) > 0:` |

**代码短了，而且读起来像在说话。**

> 💡 最后那个 `if t:` 有点意思 —— 有了 `__len__`，
> Python 会用「长度是不是 0」来判断真假。空队伍就是 `False`。

---

## 📌 知识卡 4 · `__eq__` —— 让 `==` 有意义 ⭐

```python runnable 默认的 == 没用
class Role:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp


a = Role("星野樱", 340)
b = Role("星野樱", 340)

print(a == b)
print(a == a)
```

两个一模一样的角色，`==` 却是 `False` ——
因为默认的 `==` 比的是「**是不是同一个对象**」，不是「内容一不一样」。

```python runnable 自己定义什么叫「相等」
class Role:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def __eq__(self, other):
        """名字一样就算同一个角色。"""
        if not isinstance(other, Role):
            return False
        return self.name == other.name


a = Role("星野樱", 340)
b = Role("星野樱", 100)
c = Role("月见琉璃", 340)

print(a == b)
print(a == c)
print(a == "星野樱")
```

⚠️ 开头那句 `isinstance` 检查很重要 —— 别人拿一个字符串来比，
不检查就会 AttributeError。

有了 `__eq__`，`in` 和 `.index()` 对列表也会跟着变聪明：

```python runnable __eq__ 让 in 也变聪明
class Role:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Role) and self.name == other.name


team = [Role("星野樱"), Role("月见琉璃")]

print(Role("星野樱") in team)
print(Role("路人甲") in team)
```

---

## 📌 知识卡 5 · `__repr__` —— 调试时看到的样子

```python runnable str 和 repr 的区别
class Role:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def __str__(self):
        return f"【{self.name}】"

    def __repr__(self):
        """给程序员看的。放进列表打印时用的是它。"""
        return f"Role({self.name!r}, {self.hp})"


r = Role("星野樱", 340)
print(r)
print([r, r])
print(repr(r))
```

**注意第二行** —— 打印列表时用的是 `__repr__` 而不是 `__str__`。

| 方法 | 给谁看 | 什么时候用 |
|---|---|---|
| `__str__` | **用户** | `print(对象)`、f-string |
| `__repr__` | **程序员** | 打印列表、调试器、交互式命令行 |

> 💡 惯例：`__repr__` 写成「**看着像能重新造出这个对象的代码**」，
> 比如 `Role('星野樱', 340)`。
>
> `{self.name!r}` 里的 `!r` 表示「用 repr 显示」，字符串会带上引号。

---

## 📌 知识卡 6 · 比较大小：`__lt__`

```python runnable 让角色能排序
class Role:
    def __init__(self, name, atk):
        self.name = name
        self.atk = atk

    def __str__(self):
        return f"{self.name}({self.atk})"

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        """「小于」的规则：按攻击力比。"""
        return self.atk < other.atk


team = [Role("樱", 88), Role("凛", 110), Role("灯", 72)]

print(sorted(team))
print(max(team))
print(min(team))
```

有了 `__lt__`，**`sorted` / `max` / `min` 都不用写 `key=` 了**。

（`lt` 是 less than 的缩写。还有 `__gt__` 大于、`__le__` 小于等于等等。）

---

## 🛠 今天的任务 · 好用的类

给 `Role` 和 `Team` 都装上特殊方法：

### `Role`

| 方法 | 要求 |
|---|---|
| `__str__` | 返回一行漂亮的卡片文字，含名字、HP、ATK |
| `__repr__` | 返回 `Role('名字', 血量, 攻击)` 这种样子 |
| `__eq__` | **名字相同**就算相等；跟非 Role 比返回 `False` |
| `__lt__` | 按**攻击力**比大小 |

### `Team`

| 方法 | 要求 |
|---|---|
| `__str__` | 返回队伍名和人数 |
| `__len__` | 返回成员数 |
| `__contains__` | 支持 `"星野樱" in team`（**按名字**判断） |
| `add(self, role)` | 普通方法，加成员 |

主流程要求：

- 直接 `print(角色)`，不许用 `.status()`
- 打印一个**装着角色的列表**，展示 `__repr__` 的效果
- 演示 `==`：两个同名不同血的角色相等；跟字符串比返回 `False`
- 演示 `Role("星野樱", ...) in 角色列表`
- 用 `sorted(team_list)` 排序，**不写 `key=`**
- 用 `max()` / `min()` 找最强最弱，**不写 `key=`**
- 演示 `len(team)` 和 `"名字" in team`
- 演示 `if team:` 判断队伍空不空（造一个空队伍对比）

> ⚠️ 主流程里**不许出现 `.members`** —— 那正是特殊方法要帮你藏起来的东西。
