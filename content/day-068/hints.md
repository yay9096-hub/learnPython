## 提示 1 · 造棋盘的唯一正确写法

```python
def make_board(size):
    """造一个 size x size 的空棋盘。"""
    return [[EMPTY] * size for _ in range(size)]
```

⚠️ **千万别写 `[[EMPTY] * size] * size`**。

外层的 `* size` 复制的是**同一个列表的引用** —— 七行其实是同一行，
下一个子会整列一起变。判题专门有一条在验这个。

打印时带上坐标：

```python
def show_board(board):
    """打印棋盘，带行号和列号。"""
    print("    " + " ".join(str(c) for c in range(len(board))))
    for r in range(len(board)):
        print(f" {r}  " + " ".join(board[r]))
```

第一行是列号，每行开头是行号。**没坐标玩家根本不知道该输什么数字。**

## 提示 2 · 检查在前，落子在后

```python
def can_place(board, row, col):
    """这个位置能不能下。返回 (能不能, 说明)。"""
    size = len(board)
    if row < 0 or row >= size or col < 0 or col >= size:
        return False, "超出棋盘了"          # ← 越界检查必须最先
    if board[row][col] != EMPTY:
        return False, "这里已经有子了"
    return True, "可以下"


def place(board, row, col, piece):
    """落子。不合法就不下，返回是否成功。"""
    ok, why = can_place(board, row, col)
    if not ok:
        print(f"     ⚠️ {why}")
        return False
    board[row][col] = piece
    return True
```

⚠️ **越界判断一定要在 `board[row][col]` 之前** ——
顺序反了会直接 IndexError，`can_place` 自己就崩了。

## 提示 3 · 判赢：一个方向和它的反方向

先写一个「沿着某方向数」的小工具：

```python
def count_line(board, row, col, dr, dc, piece):
    """从 (row,col) 出发沿 (dr,dc) 数有几个连着的 piece，不含自己。"""
    size = len(board)
    n = 0
    r = row + dr          # ← 从下一格开始，所以不含自己
    c = col + dc
    while 0 <= r < size and 0 <= c < size and board[r][c] == piece:
        n += 1
        r += dr
        c += dc
    return n
```

`while` 的三个条件缺一不可：行不越界、列不越界、棋子是自己的。

然后四个方向各查一遍：

```python
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]


def check_win(board, row, col, piece):
    """刚在 (row,col) 落了一个 piece，看看有没有连成 WIN 个。"""
    for dr, dc in DIRECTIONS:
        total = 1                                              # 自己算一个
        total += count_line(board, row, col, dr, dc, piece)     # 一边
        total += count_line(board, row, col, -dr, -dc, piece)   # 另一边
        if total >= WIN:
            return True
    return False
```

**关键是 `-dr, -dc` 那一行** —— 只数一边的话，
落在四连正中间时会漏判（判题专门试了这种情况）。

主流程问玩家坐标记得转数字并兜底：

```python
try:
    row = int(row_text)
    col = int(col_text)
except ValueError:
    row = -1
    col = -1
    print("  ⚠️ 要输入数字哦")
```

`-1` 会被 `can_place` 挡下来，正好。
