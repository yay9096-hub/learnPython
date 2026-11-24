# Day 43 · 我的分形森林
import turtle

TRUNK_COLOR = "#5B3A2E"
LEAF_COLOR = "#7BC96F"
SHRINK = 0.72
ANGLE = 28


def countdown(n):
    """从 n 倒数到 1，数完喊发射。"""
    if n <= 0:
        print("发射！🚀")
        return
    print(n)
    countdown(n - 1)


def factorial(n):
    """算 n 的阶乘：n × (n-1) × ... × 1。"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def tree(length, depth):
    """画一根树枝，并在末端递归长出两根更小的。

    画完必须退回起点、角度转回来，
    否则上一层继续画的时候位置就错了。
    """
    if depth == 0:
        return

    if depth <= 2:
        turtle.pencolor(LEAF_COLOR)
    else:
        turtle.pencolor(TRUNK_COLOR)
    turtle.pensize(depth)

    turtle.forward(length)

    turtle.left(ANGLE)
    tree(length * SHRINK, depth - 1)

    turtle.right(ANGLE * 2)
    tree(length * SHRINK, depth - 1)

    turtle.left(ANGLE)
    turtle.backward(length)


# ---------- 主流程 ----------
print("🌳 === 分形森林 === 🌳")

countdown(5)
print(f"5 的阶乘是 {factorial(5)}")

turtle.speed(0)
turtle.bgcolor("#FDF9FF")
turtle.penup()
turtle.goto(0, -200)
turtle.left(90)
turtle.pendown()

tree(100, 7)

turtle.hideturtle()
