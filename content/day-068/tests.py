import ast

NEEDED = ["make_board", "show_board", "can_place", "place",
          "count_line", "check_win", "is_full"]


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def board_is_2d(ctx):
    fn = ctx["ns"].get("make_board")
    if not callable(fn):
        return False
    b = fn(7)
    if not isinstance(b, list) or len(b) != 7:
        return False
    return all(isinstance(r, list) and len(r) == 7 for r in b)


def rows_independent(ctx):
    """今天最大的坑：三行不能是同一个列表。"""
    fn = ctx["ns"].get("make_board")
    if not callable(fn):
        return False
    b = fn(5)
    b[0][0] = "X"
    return b[1][0] != "X" and b[2][0] != "X"


def can_place_bounds(ctx):
    fn = ctx["ns"].get("can_place")
    mk = ctx["ns"].get("make_board")
    if not callable(fn) or not callable(mk):
        return False
    b = mk(7)
    try:
        ok1, _ = fn(b, 3, 3)
        ok2, _ = fn(b, 9, 9)
        ok3, _ = fn(b, -1, 0)
        ok4, _ = fn(b, 0, 7)
    except Exception:
        return False
    return ok1 is True and ok2 is False and ok3 is False and ok4 is False


def can_place_occupied(ctx):
    fn = ctx["ns"].get("can_place")
    mk = ctx["ns"].get("make_board")
    if not callable(fn) or not callable(mk):
        return False
    b = mk(7)
    b[2][2] = "X"
    ok, why = fn(b, 2, 2)
    return ok is False and isinstance(why, str) and len(why) > 0


def place_works(ctx):
    fn = ctx["ns"].get("place")
    mk = ctx["ns"].get("make_board")
    if not callable(fn) or not callable(mk):
        return False
    b = mk(7)
    got = fn(b, 3, 3, "X")
    if got is not True or b[3][3] != "X":
        return False
    again = fn(b, 3, 3, "O")
    return again is False and b[3][3] == "X"


def place_rejects_oob(ctx):
    """越界落子不能崩，也不能真的写进去。"""
    fn = ctx["ns"].get("place")
    mk = ctx["ns"].get("make_board")
    if not callable(fn) or not callable(mk):
        return False
    b = mk(7)
    try:
        return fn(b, 99, 99, "X") is False
    except Exception:
        return False


def count_line_ok(ctx):
    fn = ctx["ns"].get("count_line")
    mk = ctx["ns"].get("make_board")
    if not callable(fn) or not callable(mk):
        return False
    b = mk(7)
    for c in [1, 2, 3]:
        b[3][c] = "X"
    # 从 (3,0) 往右数：3 个（不含自己）
    if fn(b, 3, 0, 0, 1, "X") != 3:
        return False
    # 从 (3,4) 往左数：3 个
    if fn(b, 3, 4, 0, -1, "X") != 3:
        return False
    # 空方向数 0
    return fn(b, 3, 0, 1, 0, "X") == 0


def count_line_excludes_self(ctx):
    """不能把起点自己算进去。"""
    fn = ctx["ns"].get("count_line")
    mk = ctx["ns"].get("make_board")
    if not callable(fn) or not callable(mk):
        return False
    b = mk(7)
    b[3][3] = "X"
    return fn(b, 3, 3, 0, 1, "X") == 0


def win_horizontal(ctx):
    ctxn = ctx["ns"]
    win = ctxn.get("check_win")
    mk = ctxn.get("make_board")
    if not callable(win) or not callable(mk):
        return False
    b = mk(7)
    for c in [1, 2, 3, 4]:
        b[3][c] = "X"
    return win(b, 3, 4, "X") is True and win(b, 3, 4, "O") is False


def win_vertical(ctx):
    win = ctx["ns"].get("check_win")
    mk = ctx["ns"].get("make_board")
    if not callable(win) or not callable(mk):
        return False
    b = mk(7)
    for r in [1, 2, 3, 4]:
        b[r][2] = "O"
    return win(b, 4, 2, "O") is True


def win_diagonal(ctx):
    win = ctx["ns"].get("check_win")
    mk = ctx["ns"].get("make_board")
    if not callable(win) or not callable(mk):
        return False
    b = mk(7)
    for i in range(4):
        b[i][i] = "X"
    return win(b, 3, 3, "X") is True


def win_anti_diagonal(ctx):
    win = ctx["ns"].get("check_win")
    mk = ctx["ns"].get("make_board")
    if not callable(win) or not callable(mk):
        return False
    b = mk(7)
    for i in range(4):
        b[i][5 - i] = "O"
    return win(b, 3, 2, "O") is True


def win_needs_four(ctx):
    """三个不算赢。"""
    win = ctx["ns"].get("check_win")
    mk = ctx["ns"].get("make_board")
    if not callable(win) or not callable(mk):
        return False
    b = mk(7)
    for c in [1, 2, 3]:
        b[3][c] = "X"
    return win(b, 3, 3, "X") is False


def win_counts_both_sides(ctx):
    """左二右一，落中间也该算 4 连 —— 检验有没有数两边。"""
    win = ctx["ns"].get("check_win")
    mk = ctx["ns"].get("make_board")
    if not callable(win) or not callable(mk):
        return False
    b = mk(7)
    b[3][1] = "X"
    b[3][2] = "X"
    b[3][3] = "X"
    b[3][4] = "X"
    return win(b, 3, 3, "X") is True


def is_full_ok(ctx):
    fn = ctx["ns"].get("is_full")
    mk = ctx["ns"].get("make_board")
    if not callable(fn) or not callable(mk):
        return False
    b = mk(3)
    if fn(b) is not False:
        return False
    for r in range(3):
        for c in range(3):
            b[r][c] = "X"
    return fn(b) is True


