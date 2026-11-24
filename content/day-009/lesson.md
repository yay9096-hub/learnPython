# Day 9 · 专属魔法阵 🔮

> 「昨天你画了线。今天我们上色 —— 让画面真正变得好看起来。」

---

## 📌 知识卡 1 · 坐标系：画布上的地址

画布正中间是 `(0, 0)`。

```
              y 变大 ↑
                    |
                    |
   ←  x 变小 -------+------- x 变大  →
                    |
                    |
              y 变小 ↓
```

`goto(x, y)` 就是「直接传送到这个地址」。

```python runnable 四个角落各点一下
import turtle

turtle.speed(0)
turtle.penup()

turtle.goto(-150, 100)
turtle.dot(20, "#EC6FA9")

turtle.goto(150, 100)
turtle.dot(20, "#8B5CF6")

turtle.goto(0, -100)
turtle.dot(30, "#F59E0B")
```

`turtle.dot(大小, 颜色)` 会在当前位置点一个圆点，做装饰特别方便。

---

## 📌 知识卡 2 · `setheading` —— 直接指定朝向

昨天的 `right()` / `left()` 是**相对转向**，容易转晕。
`setheading()` 是**绝对朝向**，直接告诉它「朝这个方向」：

```python runnable 绝对朝向
import turtle

turtle.setheading(90)     # 朝上
turtle.forward(100)

turtle.setheading(180)    # 朝左
turtle.forward(100)
```

| 角度 | 方向 |
|---|---|
| `0` | 右 → |
| `90` | 上 ↑ |
| `180` | 左 ← |
| `270` | 下 ↓ |

---

## 📌 知识卡 3 · 填充 ⭐

这是今天最好玩的一招。用 `begin_fill()` 和 `end_fill()` **夹住**你画的形状：

```python runnable 一个填了色的三角形
import turtle

turtle.speed(0)
turtle.pencolor("#7C3AED")
turtle.fillcolor("#DDCEFF")
turtle.pensize(4)

turtle.begin_fill()
turtle.forward(150)
turtle.right(120)
turtle.forward(150)
turtle.right(120)
turtle.forward(150)
turtle.end_fill()
```

规则很简单：

1. `fillcolor("颜色")` 先说好要填什么色
2. `begin_fill()` 开始记录
3. 中间画你的形状
4. `end_fill()` 收工，Python 自动把围起来的区域涂满

⚠️ 形状要**闭合**（画回起点附近），否则填色会很奇怪。

圆也能填：

```python runnable 填色的圆
import turtle

turtle.fillcolor("#F59E0B")
turtle.pencolor("#7C3AED")
turtle.pensize(3)

turtle.begin_fill()
turtle.circle(80)
turtle.end_fill()
```

---

## 📌 知识卡 4 · 背景色 —— 一秒变高级

```python runnable 深色背景 + 亮色线条
import turtle

turtle.bgcolor("#1A1625")
turtle.pensize(4)
turtle.pencolor("#F59E0B")

turtle.circle(90)

turtle.penup()
turtle.goto(-30, -20)
turtle.pendown()
turtle.pencolor("#EC6FA9")
turtle.write("MAGIC", font=("", 22, "bold"))
```

> 🎨 配色小抄（拿去直接用）：
> 紫 `#8B5CF6` · 粉 `#EC6FA9` · 金 `#F59E0B` · 青 `#34D399` ·
> 浅紫 `#DDCEFF` · 深底 `#1A1625`

---

## 📌 知识卡 5 · 同心圆的做法

魔法阵最经典的元素就是好几层圆环。
诀窍是：**每画一个圆之前，把海龟往下挪一点**，圆心才会重合。

```python runnable 三层圆环
import turtle

turtle.speed(0)
turtle.pensize(3)

turtle.penup()
turtle.goto(0, -60)
turtle.pendown()
turtle.pencolor("#8B5CF6")
turtle.circle(60)

turtle.penup()
turtle.goto(0, -100)
turtle.pendown()
turtle.pencolor("#EC6FA9")
turtle.circle(100)

turtle.penup()
turtle.goto(0, -140)
turtle.pendown()
turtle.pencolor("#F59E0B")
turtle.circle(140)
```

看出规律了吗？半径是 60 / 100 / 140，起点的 y 就是 `-60` / `-100` / `-140`。

---

## 🛠 今天的任务

画一个**属于你的魔法阵**：

| 要求 | 说明 |
|---|---|
| 设置了背景色 | `bgcolor()` |
| 至少两层同心圆环 | 用 `circle()` + `goto()` |
| 至少一个填充图形 | `begin_fill()` … `end_fill()` |
| 用了 `setheading()` | 至少一次绝对朝向 |
| 至少三种颜色 | 让它花一点 |
| 用 `dot()` 加装饰点 | 至少两个 |
| 中间写上你的名字或咒语 | `write()` |

> ✨ 这一关**没有标准答案**，好看就行。
> 画完之后它会被存进作品陈列馆，随时可以拿给爸爸看。
