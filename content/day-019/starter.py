# Day 19 · 我的星空
import random
import turtle

turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.penup()

palette = ["#FFFFFF", "#FFE9A8", "#A8D8FF", "#FFC8E4"]

# TODO 1: 用 for 循环撒至少 60 颗星星
#   每一颗：
#     ① 随机坐标  turtle.goto(random.randint(-250, 250), random.randint(-190, 190))
#     ② 用 if 判断是不是「亮星」（10% 概率画大一点）
#     ③ turtle.dot(随机大小, 随机颜色)


# TODO 2: 画一个月亮（circle + begin_fill/end_fill）
#   小技巧：先画满月，再用背景色画一个圆叠上去咬掉一块

