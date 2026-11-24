## 提示 1 · 同心圆的那个小技巧

`circle(r)` 是**从当前位置开始**往上画一个圆，
所以想让几个圆的圆心重合，起点的 y 要等于「负的半径」：

```python
turtle.penup()
turtle.goto(0, -150)    # ← 半径 150，就 goto 到 -150
turtle.pendown()
turtle.circle(150)
```

第二层换个半径，重复一遍就行。

## 提示 2 · 填充的固定套路

```python
turtle.fillcolor("#3B2A5C")   # 1. 说好填什么色
turtle.begin_fill()           # 2. 开始记录
turtle.forward(160)           # 3. 画一个闭合图形
turtle.left(120)
turtle.forward(160)
turtle.left(120)
turtle.forward(160)
turtle.end_fill()             # 4. 收工，自动涂满
```

⚠️ 图形一定要**画回起点附近**，不然填出来会很鬼畜（可以故意试一次，挺好玩的）。

## 提示 3 · 放射线的写法

每画一条放射线，都先回到中心、再指定朝向：

```python
turtle.penup()
turtle.goto(0, 0)
turtle.setheading(90)     # 朝上
turtle.pendown()
turtle.forward(150)
```

改 `setheading()` 里的角度（比如 210、330），就能画出不同方向的线。
三条线用 90 / 210 / 330 会很对称 ✨

装饰点更简单，抬着笔直接点：

```python
turtle.penup()
turtle.goto(0, 150)
turtle.dot(18, "#F59E0B")
```
