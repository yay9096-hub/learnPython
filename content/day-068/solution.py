# Day 68 · 文字版五子棋（7x7，连成 4 个就赢）
SIZE = 7
WIN = 4
EMPTY = "."
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]


def make_board(size):
    """造一个 size x size 的空棋盘。

    注意用推导式而不是 [[EMPTY] * size] * size ——
    后者三行是同一个列表，下一个子会全盘都变。
    """
    return [[EMPTY] * size for _ in range(size)]


def show_board(board):
    """打印棋盘，带行号和列号。"""
    print("    " + " ".join(str(c) for c in range(len(board))))
    for r in range(len(board)):
        print(f" {r}  " + " ".join(board[r]))


def can_place(board, row, col):
    """这个位置能不能下。返回 (能不能, 说明)。"""
    size = len(board)
    if row < 0 or row >= size or col < 0 or col >= size:
        return False, "超出棋盘了"
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


def count_line(board, row, col, dr, dc, piece):
    """从 (row,col) 出发沿 (dr,dc) 数有几个连着的 piece，不含自己。"""
    size = len(board)
    n = 0
    r = row + dr
    c = col + dc
    while 0 <= r < size and 0 <= c < size and board[r][c] == piece:
        n += 1
        r += dr
        c += dc
    return n


def check_win(board, row, col, piece):
    """刚在 (row,col) 落了一个 piece，看看有没有连成 WIN 个。"""
    for dr, dc in DIRECTIONS:
        total = 1
        total += count_line(board, row, col, dr, dc, piece)
        total += count_line(board, row, col, -dr, -dc, piece)
        if total >= WIN:
            return True
    return False


def is_full(board):
    """棋盘满了吗。"""
    for row in board:
        if EMPTY in row:
            return False
    return True


# ---------- 主流程 ----------
print("⚫️⚪️ === 文字版五子棋（4 连即胜）=== ⚫️⚪️")

board = make_board(SIZE)

print("\n--- 初始棋盘 ---")
show_board(board)

print("\n--- 开局几手 ---")
opening = [(3, 1, "X"), (0, 0, "O"), (3, 2, "X"), (0, 1, "O")]
for row, col, piece in opening:
    place(board, row, col, piece)
    print(f"  {piece} 落在 ({row}, {col})")
show_board(board)

print("\n--- 合法性检查 ---")
print(f"  空位 (5, 5)：{can_place(board, 5, 5)}")
print(f"  已有子 (3, 1)：{can_place(board, 3, 1)}")
print(f"  越界 (9, 9)：{can_place(board, 9, 9)}")

print("\n--- X 连成四个 ---")
place(board, 3, 3, "X")
print(f"  X 落在 (3, 3) → 赢了吗：{check_win(board, 3, 3, 'X')}")
place(board, 3, 4, "X")
print(f"  X 落在 (3, 4) → 赢了吗：{check_win(board, 3, 4, 'X')}")
show_board(board)

print(f"\n棋盘满了吗：{is_full(board)}")

print("\n--- 轮到你了 ---")
row_text = input("你想下第几行？（0-6）").strip()
col_text = input("第几列？（0-6）").strip()

try:
    row = int(row_text)
    col = int(col_text)
except ValueError:
    row = -1
    col = -1
    print("  ⚠️ 要输入数字哦")

if place(board, row, col, "O"):
    print(f"  O 落在 ({row}, {col})")
    if check_win(board, row, col, "O"):
        print("  🎉 你连成四个了！")

print("\n--- 最终棋盘 ---")
show_board(board)
