# Day 8 · 画一颗魔法星星 🌟

> 「前七天全是文字，看腻了吧？
> 今天给你一支笔 —— 准确地说，是一只**会走路的小海龟**。
> 它走过的地方就会留下线条。」

今天的目标：一颗五角星 + 一圈光环 + 你的署名。
（右边切到「🐢 画布」标签页，就能看到你画的东西）

---

## 📌 知识卡 1 · `import` —— 借用别人的工具箱

Python 自带很多现成的工具箱，用之前要先「搬进来」：

```python runnable 搬工具箱
import turtle

turtle.forward(100)
```

点 ▶ 之后**看右边的画布**，小海龟往前走了 100 步，留下一条线。

`import turtle` 之后，所有海龟的功能都要写成 `turtle.功能名()`，
中间那个点的意思是「turtle 工具箱里的」。

---

## 📌 知识卡 2 · 前进和转弯

小海龟只认三件事：**往前走**、**左转**、**右转**。

```python runnable 走一个直角
import turtle

turtle.forward(120)
turtle.right(90)
turtle.forward(120)
```

| 命令 | 意思 |
|---|---|
| `turtle.forward(100)` | 朝**当前朝向**前进 100 |
| `turtle.backward(100)` | 后退 |
| `turtle.right(90)` | 原地**右转** 90 度 |
| `turtle.left(90)` | 原地**左转** 90 度 |

⚠️ 关键：**转弯是相对的**。它转的是「相对现在的朝向」，不是绝对方向。
小海龟一开始头朝右边。

```python runnable 画一个正方形（很啰嗦对吧？）
import turtle

turtle.forward(100)
turtle.right(90)
turtle.forward(100)
turtle.right(90)
turtle.forward(100)
turtle.right(90)
turtle.forward(100)
```

> 😩 是不是觉得「这也太重复了」？
> **对！这就是循环存在的意义。** 第 11 天你会学到怎么把这 7 行压成 2 行。
> 今天先忍一忍 —— 感受过手工的痛苦，才知道循环有多香 (๑•̀ㅂ•́)و

---

## 📌 知识卡 3 · 换颜色、换粗细、换速度

```python runnable 让线条好看一点
import turtle

turtle.pensize(6)
turtle.pencolor("#8B5CF6")
turtle.forward(150)

turtle.pencolor("#EC6FA9")
turtle.right(120)
turtle.forward(150)
```

| 命令 | 作用 |
|---|---|
| `turtle.pencolor("red")` | 换笔的颜色，也可以用 `"#EC6FA9"` 这种色号 |
| `turtle.pensize(6)` | 换笔的粗细 |
| `turtle.speed(0)` | 速度。1 最慢，10 很快，**0 是瞬间画完** |
| `turtle.bgcolor("#FDF9FF")` | 换背景色 |

颜色可以写英文名（red、blue、pink、purple、gold），
也可以写十六进制色号（`#8B5CF6`）—— 后者能调出更好看的颜色。

---

## 📌 知识卡 4 · 抬笔 —— 移动但不画线

想换个地方再画？用 `penup()` 把笔抬起来。

```python runnable 抬笔挪窝
import turtle

turtle.forward(80)

turtle.penup()          # 抬笔
turtle.right(90)
turtle.forward(100)     # 这一段不会留下线
turtle.pendown()        # 落笔

turtle.left(90)
turtle.forward(80)
```

还有一个更直接的：`goto(x, y)` 直接跳到指定坐标。
画布正中间是 `(0, 0)`，**向右 x 变大，向上 y 变大**。

```python runnable 直接传送
import turtle

turtle.penup()
turtle.goto(-100, 80)
turtle.pendown()
turtle.forward(200)
```

---

## 📌 知识卡 5 · 画圆和写字

```python runnable 圆环和署名
import turtle

turtle.pencolor("#F59E0B")
turtle.pensize(3)
turtle.circle(80)

turtle.penup()
turtle.goto(-40, -120)
turtle.pendown()
turtle.pencolor("#8B5CF6")
turtle.write("星野樱", font=("", 20, "normal"))
```

- `turtle.circle(半径)` —— 从当前位置画一个圆
- `turtle.write("文字")` —— 在当前位置写字

---

## 🔺 五角星的秘密

画五角星只要重复 5 次：**前进 → 右转 144 度**。

为什么是 144？因为笔迹绕中心要转**两圈**才回到起点：`360 × 2 ÷ 5 = 144`。

```python runnable 半颗星（剩下的你来补）
import turtle

turtle.pensize(5)
turtle.pencolor("#F59E0B")

turtle.forward(200)
turtle.right(144)
turtle.forward(200)
turtle.right(144)
```

---

## 🛠 今天的任务

画一张**魔法星星海报**：

| 要求 | 说明 |
|---|---|
| `import turtle` | 先把工具箱搬进来 |
| 画一颗完整的五角星 | 5 条边，每次 `right(144)` |
| 至少用两种颜色 | 星星一种，其它一种 |
| 设置了笔的粗细 | `pensize()` |
| 画一个圆当光环 | `circle()` |
| 用 `penup()` 挪过位置 | 换地方画的时候别拖出线来 |
| 用 `write()` 署名 | 写上你的名字 |

> 🎨 画完切到右边的「🐢 画布」标签看效果。
> 觉得不好看？改改颜色和数字，再跑一次 —— 这就是写代码最爽的部分。
