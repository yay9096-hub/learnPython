## 提示 1 · 先写出口，再写递归

递归函数的固定骨架 —— **出口永远写在第一句**：

```python
def countdown(n):
    """从 n 倒数到 1，数完喊发射。"""
    if n <= 0:            # ① 出口：满足就 return，不再调自己
        print("发射！🚀")
        return
    print(n)
    countdown(n - 1)      # ② 朝出口靠近：n 每次都变小
```

阶乘版有返回值：

```python
def factorial(n):
    """算 n 的阶乘。"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

⚠️ 出口写 `n <= 1` 而不是 `n == 1` —— 这样 `factorial(0)` 也能返回 1，
判题会拿 0 试。

## 提示 2 · 树的六个步骤

```python
def tree(length, depth):
    """画一根树枝，并在末端递归长出两根更小的。"""
    if depth == 0:                      # ① 出口
        return

    if depth <= 2:                      # ② 设颜色和粗细
        turtle.pencolor("#7BC96F")
    else:
        turtle.pencolor("#5B3A2E")
    turtle.pensize(depth)

    turtle.forward(length)              # ③ 画这一根

    turtle.left(28)                     # ④ 左偏，长左边的小树
    tree(length * 0.72, depth - 1)

    turtle.right(56)                    # ⑤ 转到右边，长右边的小树
    tree(length * 0.72, depth - 1)

    turtle.left(28)                     # ⑥ 角度转回来
    turtle.backward(length)             #    位置退回去
```

**第 ⑥ 步是最容易漏的**。角度 `left(28)` → `right(56)` → `left(28)` 正好抵消，
`backward` 把海龟送回这根树枝的起点。

> 🧠 口诀：**来时什么样，走时还什么样。**
> 递归函数结束时必须把位置和角度还原，上一层才能继续正常工作。

## 提示 3 · 主流程要先摆好海龟

海龟默认在画布中央、头朝右。画树要它在**下方、头朝上**：

```python
turtle.speed(0)
turtle.bgcolor("#FDF9FF")
turtle.penup()
turtle.goto(0, -200)      # 挪到下方
turtle.left(90)           # 头转向正上方
turtle.pendown()

tree(100, 7)
turtle.hideturtle()
```

⚠️ `turtle.speed(0)` 很重要 —— 7 层树有一百多根树枝，
不用 0 会画得很慢。

### 树画歪了怎么办

| 症状 | 原因 |
|---|---|
| 树枝越长越乱、不成形 | 漏了 `turtle.backward(length)` |
| 树整体歪向一边 | 三次转角没有抵消（应该是 28 → 56 → 28） |
| 只有一根光杆 | `depth` 给太小，或者只递归调用了一次 |
| RecursionError | 忘了写出口 `if depth == 0: return` |
