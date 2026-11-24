# Day 9 · 专属魔法阵
import turtle

turtle.speed(0)
turtle.bgcolor("#1A1625")

# ---------- 外层圆环 ----------
turtle.penup()
turtle.goto(0, -150)
turtle.pendown()
turtle.pensize(4)
turtle.pencolor("#8B5CF6")
turtle.circle(150)

# ---------- 内层圆环 ----------
turtle.penup()
turtle.goto(0, -110)
turtle.pendown()
turtle.pencolor("#EC6FA9")
turtle.pensize(2)
turtle.circle(110)

# ---------- 中心填充三角 ----------
turtle.penup()
turtle.goto(-80, -50)
turtle.pendown()
turtle.setheading(0)
turtle.pencolor("#F59E0B")
turtle.fillcolor("#3B2A5C")
turtle.pensize(3)

turtle.begin_fill()
turtle.forward(160)
turtle.left(120)
turtle.forward(160)
turtle.left(120)
turtle.forward(160)
turtle.end_fill()

# ---------- 放射线 ----------
turtle.pencolor("#34D399")
turtle.pensize(2)

turtle.penup()
turtle.goto(0, 0)
turtle.setheading(90)
turtle.pendown()
turtle.forward(150)

turtle.penup()
turtle.goto(0, 0)
turtle.setheading(210)
turtle.pendown()
turtle.forward(150)

turtle.penup()
turtle.goto(0, 0)
turtle.setheading(330)
turtle.pendown()
turtle.forward(150)

# ---------- 装饰点 ----------
turtle.penup()
turtle.goto(0, 150)
turtle.dot(18, "#F59E0B")
turtle.goto(-130, -75)
turtle.dot(18, "#EC6FA9")
turtle.goto(130, -75)
turtle.dot(18, "#8B5CF6")

# ---------- 咒语 ----------
turtle.goto(-45, -10)
turtle.pendown()
turtle.pencolor("#FFE9A8")
turtle.write("星野樱", font=("", 24, "bold"))

turtle.hideturtle()
