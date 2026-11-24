# Day 8 · 魔法星星海报
import turtle

turtle.speed(8)

# ---------- 五角星 ----------
turtle.pensize(5)
turtle.pencolor("#F59E0B")

turtle.penup()
turtle.goto(-100, 40)
turtle.pendown()

turtle.forward(200)
turtle.right(144)
turtle.forward(200)
turtle.right(144)
turtle.forward(200)
turtle.right(144)
turtle.forward(200)
turtle.right(144)
turtle.forward(200)

# ---------- 光环 ----------
turtle.penup()
turtle.goto(0, -60)
turtle.pendown()
turtle.pencolor("#8B5CF6")
turtle.pensize(3)
turtle.circle(120)

# ---------- 署名 ----------
turtle.penup()
turtle.goto(-40, -140)
turtle.pendown()
turtle.pencolor("#EC6FA9")
turtle.write("星野樱", font=("", 22, "normal"))

turtle.hideturtle()
