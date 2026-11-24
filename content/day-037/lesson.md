# Day 37 · 骰子与判定 🎲

> 「昨天的 `deal_damage()` 有个大问题：
> 它把伤害**打印出来**了，但你**拿不到那个数字**。
>
> 想拿伤害去扣血、去比大小、去累加？做不到。
> 今天学 `return` —— 让函数把结果**交回来**。」

---

## 📌 知识卡 1 · 打印 ≠ 返回 ⭐

这是今天最重要的一件事，先感受一下区别：

```python runnable 只打印，拿不到
def add_print(a, b):
    print(a + b)

result = add_print(3, 5)
print("接到的是：", result)
```

打印出来了 8，但 `result` 是 `None` —— **什么都没接到**。

```python runnable return 才交得回来
def add_return(a, b):
    return a + b

result = add_return(3, 5)
print("接到的是：", result)
print("还能继续算：", result * 10)
```

| | `print(x)` | `return x` |
|---|---|---|
| 做什么 | 显示给人看 | **交回给代码** |
| 能接住吗 | ❌ 不能 | ✅ 能 |
| 能继续算吗 | ❌ 不能 | ✅ 能 |

> 🧠 一句话：**`print` 是说给人听，`return` 是交给程序。**

---

## 📌 知识卡 2 · 没写 `return` 就返回 `None`

```python runnable 悄悄返回 None
def greet(name):
    print(f"你好，{name}")

x = greet("星野樱")
print(x)
print(type(x))
```

`None` 是 Python 里表示「什么都没有」的特殊值。

⚠️ 这就是 Day 24 那个坑的原因 —— `bag.append(x)` 也没有 return，
所以 `bag = bag.append(x)` 会把背包变成 `None`。

---

## 📌 知识卡 3 · 有了返回值，就能接着用

```python runnable 返回值能参与后续运算
def deal_damage(atk, defense):
    """算出伤害，最低 1 点。"""
    damage = atk - defense
    if damage < 1:
        damage = 1
    return damage

hp = 500
hp = hp - deal_damage(88, 25)
print(f"敌人剩余血量：{hp}")

hp = hp - deal_damage(110, 25)
print(f"敌人剩余血量：{hp}")
```

**扣血这件事，昨天的版本根本做不到** —— 因为拿不到伤害值。

返回值还能直接塞进别的函数：

```python runnable 函数套函数
def deal_damage(atk, defense):
    return max(atk - defense, 1)

print(f"伤害是 {deal_damage(88, 25)} 点")
total = deal_damage(88, 25) + deal_damage(70, 30)
print(f"两次共 {total} 点")
```

> 💡 `max(a, b)` 返回较大的那个 —— 用它一行就能做保底，比 `if` 短。
> 还有 `min(a, b)` 返回较小的。

---

## 📌 知识卡 4 · `return` 会立刻结束函数 ⚠️

```python runnable return 后面的不执行
def check(hp):
    print("开始检查")
    return "还活着"
    print("这一行永远跑不到")

print(check(100))
```

`return` 一执行，函数**当场结束**，后面的代码直接跳过。

这个特性很有用 —— 可以**提前返回**：

```python runnable 提前返回，省掉 else
def grade(score):
    """把分数转成等第。"""
    if score >= 90:
        return "优秀"
    if score >= 60:
        return "及格"
    return "再努力一下"

print(grade(95))
print(grade(70))
print(grade(30))
```

三个 `if`，没有一个 `else` —— 因为 `return` 一执行就结束了，
后面的判断根本没机会跑。**这种写法很常见，读起来比嵌套 else 清爽。**

---

## 📌 知识卡 5 · 返回值可以是任何类型

```python runnable 返回布尔值
def is_alive(hp):
    """血量大于 0 就还活着。"""
    return hp > 0

print(is_alive(100))
print(is_alive(0))

if is_alive(50):
    print("继续战斗！")
```

⚠️ 注意 `return hp > 0` —— **比较本身就是 True/False**，不用写成：

```python
if hp > 0:        # 啰嗦的写法
    return True
else:
    return False
```

返回列表、字典也行：

```python runnable 返回一个列表
def make_team(n):
    """造一支 n 人的队伍。"""
    team = []
    for i in range(n):
        team.append(f"学员{i + 1}号")
    return team

print(make_team(3))
print(len(make_team(5)))
```

---

## 📌 知识卡 6 · 随机数配合返回值

```python runnable 掷骰子
import random

def roll(sides):
    """掷一个 sides 面的骰子，返回点数。"""
    return random.randint(1, sides)

print(roll(6))
print(roll(20))

total = roll(6) + roll(6)
print(f"两颗骰子合计 {total} 点")
```

因为有返回值，才能**把两次结果加起来** —— 这是 `print` 版做不到的。

---

## 🛠 今天的任务 · 骰子判定系统

做一套跑团式的判定系统，**全部用 `return`**：

| 函数 | 参数 | 返回什么 |
|---|---|---|
| `roll(sides)` | 骰子面数 | 1 到 sides 之间的随机整数 |
| `deal_damage(atk, defense)` | 攻击、防御 | 伤害值，**最低 1** |
| `is_alive(hp)` | 血量 | `True` / `False` |
| `grade(score)` | 分数 | `"优秀"` / `"及格"` / `"再努力一下"` |
| `battle_report(name, hp)` | 名字、血量 | **一个字符串**（不是 print！） |

主流程要求：

- 掷 3 次骰子，把点数**加起来**打印总和
- 用 `deal_damage` 的返回值**真的扣血**，连续攻击 3 次，每次打印剩余血量
- 用 `is_alive` 判断敌人死没死
- 用 `grade` 转换至少 3 个不同分数
- 打印 `battle_report` 返回的字符串

> ⚠️ 这五个函数里**一个 `print` 都不要写** —— 它们只负责算和返回，
> 打印全部交给主流程。这是函数设计的一条重要原则。
