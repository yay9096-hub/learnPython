# Day 16 · 循环画图 · 万花筒 🌸

> 「还记得 Day 8 吗？画一颗五角星你敲了 9 行：
> forward、right、forward、right…… 当时我说了一句：
> **『第 11 天你会学到怎么把这 9 行压成 3 行』**。
>
> 今天到了。」

---

## 📌 知识卡 1 · 那 9 行，现在 3 行

先看 Day 8 你写过的东西：

```python runnable Day 8 的写法（9 行）
import turtle
turtle.speed(0)
turtle.pensize(4)

turtle.forward(150)
turtle.right(144)
turtle.forward(150)
turtle.right(144)
turtle.forward(150)
turtle.right(144)
turtle.forward(150)
turtle.right(144)
turtle.forward(150)
```

现在：

```python runnable 今天的写法（3 行）
import turtle
turtle.speed(0)
turtle.pensize(4)

for i in range(5):
    turtle.forward(150)
    turtle.right(144)
```

**完全一样的图，代码少了三分之二。**

这就是循环的意义 —— 不是为了炫技，是为了**把重复的部分只写一遍**。

---

## 📌 知识卡 2 · 一个公式画出所有正多边形

Day 8 的练习题里你已经发现规律了：**转的角度 = 360 ÷ 边数**。

现在有了循环，一改数字就换个图形：

```python runnable 改 sides 试试 3、4、6、8、12
import turtle
turtle.speed(0)
turtle.pensize(3)

sides = 6

for i in range(sides):
    turtle.forward(100)
    turtle.right(360 / sides)
```

把 `sides` 改成 `36` 试试 —— 边数一多，看起来就是个圆了 ✨

> 🧠 这就是「参数化」：**把会变的东西抽出来变成一个变量**。
> 想换图形只要改一个数字，不用重写代码。

---

## 📌 知识卡 3 · 循环变量能控制大小和颜色

`i` 每圈都在变，把它用进 `forward` 里就出效果了：

```python runnable 螺旋
import turtle
turtle.speed(0)
turtle.pensize(2)

for i in range(60):
    turtle.forward(i * 3)
    turtle.right(91)
```

第 1 圈走 3 步，第 2 圈走 6 步……越走越远，就螺旋出去了。

把 `91` 改成 `90` 试试，会得到完全不同的图形（正方形螺旋）。
**差一度，图形天差地别** —— 这就是画图最好玩的地方，随便改随便试。

---

## 📌 知识卡 4 · 万花筒 = 画一个，转一点，再画一个

这是今天的重头戏。套路只有三步：

1. 画一个基本图形
2. 转一个小角度
3. 重复 N 次

```python runnable 圆形万花筒
import turtle
turtle.speed(0)
turtle.pensize(2)
turtle.pencolor("#8B5CF6")

for i in range(12):
    turtle.circle(80)
    turtle.right(30)
```

12 个圆，每个转 30 度（`360 ÷ 12 = 30`），转完正好一整圈。

> 🧠 万花筒公式：**转的角度 = 360 ÷ 重复次数**。
> 这样最后一笔正好回到起点，图案才对称。

---

## 📌 知识卡 5 · 循环套循环（预告）

万花筒里的「基本图形」本身也可以是个循环：

```python runnable 12 个正方形转一圈
import turtle
turtle.speed(0)
turtle.pensize(2)
turtle.pencolor("#EC6FA9")

for i in range(12):
    for j in range(4):
        turtle.forward(80)
        turtle.right(90)
    turtle.right(30)
```

看缩进：

- 外层 `for i` 管「转 12 次」
- 内层 `for j` 管「画一个正方形」，缩进 8 格
- `turtle.right(30)` 缩进 4 格，属于外层 —— **每画完一个正方形转一次**

这叫**嵌套循环**，第 18 天会专门讲。今天先感受一下威力。

---

## 📌 知识卡 6 · 换颜色

```python runnable 每层换个颜色
import turtle
turtle.speed(0)
turtle.pensize(3)

colors = ["#8B5CF6", "#EC6FA9", "#F59E0B", "#34D399"]

for i in range(16):
    turtle.pencolor(colors[i % 4])
    turtle.forward(100)
    turtle.right(360 / 16 * 3)
```

`colors[i % 4]` 里的 `%` 是 Day 3 学的**取余** ——
`i` 一直变大，但 `i % 4` 永远在 0、1、2、3 之间循环，正好轮流取四个颜色。

> 💡 这个「取余循环取值」的技巧非常常用，记住它。

---

## 🛠 今天的任务 · 我的万花筒

用循环画一幅**万花筒**，要求：

| 要求 | 说明 |
|---|---|
| 至少两个 `for` 循环 | 一个画基本图形，一个负责旋转重复 |
| 至少一个嵌套循环 | 循环里面套循环 |
| 旋转次数 >= 8 | 转的角度用 `360 / 次数` 算出来 |
| 至少三种颜色 | 用 `colors[i % n]` 轮流取 |
| 设置背景色 | 深色底最好看 |
| **`forward` 只能出现 1~2 次** | 全靠循环生成，不许复制粘贴 😉 |

> 🎨 没有标准答案，好看就行。画完存进作品陈列馆。
> 改改角度、边数、颜色，多跑几次 —— 这一关就是让你玩的。
