## 提示 1 · 一颗星星只要三行

先把「画一颗随机星星」写出来，跑一次看看：

```python
turtle.goto(random.randint(-250, 250), random.randint(-190, 190))
turtle.dot(5, "white")
```

能出来一颗，就把它缩进到循环里 —— 一百颗就出来了：

```python
for i in range(120):
    turtle.goto(random.randint(-250, 250), random.randint(-190, 190))
    turtle.dot(5, "white")
```

⚠️ `turtle.penup()` 写在循环**外面**就行，抬一次就一直抬着。
忘了写的话，星星之间会拖出一堆线。

## 提示 2 · 加上随机大小和颜色

```python
palette = ["#FFFFFF", "#FFE9A8", "#A8D8FF", "#FFC8E4"]

for i in range(120):
    turtle.goto(random.randint(-250, 250), random.randint(-190, 190))
    turtle.dot(random.randint(2, 6), random.choice(palette))
```

`random.choice(palette)` 是 Day 10 学的 —— 从一串里随便挑一个。

再用 `if` 让少数星星特别亮：

```python
    if random.randint(1, 12) == 1:            # 大约 8% 的概率
        turtle.dot(random.randint(9, 15), "#FFE9A8")
    else:
        turtle.dot(random.randint(2, 6), random.choice(palette))
```

## 提示 3 · 月亮：两个圆叠出来

```python
# ① 先画一个满月
turtle.goto(150, 80)
turtle.pendown()
turtle.pencolor("#FFE9A8")
turtle.fillcolor("#FFE9A8")
turtle.begin_fill()
turtle.circle(45)
turtle.end_fill()

# ② 再用背景色画一个圆，稍微偏一点，咬掉一块
turtle.penup()
turtle.goto(172, 92)
turtle.pendown()
turtle.pencolor("#0B0A1A")
turtle.fillcolor("#0B0A1A")
turtle.begin_fill()
turtle.circle(45)
turtle.end_fill()
```

第二个圆的位置错开多少，决定了月牙有多细 —— 自己调着玩 ✨
（记得月亮要画在星星**之后**，不然会被星星盖住。）
