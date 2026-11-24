# Day 67 · 我的雪花夜空
import turtle


def koch(length, depth):
    """画一条科赫曲线。depth 是细分层数。

    三个转角 +60 / -120 / +60 加起来正好抵消，
    所以画完之后海龟朝向和进来时一致。
    """
    if depth == 0:
        turtle.forward(length)
        return

    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)
    turtle.right(120)
    koch(length / 3, depth - 1)
    turtle.left(60)
    koch(length / 3, depth - 1)


def snowflake(length, depth):
    """三条科赫曲线围成一片雪花。"""
    for i in range(3):
        koch(length, depth)
        turtle.right(120)


def draw_at(x, y, length, depth, color, width):
    """在指定位置画一片雪花。"""
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.pencolor(color)
    turtle.pensize(width)
    snowflake(length, depth)


def count_segments(depth):
    """一条科赫曲线在这个深度下有多少段直线。"""
    return 4 ** depth


# ---------- 主流程 ----------
print("❄️ === 我的雪花夜空 === ❄️")

turtle.speed(0)
turtle.bgcolor("#0B1020")

flakes = [
    (-170, 60, 190, 3, "#A8D8FF", 2),
    (40, 110, 120, 3, "#E8B4FF", 2),
    (70, -70, 90, 2, "#FFE9A8", 1),
]

total = 0
for x, y, length, depth, color, width in flakes:
    draw_at(x, y, length, depth, color, width)
    total += 3 * count_segments(depth)

turtle.hideturtle()

print("\n--- 线段数增长表 ---")
for d in range(6):
    print(f"  depth={d}：一条边 {count_segments(d)} 段，"
          f"整片雪花 {3 * count_segments(d)} 段")

print(f"\n这次一共画了 {total} 段直线")
print("切到「🐢 画布」看看你的雪花夜空 ✨")
