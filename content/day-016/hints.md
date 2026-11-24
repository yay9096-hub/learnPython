## 提示 1 · 先把「画一个正方形」写出来

内层循环就是 Day 15 的老套路：

```python
for j in range(4):
    turtle.forward(90)
    turtle.right(90)
```

先只写这一段，运行一次，确认能画出一个正方形，再往下做。

**每写一小块就跑一次** —— 这是 Day 7 说过的，画图的时候尤其管用。

## 提示 2 · 外面再套一层

把刚才那段整体**往右缩 4 格**，塞进外层循环里：

```python
for i in range(layers):

    for j in range(4):
        turtle.forward(90)
        turtle.right(90)

    turtle.right(360 / layers)
```

看清楚三层缩进：

- `for i` 顶格
- `for j` 缩进 4 格
- `turtle.forward` 缩进 8 格
- 最后那句 `turtle.right(360 / layers)` 缩进 **4 格** ——
  它属于外层，意思是「画完一整个正方形之后，转一点点」

## 提示 3 · 加上颜色

```python
colors = ["#8B5CF6", "#EC6FA9", "#F59E0B", "#34D399"]

for i in range(layers):
    turtle.pencolor(colors[i % 4])

    for j in range(4):
        turtle.forward(90)
        turtle.right(90)

    turtle.right(360 / layers)
```

`i % 4` 是 Day 3 学的取余：`i` 一直变大，但余数永远在 0~3 之间转圈，
正好轮流取到四个颜色。

📌 **画完之后一定要玩一玩**：把 `layers` 改成 6、20、36，
把内层的 4 改成 3 或 6，把 `forward` 的 90 改成 60 或 130。
每改一个数字都是一幅新图 ✨
