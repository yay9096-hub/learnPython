# Day 19 · 星空生成器 ✨

> 「今天把三样东西拧在一起：**循环**（Day 15）、**随机**（Day 10）、**画笔**（Day 8）。
> 结果是 —— 每次运行都不一样的一整片星空。」

---

## 📌 知识卡 1 · 循环 + 随机坐标 = 撒一把点

```python runnable 随机撒 50 颗星（多跑几次）
import random
import turtle

turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.penup()

for i in range(50):
    x = random.randint(-250, 250)
    y = random.randint(-190, 190)
    turtle.goto(x, y)
    turtle.dot(4, "white")
```

三步循环体：

1. 随机挑一个坐标
2. 传送过去（记得 `penup()`，不然会拖出线）
3. 点一个点

⚠️ `penup()` 写在循环**外面**就够了 —— 抬起来之后一直是抬着的。

> 📐 画布是 520×420，所以坐标范围大约是
> x: -260 ~ 260，y: -210 ~ 210。留点边距更好看。

---

## 📌 知识卡 2 · 随机大小 = 远近层次

所有星星一样大就很假。让大小也随机：

```python runnable 有大有小
import random
import turtle

turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.penup()

for i in range(80):
    turtle.goto(random.randint(-250, 250), random.randint(-190, 190))
    turtle.dot(random.randint(2, 9), "white")
```

大的像近处的亮星，小的像远处的 —— 一下就有纵深了。

---

## 📌 知识卡 3 · 随机颜色

Day 10 学过 RGB 三个随机数。这里再加个技巧：**让颜色偏冷**，星空才自然。

```python runnable 冷色调星星
import random
import turtle

turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.penup()

for i in range(80):
    r = random.randint(180, 255)
    g = random.randint(180, 255)
    b = 255                              # 蓝色拉满，整体偏冷
    turtle.goto(random.randint(-250, 250), random.randint(-190, 190))
    turtle.dot(random.randint(2, 8), (r, g, b))
```

把 `b = 255` 改成 `b = random.randint(100, 255)` 看看区别。

也可以从一个列表里随机挑（Day 16 的 `colors[i % 4]` 是轮流，这里是随机）：

```python runnable 从色板里随机挑
import random
import turtle

turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.penup()

palette = ["#FFFFFF", "#FFE9A8", "#A8D8FF", "#FFC8E4"]

for i in range(60):
    turtle.goto(random.randint(-250, 250), random.randint(-190, 190))
    turtle.dot(random.randint(3, 8), random.choice(palette))
```

---

## 📌 知识卡 4 · 用 `if` 让少数星星特别一点

真实的星空里，绝大多数是小点，只有几颗特别亮。用 `if` + 随机实现：

```python runnable 十分之一的概率画一颗大星
import random
import turtle

turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.penup()

for i in range(100):
    turtle.goto(random.randint(-250, 250), random.randint(-190, 190))

    if random.randint(1, 10) == 1:        # 10% 概率
        turtle.dot(random.randint(10, 16), "#FFE9A8")
    else:
        turtle.dot(random.randint(2, 5), "white")
```

`random.randint(1, 10) == 1` 就是「**十分之一的概率**」。
想要 20% 就写 `random.randint(1, 5) == 1`。这个技巧以后做游戏天天用。

---

## 📌 知识卡 5 · 画月亮：两个圆叠出来

```python runnable 弯月
import turtle

turtle.speed(0)
turtle.bgcolor("#0B0A1A")

# 先画一个满月
turtle.penup()
turtle.goto(150, 90)
turtle.pendown()
turtle.fillcolor("#FFE9A8")
turtle.pencolor("#FFE9A8")
turtle.begin_fill()
turtle.circle(45)
turtle.end_fill()

# 再用背景色画一个圆，叠上去咬掉一块
turtle.penup()
turtle.goto(170, 100)
turtle.pendown()
turtle.fillcolor("#0B0A1A")
turtle.pencolor("#0B0A1A")
turtle.begin_fill()
turtle.circle(45)
turtle.end_fill()
```

「**用背景色盖掉一部分**」是画图里非常常用的取巧办法 ✨

---

## 🛠 今天的任务 · 我的星空

画一片属于你的星空：

| 要求 | 说明 |
|---|---|
| 深色背景 | `bgcolor()` |
| 用 `for` 循环撒星星 | 至少 60 颗 |
| 位置随机 | `random.randint` 决定 x 和 y |
| 大小随机 | 星星不能一样大 |
| 至少三种颜色 | 随机挑或按概率分 |
| 用 `if` 做出「少数亮星」 | 用概率控制 |
| 画一个月亮 | 用 `circle` + 填充 |
| **`dot` 或 `circle` 调用不超过 6 次** | 靠循环生成，不许复制粘贴 |

> 🎨 这一关没有标准答案，好看就行 —— 画完存进作品陈列馆。
> 多跑几次，每次都不一样 ✨