def board_printed_with_coords(ctx):
    """棋盘输出里要有行号列号。"""
    import re
    out = ctx["stdout"]
    return re.search(r"0\s+1\s+2\s+3", out) is not None


def board_printed_times(ctx):
    """至少打印了 3 次棋盘。"""
    return ctx["stdout"].count(". . .") >= 3


def demos_three_cases(ctx):
    out = ctx["stdout"]
    return "超出棋盘" in out and "已经有子" in out


def demos_win(ctx):
    return "True" in ctx["stdout"]


def user_move(ctx):
    """玩家下的 (5,5) 要落到棋盘上。"""
    b = ctx["ns"].get("board")
    if not isinstance(b, list):
        return False
    return b[5][5] == "O"


def survived(ctx):
    return ctx["error"] is None


CASES = [
    {
        "stdin": ["5", "5"],
        "checks": [
            {"id": "defined", "desc": "七个函数都定义了",
             "type": "custom", "fn": "all_defined",
             "fail": "make_board / show_board / can_place / place / "
                     "count_line / check_win / is_full"},
            {"id": "2d", "desc": "棋盘是 7×7 的二维列表",
             "type": "custom", "fn": "board_is_2d",
             "fail": "`[[EMPTY] * size for _ in range(size)]`"},
            {"id": "independent", "desc": "各行互不影响",
             "type": "custom", "fn": "rows_independent",
             "fail": "⚠️ 今天最大的坑：写成 `[[EMPTY] * n] * n` 的话，"
                     "几行其实是**同一个列表**，下一个子会整列都变"},
            {"id": "bounds", "desc": "can_place 挡住了越界",
             "type": "custom", "fn": "can_place_bounds",
             "fail": "行列小于 0 或大于等于 size 都不行。"
                     "**越界检查必须写在取值之前**"},
            {"id": "occupied", "desc": "can_place 挡住了已有子",
             "type": "custom", "fn": "can_place_occupied",
             "fail": "`if board[row][col] != EMPTY: return False, \"这里已经有子了\"`"},
            {"id": "place", "desc": "落子成功 / 重复落子失败",
             "type": "custom", "fn": "place_works",
             "fail": "落子前先调 `can_place`，不合法就返回 `False` 且**不改棋盘**"},
            {"id": "place-oob", "desc": "越界落子不会崩",
             "type": "custom", "fn": "place_rejects_oob",
             "fail": "`place(board, 99, 99, \"X\")` 要安静地返回 False"},
            {"id": "count", "desc": "count_line 数得对",
             "type": "custom", "fn": "count_line_ok",
             "fail": "用 `while` 沿方向走，越界或者不是自己的子就停"},
            {"id": "count-self", "desc": "count_line 不含起点",
             "type": "custom", "fn": "count_line_excludes_self",
             "fail": "从 `row + dr, col + dc` 开始数 —— 起点在 check_win 里单独算 1"},
            {"id": "win-h", "desc": "横向四连判赢",
             "type": "custom", "fn": "win_horizontal",
             "fail": "方向 (0, 1)。而且换个棋子要返回 False"},
            {"id": "win-v", "desc": "竖向四连判赢",
             "type": "custom", "fn": "win_vertical",
             "fail": "方向 (1, 0)"},
            {"id": "win-d", "desc": "斜向四连判赢",
             "type": "custom", "fn": "win_diagonal",
             "fail": "方向 (1, 1)"},
            {"id": "win-a", "desc": "反斜向四连判赢",
             "type": "custom", "fn": "win_anti_diagonal",
             "fail": "方向 (1, -1) —— 四个方向一个都不能少"},
            {"id": "win-3", "desc": "只有三连不算赢",
             "type": "custom", "fn": "win_needs_four",
             "fail": "要 `>= WIN`（4）才算，三个不行"},
            {"id": "win-both", "desc": "两边都要数",
     "type": "custom", "fn": "win_counts_both_sides",
             "fail": "`1 + 正方向 + 反方向` —— 只数一边的话，"
                     "落在中间时会漏判"},
            {"id": "full", "desc": "is_full 判断正确",
             "type": "custom", "fn": "is_full_ok",
             "fail": "每行用 `if EMPTY in row: return False`"},
            {"id": "coords", "desc": "棋盘带行号列号",
             "type": "custom", "fn": "board_printed_with_coords",
             "fail": "第一行打印列号，每行前面打印行号 —— "
                     "没坐标玩家不知道该输什么"},
            {"id": "shown", "desc": "至少打印了三次棋盘",
             "type": "custom", "fn": "board_printed_times",
             "fail": "初始、开局后、结束时都要显示一次"},
            {"id": "cases", "desc": "演示了三种落子情况",
             "type": "custom", "fn": "demos_three_cases",
             "fail": "能下 / 已有子 / 超出棋盘，三种都要打印出来"},
            {"id": "win-demo", "desc": "演示了判赢",
             "type": "custom", "fn": "demos_win",
             "fail": "摆出一个四连，打印 `check_win(...)` 的结果"},
            {"id": "user", "desc": "玩家的落子生效了",
             "type": "custom", "fn": "user_move",
             "fail": "把 input 拿到的行列转成 int，落一个 O。"
                     "棋盘变量要叫 `board`",
             },
            {"id": "survive", "desc": "全程没有崩溃",
             "type": "custom", "fn": "survived",
             "fail": "玩家可能输入非数字 —— 用 try/except 兜住"},
        ],
    }
]
