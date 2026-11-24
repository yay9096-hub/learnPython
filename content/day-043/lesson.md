# Day 43 · 分形树 🌳

> 「今天这一课有点像魔法。
>
> 你会写一个**只有十几行**的函数，画出一棵有几百根树枝的树。
> 秘诀是一件听起来很怪的事：**让函数调用它自己**。」

---

## 📌 知识卡 1 · 函数可以调用自己

```python runnable 倒数
def countdown(n):
    """从 n 倒数到 1。"""
    if n <= 0:
        print("发射！🚀")
        return
    print(n)
    countdown(n - 1)

countdown(5)
```

看第 7 行 —— `countdown` **在自己的函数体里调用了自己**。

这叫**递归**（recursion）。

跟着走一遍：

```
countdown(5) 打印 5，然后调用 countdown(4)
  countdown(4) 打印 4，然后调用 countdown(3)
    countdown(3) 打印 3，然后调用 countdown(2)
      countdown(2) 打印 2，然后调用 countdown(1)
        countdown(1) 打印 1，然后调用 countdown(0)
          countdown(0) 发现 n <= 0，打印「发射」然后 return
```

**一层层进去，到底之后再一层层回来。**

---

## 📌 知识卡 2 · ⚠️ 必须有出口

```python runnable 没有出口会怎样（跑一下看）
def forever(n):
    print(n)
    forever(n - 1)

forever(3)
```

`RecursionError` —— 它永远停不下来，Python 只好喊停。

**递归的两条铁律：**

| 铁律 | 说明 |
|---|---|
| ① 必须有**出口条件** | 满足了就 `return`，不再调用自己 |
| ② 每次调用参数要**朝出口靠近** | 写 `f(n - 1)` 不是 `f(n)` |

```python runnable 对比：出口和递减，缺一不可
def good(n):
    if n <= 0:        # ① 出口
        return
    print(n)
    good(n - 1)       # ② 朝出口靠近

good(3)
```

> 🧠 写递归时先写出口，再写递归调用。**顺序反过来最容易写出死循环。**

---

## 📌 知识卡 3 · 递归也能返回值

```python runnable 阶乘
def factorial(n):
    """算 n 的阶乘：n × (n-1) × ... × 1。"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))
print(factorial(10))
```

`factorial(5)` = `5 * factorial(4)` = `5 * 4 * factorial(3)` = … = `5*4*3*2*1` = 120

```python runnable 数字总和
def total(n):
    """1 + 2 + ... + n。"""
    if n <= 0:
        return 0
    return n + total(n - 1)

print(total(10))
print(total(100))
```

⚠️ 这些用循环也能写，而且更快。**递归的真正价值在下面这种场景**。

---

## 📌 知识卡 4 · 树：天生适合递归 ⭐

看一棵树的结构：

```
        一根树枝
        ↙      ↘
    一根树枝   一根树枝
    ↙   ↘      ↙   ↘
   ...  ...   ...  ...
```

**每一根树枝，都长着两根更小的树枝。**

「树枝」这个东西是**用自己定义自己**的 —— 这正是递归的形状。

```python runnable 文字版的树（先感受结构）
def branch(depth, prefix=""):
    """打印一棵文字树。"""
    if depth <= 0:
        return
    print(prefix + "├─ 树枝")
    branch(depth - 1, prefix + "│  ")
    branch(depth - 1, prefix + "│  ")

branch(3)
```

一个函数，`depth` 减到 0 自动停 —— 你不用管一共要画几根。

---

## 📌 知识卡 5 · 用 turtle 画出来 ⭐

```python runnable 真·分形树
import turtle

def tree(length, depth):
    """画一根长 length 的树枝，然后在末端长出两根小的。"""
    if depth == 0:
        return

    turtle.forward(length)          # 画这根树枝

    turtle.left(30)                 # 向左偏
    tree(length * 0.7, depth - 1)   # 长出左边的小树
    turtle.right(60)                # 转向右
    tree(length * 0.7, depth - 1)   # 长出右边的小树
    turtle.left(30)                 # 转回来

    turtle.backward(length)         # 退回起点（关键！）

turtle.speed(0)
turtle.pensize(2)
turtle.pencolor("#5B3A2E")
turtle.penup()
turtle.goto(0, -180)
turtle.left(90)
turtle.pendown()

tree(90, 6)
turtle.hideturtle()
```

把 `depth` 从 6 改成 3、8、10 各跑一次，感受一下变化。

### 三个关键点

**① `turtle.backward(length)` 不能少**
画完这一支的所有分叉后，海龟要**退回到起点**，
不然下一根树枝会从错误的位置开始长。

**② 角度要转回来**
`left(30)` → 画左边 → `right(60)` → 画右边 → `left(30)`
最后那个 `left(30)` 把朝向**还原**成进来时的样子。

> 🧠 记住一条：**递归函数结束时，要把状态恢复成刚进来的样子。**
> 位置退回去、角度转回来 —— 这样上一层才能继续正常工作。

**③ 每层变短**
`length * 0.7` 让树枝越往上越细 —— 这就是「朝出口靠近」的视觉版。

---

## 📌 知识卡 6 · 让树好看一点

```python runnable 带颜色和粗细变化
import turtle

def tree(length, depth):
    """越往末梢越细越绿的分形树。"""
    if depth == 0:
        return

    if depth <= 2:
        turtle.pencolor("#7BC96F")      # 末梢是叶子的绿
    else:
        turtle.pencolor("#5B3A2E")      # 主干是木头色
    turtle.pensize(depth)

    turtle.forward(length)
    turtle.left(28)
    tree(length * 0.72, depth - 1)
    turtle.right(56)
    tree(length * 0.72, depth - 1)
    turtle.left(28)
    turtle.backward(length)

turtle.speed(0)
turtle.bgcolor("#FDF9FF")
turtle.penup()
turtle.goto(0, -200)
turtle.left(90)
turtle.pendown()

tree(100, 7)
turtle.hideturtle()
```

---

## 🛠 今天的任务 · 我的分形森林

| 要求 | 说明 |
|---|---|
| `countdown(n)` | 递归倒数，练手用 |
| `factorial(n)` | 递归阶乘，返回值版 |
| `tree(length, depth)` | 递归画树，**必须有出口条件** |
| 树至少 6 层 | `depth >= 6` |
| 粗细随层数变化 | 用 `turtle.pensize(depth)` |
| 末梢和主干**颜色不同** | 用 `if depth <= 2:` 区分 |
| 每层树枝变短 | 乘一个小于 1 的系数 |
| 画完要退回起点 | `turtle.backward(length)` |
| 打印 `factorial(5)` 的结果 | 应该是 120 |

> 💡 树画歪了、断了、越长越乱？八成是漏了 `backward` 或者角度没转回来。
> **递归函数要「来时什么样，走时还什么样」。**
