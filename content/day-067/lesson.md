# Day 67 · 科赫雪花 ❄️

> 「Day 43 你用递归画了一棵树。今天画一个更神奇的东西 ——
>
> 取一条直线，把它中间凸出一个尖；
> 对新产生的每一段再做同样的事；
> 重复四次 —— **它就变成了一片雪花。**
>
> 这是数学里最有名的图形之一，叫**科赫雪花**。」

---

## 📌 知识卡 1 · 一条线怎么变成四段

科赫曲线的规则只有一句话：

> **把一条线分成三等份，中间那份换成一个向外凸的尖角。**

```
原来：  ────────────

变成：  ──  /\  ──
           /  \
```

用海龟的语言说，就是这四步：

```python runnable 一层的科赫曲线
import turtle

turtle.speed(0)
turtle.pensize(2)

length = 240

turtle.penup()
turtle.goto(-120, 0)
turtle.pendown()

turtle.forward(length / 3)
turtle.left(60)
turtle.forward(length / 3)
turtle.right(120)
turtle.forward(length / 3)
turtle.left(60)
turtle.forward(length / 3)

turtle.hideturtle()
```

**前进、左转 60、前进、右转 120、前进、左转 60、前进** ——
记住这个节奏，今天全靠它。

⚠️ 注意三个角度加起来正好抵消：`+60 - 120 + 60 = 0`，
所以画完之后海龟的朝向跟出发时一样（Day 43 的老规矩）。

---

## 📌 知识卡 2 · 递归：每一段再来一遍 ⭐

```python runnable 真正的科赫曲线
import turtle

def koch(length, depth):
    """画一条科赫曲线。depth 是细分层数。"""
    if depth == 0:
        turtle.forward(length)
        return

    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)
    turtle.right(120)
    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)

turtle.speed(0)
turtle.pensize(2)
turtle.pencolor("#8B5CF6")
turtle.penup()
turtle.goto(-150, 0)
turtle.pendown()

koch(300, 3)
turtle.hideturtle()
```

对比一下上一段：**把四个 `forward` 换成了四个 `koch(...)`**。

- `depth == 0` 时，`koch` 就是简单的「画一条直线」—— 这是出口
- 否则，它把自己拆成**四段更短的科赫曲线**

把 `depth` 从 0 改到 4，一个一个跑，看着它长出细节：

```python runnable 试试 depth = 0 / 1 / 2 / 4
import turtle

def koch(length, depth):
    if depth == 0:
        turtle.forward(length)
        return
    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)
    turtle.right(120)
    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)

turtle.speed(0)
turtle.penup()
turtle.goto(-150, 0)
turtle.pendown()

koch(300, 4)
turtle.hideturtle()
```

> 🧠 **一个 9 行的函数，画出了几百条线段。**
> 递归的威力就在这里：**规则很简单，结果很复杂。**

---

## 📌 知识卡 3 · 三条曲线拼成雪花 ⭐

雪花 = **三条科赫曲线围成一个三角形**。

```python runnable 科赫雪花
import turtle

def koch(length, depth):
    """一条科赫曲线。"""
    if depth == 0:
        turtle.forward(length)
        return
    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)
    turtle.right(120)
    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)


def snowflake(length, depth):
    """三条科赫曲线围成一片雪花。"""
    for i in range(3):
        koch(length, depth)
        turtle.right(120)


turtle.speed(0)
turtle.bgcolor("#0B1020")
turtle.pensize(2)
turtle.pencolor("#A8D8FF")
turtle.penup()
turtle.goto(-140, 80)
turtle.pendown()

snowflake(280, 3)
turtle.hideturtle()
```

`for i in range(3): koch(...); turtle.right(120)` ——
画一条边、右转 120 度，重复三次就闭合了（Day 16 学的正多边形套路）。

⚠️ 起点要往**左上**放一点，不然雪花会跑出画布。

---

## 📌 知识卡 4 · 深度的代价

```python runnable 数一数画了多少段
def count_segments(depth):
    """算一算 depth 层的科赫曲线有多少段直线。"""
    return 4 ** depth

for d in range(7):
    print(f"  depth={d}：一条边 {count_segments(d)} 段，整片雪花 {3 * count_segments(d)} 段")
```

每加一层，线段数**乘以 4**。

- `depth=3` → 一片雪花 192 段，很快
- `depth=5` → 3072 段，开始慢了
- `depth=7` → 49152 段，浏览器会卡住

> ⚠️ **递归的深度要克制。** 今天用 3 或 4 就很漂亮了。
> 想画更深，记得先 `turtle.speed(0)`。

---

## 📌 知识卡 5 · 让雪花好看

```python runnable 三层不同颜色和大小
import turtle

def koch(length, depth):
    if depth == 0:
        turtle.forward(length)
        return
    for angle in [60, -120, 60, 0]:
        koch(length / 3, depth - 1)
        if angle:
            turtle.left(angle)


def snowflake(length, depth):
    for i in range(3):
        koch(length, depth)
        turtle.right(120)


def draw_at(x, y, length, depth, color, width):
    """在指定位置画一片雪花。"""
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.pencolor(color)
    turtle.pensize(width)
    snowflake(length, depth)


turtle.speed(0)
turtle.bgcolor("#0B1020")

draw_at(-170, 60, 190, 3, "#A8D8FF", 2)
draw_at(40, 100, 120, 3, "#E8B4FF", 2)
draw_at(60, -60, 90, 2, "#FFE9A8", 1)

turtle.hideturtle()
```

上面的 `koch` 用循环写了同一件事 —— **四段 + 三次转角**，
`angle` 为 0 时不转（最后一段后面不需要转）。

两种写法都对，展开写更好读，循环写更短。

---

## 🛠 今天的任务 · 我的雪花夜空

| 函数 | 说明 |
|---|---|
| `koch(length, depth)` | 一条科赫曲线。**必须递归、必须有出口** |
| `snowflake(length, depth)` | 三条曲线围成雪花（循环 3 次，每次右转 120） |
| `draw_at(x, y, length, depth, color, width)` | 在指定位置画一片（抬笔 → 移动 → 落笔 → 设样式 → 画） |
| `count_segments(depth)` | 返回一条曲线的线段数（`4 ** depth`） |

主流程要求：

- 深色背景（星空感）
- 用 `draw_at` 画**至少 3 片**雪花，**大小、颜色、深度各不相同**
- 至少有一片 `depth >= 3`
- 用 `turtle.speed(0)`（不然要画很久）
- 最后 `hideturtle()`
- 在**终端**打印一张表：depth 0~5 各自的线段数，以及你这次一共画了多少段

> ⚠️ `koch` 里的三个转角必须是 **左60 / 右120 / 左60** —— 加起来抵消，
> 不然雪花会歪掉或者画不闭合。
>
> ❄️ 画好之后切到「🐢 画布」标签看 —— 这大概是整个课程里最好看的一张图。
