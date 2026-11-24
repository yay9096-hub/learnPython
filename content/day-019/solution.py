# Day 19 · 我的星空
import random
import turtle

turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.penup()

palette = ["#FFFFFF", "#FFE9A8", "#A8D8FF", "#FFC8E4"]

# ---------- 星星 ----------
for i in range(120):
    turtle.goto(random.randint(-250, 250), random.randint(-190, 190))

    if random.randint(1, 12) == 1:
        turtle.dot(random.randint(9, 15), "#FFE9A8")
    else:
        turtle.dot(random.randint(2, 6), random.choice(palette))

# ---------- 月亮 ----------
turtle.goto(150, 80)
turtle.pendown()
turtle.pencolor("#FFE9A8")
turtle.fillcolor("#FFE9A8")
turtle.begin_fill()
turtle.circle(45)
turtle.end_fill()

turtle.penup()
turtle.goto(172, 92)
turtle.pendown()
turtle.pencolor("#0B0A1A")
turtle.fillcolor("#0B0A1A")
turtle.begin_fill()
turtle.circle(45)
turtle.end_fill()

turtle.hideturtle()
