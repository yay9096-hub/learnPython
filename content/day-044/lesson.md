# Day 44 · 猜数字 · 函数版 🔧

> 「Day 14 你写了第一个猜数字游戏，Day 22 又做了进化版。
> 那时候所有代码挤在一起，加个功能就得从头读一遍。
>
> 今天用**函数**重写它。同样的功能，你会发现代码变得
> **一眼就能看懂哪块管什么**。」

---

## 🔍 第四章你拿到的武器

| 天 | 学到的 | 一句话 |
|---|---|---|
| D35 | `def` / 调用 | 给一段代码起个名字 |
| D36 | 参数 | 同一个函数，喂不同的料 |
| D37 | `return` | 把结果**交回来**，而不只是打印 |
| D38 | 默认参数 / 关键字参数 | 常用的值可以省着不写 |
| D39 | 多返回值 | 一次交回好几个结果 |
| D40 | 作用域 | 为什么函数里改了外面没变 |
| D41 | 函数库 / 单一职责 | 一个函数只做一件事 |
| D42 | 重构 / 命名 / 文档 | 让代码一周后还看得懂 |
| D43 | 递归 | 函数调用自己 |

**十天前你的代码是一长条，现在你能把它拆成零件再拼起来。**

---

## 🧩 复习卡 · 四个最容易忘的

### 1. 算的函数不要 print，打印的函数不要算

```python runnable 分工要清楚
def total_hp(team):
    """只算，不打印。"""
    return sum(m["hp"] for m in team)

def show_total(team):
    """只打印，不算。"""
    print(f"总血量：{total_hp(team)}")

team = [{"hp": 340}, {"hp": 280}]
show_total(team)
print(total_hp(team) * 2)
```

### 2. 数字改不动外面，列表字典改得动

```python runnable 又是这个对比
def bad(hp):
    hp = hp - 10

def good(role):
    role["hp"] = role["hp"] - 10

hp = 100
bad(hp)
print(hp)

role = {"hp": 100}
good(role)
print(role["hp"])
```

### 3. 默认值别用列表

```python runnable 用 None 才安全
def add(x, lst=None):
    if lst is None:
        lst = []
    lst.append(x)
    return lst

print(add(1))
print(add(2))
```

### 4. 递归必须有出口，而且要朝出口靠近

```python runnable 两个条件缺一不可
def count(n):
    if n <= 0:
        return
    print(n)
    count(n - 1)

count(3)
```

---

## 🎯 今天的作品 · 猜数字（函数版）

用**至少 7 个函数**重写猜数字游戏。

### 必须有的函数

| 函数 | 参数 | 返回 | 职责 |
|---|---|---|---|
| `pick_number(low, high)` | 范围 | 随机整数 | 出题 |
| `get_difficulty(name)` | 难度名 | **两个值**：`(上限, 次数)` | 简单 50/8、普通 100/7、困难 200/6 |
| `check_guess(guess, answer)` | 猜测、答案 | `"太大"` / `"太小"` / `"猜对了"` | 只判断，不打印 |
| `is_valid(text, high)` | 输入文本、上限 | **两个值**：`(是否合法, 说明)` | 校验输入 |
| `make_hint(answer)` | 答案 | 一句提示字符串 | 比如「是偶数」 |
| `show_result(won, answer, used)` | 是否赢、答案、用了几次 | 无 | 只负责打印结局 |
| `play(high, chances)` | 上限、次数 | `True` / `False` | 跑完一整局，返回赢没赢 |

### 硬性要求

- `check_guess` / `is_valid` / `make_hint` / `pick_number` / `get_difficulty`
  这五个**一个 `print` 都不许写**
- `play` 里要调用上面的函数，自己不重复实现判断逻辑
- 用完次数还没猜中要公布答案
- 输入不是数字要给提示，**而且不算消耗次数**
- 主流程：选难度 → 调 `play` → 根据返回值打印总结

> 💡 判题会喂一串固定输入，答案会被固定成一个已知数字，
> 所以放心写，随机不会让判题结果飘。
>
> 🏆 做完这一关第四章就通关了 —— 你已经会 Python 里最重要的抽象工具。
