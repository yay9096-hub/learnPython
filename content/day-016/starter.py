# Day 16 · 我的万花筒
import turtle

turtle.speed(0)
turtle.pensize(2)
turtle.bgcolor("#1A1625")

colors = ["#8B5CF6", "#EC6FA9", "#F59E0B", "#34D399"]

layers = 12          # 转多少次
sides = 4            # 每个基本图形几条边

# TODO: 外层循环 —— 重复 layers 次
#   每一圈里：
#     ① 换个颜色： turtle.pencolor(colors[i % 4])
#     ② 内层循环画一个正 sides 边形
#     ③ 转一点点： turtle.right(360 / layers)

