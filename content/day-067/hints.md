## 提示 1 · koch 的骨架

```python
def koch(length, depth):
    """画一条科赫曲线。depth 是细分层数。"""
    if depth == 0:                        # ① 出口：直接画一条直线
        turtle.forward(length)
        return

    koch(length / 3, depth - 1)           # ② 四段，中间三个转角
    turtle.left(60)
    koch(length / 3, depth - 1)
    turtle.right(120)
    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)
```

跟 Day 43 的树是同一个套路，只是拆法不同：

- **出口**：`depth == 0` 就老老实实画直线
- **递归**：四次调用自己，长度都除以 3、深度都减 1
- **转角**：`+60 → -120 → +60`，加起来是 0，所以画完朝向不变

⚠️ 最后一段后面**不用再转** —— 三个转角只夹在四段中间。

## 提示 2 · 雪花就是三条边

```python
def snowflake(length, depth):
    """三条科赫曲线围成一片雪花。"""
    for i in range(3):
        koch(length, depth)
        turtle.right(120)
```

跟 Day 16 画正三角形一模一样，只是把 `forward` 换成了 `koch`。

摆位置的函数：

```python
def draw_at(x, y, length, depth, color, width):
    """在指定位置画一片雪花。"""
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.pencolor(color)
    turtle.pensize(width)
    snowflake(length, depth)
```

**抬笔 → 移动 → 落笔** 三步不能少，否则两片雪花之间会拖一条线。

## 提示 3 · 主流程

用一个列表存参数，循环画，比写三遍干净：

```python
turtle.speed(0)
turtle.bgcolor("#0B1020")

flakes = [
    (-170, 60, 190, 3, "#A8D8FF", 2),
    (40, 110, 120, 3, "#E8B4FF", 2),
    (70, -70, 90, 2, "#FFE9A8", 1),
]

total = 0
for x, y, length, depth, color, width in flakes:
    draw_at(x, y, length, depth, color, width)
    total += 3 * count_segments(depth)

turtle.hideturtle()
```

`for x, y, length, depth, color, width in flakes:` —— 六个变量一次解包（Day 33）。

线段数表：

```python
for d in range(6):
    print(f"  depth={d}：一条边 {count_segments(d)} 段，"
          f"整片雪花 {3 * count_segments(d)} 段")
```

### 画歪了怎么办

| 症状 | 原因 |
|---|---|
| 雪花不闭合、歪向一边 | 三个转角不是 60/120/60 |
| 只有一条直线 | 忘了写出口，或者 depth 传了 0 |
| RecursionError | 出口条件写错了（比如写成 `depth == 1` 但传了 0.5） |
| 画得特别慢 | 忘了 `turtle.speed(0)`，或者 depth 给太大 |
| 两片之间有连线 | `draw_at` 里漏了 `penup()` |

> ❄️ `depth=3` 就已经很漂亮了。想试 5 也行，但会明显变慢 ——
> 每加一层线段数乘以 4。
