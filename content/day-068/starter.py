# Day 68 · 文字版五子棋（7x7，连成 4 个就赢）
SIZE = 7
WIN = 4
EMPTY = "."


# TODO 1: make_board(size) -> size x size 的棋盘
#   ⚠️ 用 [[EMPTY] * size for _ in range(size)]
#      千万别写 [[EMPTY] * size] * size


# TODO 2: show_board(board) -> 打印棋盘，带行号和列号


# TODO 3: can_place(board, row, col) -> (能不能下, 说明)
#   越界 -> (False, "超出棋盘了")
#   已有子 -> (False, "这里已经有子了")
#   ⚠️ 越界检查必须在取值之前


# TODO 4: place(board, row, col, piece) -> 落子，返回是否成功


# TODO 5: count_line(board, row, col, dr, dc, piece)
#   从 (row,col) 沿 (dr,dc) 方向数有几个连着的 piece（不含自己）


# TODO 6: check_win(board, row, col, piece)
#   四个方向 [(0,1), (1,0), (1,1), (1,-1)]
#   每个方向：1 + 正向 + 反向 >= WIN 就赢


# TODO 7: is_full(board) -> 棋盘满了吗


# ---------- 主流程 ----------
# TODO 8: 造棋盘，显示初始状态
# TODO 9: 预先摆几步棋，每步显示棋盘
# TODO 10: 演示 can_place 的三种情况
# TODO 11: 摆出一个 4 连，演示 check_win 判出胜利
# TODO 12: 问玩家输入行和列（分两次问），检查后落子
# TODO 13: 打印最终棋盘和结果
