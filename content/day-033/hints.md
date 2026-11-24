## 提示 1 · zip + 嵌套解包

三个列表一起遍历，而且顺手把坐标拆开：

```python
for name, (x, y), size in zip(names, points, sizes):
    print(f"  {name} ({x}, {y}) 亮度 {size}")
```

看清楚循环变量：`name, (x, y), size` ——

- `zip` 每一圈给出三样：名字、坐标元组、亮度
- 中间那个用**括号**包起来，就会被再拆成 `x` 和 `y`

这叫**嵌套解包**，看着花哨，其实就是「一层层对应上」。

## 提示 2 · 算中心点

```python
sum_x = 0
sum_y = 0
for x, y in points:
    sum_x += x
    sum_y += y

center_x = round(sum_x / len(points), 1)
center_y = round(sum_y / len(points), 1)
```

`for x, y in points:` 也是解包 —— 每个 point 是 `(x, y)`，直接拆成两个变量。

找最亮的星（顺便把坐标也记下来，画标注时要用）：

```python
best_name = ""
best_size = 0
best_point = (0, 0)

for name, point, size in zip(names, points, sizes):
    if size > best_size:
        best_size = size
        best_name = name
        best_point = point
```

⚠️ 这里 `point` **没有**用括号拆开 —— 因为要把整个元组存起来。

## 提示 3 · 画星星和连线

```python
turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.pensize(2)
turtle.pencolor("#5A5480")
turtle.penup()

first = True
for name, (x, y), size in zip(names, points, sizes):
    turtle.goto(x, y)
    if first:
        turtle.pendown()      # 到了第一个点才落笔
        first = False
    turtle.dot(size * 2, "#FFE9A8")
```

那个 `first` 变量的作用：**第一次移动不画线**（不然会从画布中心拖一条线过来），
到位之后再落笔，后面的移动就会连成折线。

标注最亮的星：

```python
bx, by = best_point           # 解包出坐标
turtle.penup()
turtle.goto(bx + 12, by + 8)  # 稍微错开一点，别压在星星上
turtle.pendown()
turtle.pencolor("#EC6FA9")
turtle.write(best_name, font=("", 16, "bold"))
```
