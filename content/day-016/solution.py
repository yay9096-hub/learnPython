# Day 16 · 我的万花筒
import turtle

turtle.speed(0)
turtle.pensize(2)
turtle.bgcolor("#1A1625")

colors = ["#8B5CF6", "#EC6FA9", "#F59E0B", "#34D399"]

layers = 12
sides = 4

for i in range(layers):
    turtle.pencolor(colors[i % 4])

    for j in range(sides):
        turtle.forward(90)
        turtle.right(360 / sides)

    turtle.right(360 / layers)

turtle.hideturtle()
