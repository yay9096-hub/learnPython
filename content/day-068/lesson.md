# Day 68 · 文字版五子棋 ⚫️⚪️

> 「棋盘是个方阵 —— 有行有列。
> 一维列表装不下它，得用**列表里装列表**。
>
> 今天学会二维列表，然后做一个真能下的五子棋。」

---

## 📌 知识卡 1 · 二维列表长什么样

```python runnable 三行三列
board = [
    [".", ".", "."],
    [".", "X", "."],
    [".", ".", "."],
]

print(board)
print(board[1])
print(board[1][1])
```

**外层列表的每一项，是一整行**。

取值写 `board[行][列]` —— **先行后列**，跟数学里的矩阵一样。

```python runnable 坐标怎么对应
board = [
    ["a", "b", "c"],
    ["d", "e", "f"],
]

print(board[0][0])
print(board[0][2])
print(board[1][0])
```

⚠️ **行列都从 0 开始数**（Day 23 的老规矩）。

---

## 📌 知识卡 2 · ⚠️ 造棋盘的经典陷阱

```python runnable 这样造是坏的（跑一下看）
board = [["."] * 3] * 3
print(board)

board[0][0] = "X"
print(board)
```

**下了一个子，三行全变了！**

原因跟 Day 40 一样：`* 3` 复制的是**同一个列表的引用** ——
三行其实是同一行。

```python runnable 正确的造法
board = [["."] * 3 for _ in range(3)]
print(board)

board[0][0] = "X"
print(board)
```

`[... for _ in range(3)]` 每转一圈**造一个新列表**，三行互不相干。

> 🧠 记住这个写法：**`[["."] * 列数 for _ in range(行数)]`**
> 这是造二维列表的标准姿势。
>
> `_` 是个约定俗成的变量名，意思是「这个值我不用」。

---

## 📌 知识卡 3 · 打印棋盘

```python runnable 带坐标的棋盘
SIZE = 5

board = [["."] * SIZE for _ in range(SIZE)]
board[2][2] = "X"
board[1][3] = "O"

print("   " + " ".join(str(c) for c in range(SIZE)))
for r in range(SIZE):
    print(f"{r}  " + " ".join(board[r]))
```

两个要点：

- **表头**：把列号打印在最上面一行
- **每行**：行号 + `" ".join(board[r])`（Day 28 的 join）

没有坐标的话，玩家根本不知道该输入什么数字。

---

## 📌 知识卡 4 · 两层循环遍历

```python runnable 数一数有几个空位
SIZE = 4
board = [["."] * SIZE for _ in range(SIZE)]
board[0][0] = "X"
board[1][1] = "O"

empty = 0
for r in range(SIZE):
    for c in range(SIZE):
        if board[r][c] == ".":
            empty += 1

print(f"还有 {empty} 个空位")
```

**外层管行、内层管列** —— Day 18 的嵌套循环，换个场景又用上了。

---

## 📌 知识卡 5 · 落子和合法性检查

```python runnable 落子前要检查三件事
SIZE = 5
board = [["."] * SIZE for _ in range(SIZE)]


def can_place(board, row, col):
    """这个位置能不能下。"""
    if row < 0 or row >= SIZE or col < 0 or col >= SIZE:
        return False, "超出棋盘了"
    if board[row][col] != ".":
        return False, "这里已经有子了"
    return True, "可以下"


print(can_place(board, 2, 2))
board[2][2] = "X"
print(can_place(board, 2, 2))
print(can_place(board, 9, 9))
```

⚠️ **越界检查一定要在取值之前** —— 先 `if row >= SIZE` 挡住，
再去访问 `board[row][col]`，否则直接 IndexError。

---

## 📌 知识卡 6 · 胜负判定：四个方向 ⭐

五子连珠有四个方向：**横、竖、斜、反斜**。

```
横 →      (0, 1)
竖 ↓      (1, 0)
斜 ↘      (1, 1)
反斜 ↙    (1, -1)
```

从落子点出发，**往两边各数一遍**：

```python runnable 判断有没有连成 N 个
SIZE = 7
WIN = 4

board = [["."] * SIZE for _ in range(SIZE)]
for c in range(4):
    board[3][c + 1] = "X"


def count_line(board, row, col, dr, dc, piece):
    """从 (row,col) 出发，沿 (dr,dc) 方向数有几个连着的 piece。"""
    n = 0
    r, c = row + dr, col + dc
    while 0 <= r < SIZE and 0 <= c < SIZE and board[r][c] == piece:
        n += 1
        r += dr
        c += dc
    return n


def check_win(board, row, col, piece):
    """刚在 (row,col) 下了一个 piece，判断是不是赢了。"""
    for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
        total = 1
        total += count_line(board, row, col, dr, dc, piece)
        total += count_line(board, row, col, -dr, -dc, piece)
        if total >= WIN:
            return True
    return False


print(check_win(board, 3, 2, "X"))
print(check_win(board, 3, 2, "O"))
```

看 `check_win` 的三行核心：

```
total = 1                                   ← 自己算一个
total += 往这个方向数                          ← 比如往右
total += 往相反方向数                          ← 那就是往左
```

**一个方向和它的反方向合起来，才是完整的一条线。**

`while 0 <= r < SIZE and ...` 这一句同时做了三件事：
不越界、不越界、而且棋子是自己的。

---

## 📌 知识卡 7 · 平局

```python runnable 棋盘满了就是平局
def is_full(board):
    """棋盘满了吗。"""
    for row in board:
        if "." in row:
            return False
    return True


board = [["X", "O"], ["O", "X"]]
print(is_full(board))

board2 = [["X", "."], ["O", "X"]]
print(is_full(board2))
```

`if "." in row` —— 每一行本身就是个列表，直接用 `in` 查（Day 24）。

---

## 🛠 今天的任务 · 五子棋（4 连即胜）

用 **7×7 棋盘、连成 4 个就赢**（比标准五子棋快，好演示）。

| 函数 | 说明 |
|---|---|
| `make_board(size)` | 造一个 size×size 的棋盘，**用正确的造法** |
| `show_board(board)` | 打印棋盘，**带行号和列号** |
| `can_place(board, row, col)` | 返回 `(能不能下, 说明)`。要检查越界和占位 |
| `place(board, row, col, piece)` | 落子，返回是否成功 |
| `count_line(board, row, col, dr, dc, piece)` | 沿一个方向数连子数（不含自己） |
| `check_win(board, row, col, piece)` | 判断刚落的这子有没有连成 4 |
| `is_full(board)` | 棋盘满了吗 |

主流程要求：

- 造棋盘，显示初始状态
- **预先摆几步棋**（写死的坐标），每步都显示棋盘
- 演示 `can_place` 的三种情况：能下、已有子、超出棋盘
- 演示 `check_win` 判出**胜利**（摆出一个 4 连）
- 问玩家输入一步棋（**行 和 列 分两次问**），检查合法性后落子
- 打印最终棋盘和结果

> 💡 判题会喂固定坐标，所以摆棋的顺序要照着任务写。
> ⚠️ 造棋盘**千万别用 `[["."] * n] * n`** —— 那样一下子全盘都变。
