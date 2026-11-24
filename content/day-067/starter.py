# Day 67 · 我的雪花夜空
import turtle


# TODO 1: koch(length, depth) -> 一条科赫曲线
#   出口：depth == 0 时 turtle.forward(length) 然后 return
#   否则：四段 koch(length / 3, depth - 1)
#         中间的转角依次是 左60 / 右120 / 左60


# TODO 2: snowflake(length, depth) -> 三条曲线围成雪花
#   循环 3 次：画一条 koch，然后 turtle.right(120)


# TODO 3: draw_at(x, y, length, depth, color, width)
#   抬笔 -> goto -> 落笔 -> 设颜色和粗细 -> 画雪花


# TODO 4: count_segments(depth) -> 4 ** depth


# ---------- 主流程 ----------
# TODO 5: turtle.speed(0) + 深色背景
# TODO 6: 用 draw_at 画至少 3 片雪花，大小/颜色/深度都不同
#         至少有一片 depth >= 3
# TODO 7: hideturtle()
# TODO 8: 终端打印 depth 0~5 的线段数表，以及这次一共画了多少段
