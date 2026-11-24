## 提示 1 · 嵌套循环的固定骨架

所有二维图案都是这个形状：

```python
for row in range(行数):
    for col in range(列数):
        print("要画的东西", end="")     # ← 内层：横着排
    print()                             # ← 外层：一行画完，换行
```

三个位置要看清楚缩进：

- `for col` 缩进 4 格
- `print(..., end="")` 缩进 8 格
- 空的 `print()` 缩进 **4 格** —— 它属于外层！

⚠️ 那个空 `print()` 放错层是最常见的错误。放进内层就每个字符都换行了。

## 提示 2 · 棋盘和方框：内层用 if 决定画什么

棋盘：

```python
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            print("⬛", end="")
        else:
            print("⬜", end="")
    print()
```

空心方框（只画边）：

```python
size = 5
for row in range(size):
    for col in range(size):
        if row == 0 or row == size - 1 or col == 0 or col == size - 1:
            print("★", end="")
        else:
            print(" ", end="")
    print()
```

念一遍那个条件：「第一行 **或** 最后一行 **或** 第一列 **或** 最后一列」——
这就是「边框」的数学定义。

## 提示 3 · 乘法表和菱形

乘法表的关键是**内层范围用到外层变量**：

```python
for i in range(1, 10):
    for j in range(1, i + 1):        # ← 注意这里的 i
        print(f"{j}×{i}={i * j}", end="\t")
    print()
```

菱形 = Day 15 的金字塔 + 一个倒着的：

```python
n = 5
for i in range(1, n + 1):            # 上半：1 2 3 4 5
    print(" " * (n - i) + "★" * (2 * i - 1))
for i in range(n - 1, 0, -1):        # 下半：4 3 2 1
    print(" " * (n - i) + "★" * (2 * i - 1))
```

⚠️ 下半从 `n - 1`（也就是 4）开始，不是从 5 ——
不然中间最宽那行会打印两遍。
