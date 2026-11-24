# Day 33 · 星座连线图
import turtle

names  = ["天枢", "天璇", "天玑", "天权", "玉衡", "开阳", "摇光"]
points = [(-160, 40), (-100, 70), (-40, 60), (10, 20), (70, 10), (130, 40), (180, 90)]
sizes  = [10, 8, 9, 7, 11, 9, 12]

print("✨ === 北斗七星 === ✨")

# ---------- 列表显示 ----------
for name, (x, y), size in zip(names, points, sizes):
    print(f"  {name} ({x}, {y}) 亮度 {size}")

# ---------- 星座中心 ----------
sum_x = 0
sum_y = 0
for x, y in points:
    sum_x += x
    sum_y += y

center_x = round(sum_x / len(points), 1)
center_y = round(sum_y / len(points), 1)
print(f"\n星座中心：({center_x}, {center_y})")

# ---------- 最亮的星 ----------
best_name = ""
best_size = 0
best_point = (0, 0)

for name, point, size in zip(names, points, sizes):
    if size > best_size:
        best_size = size
        best_name = name
        best_point = point

print(f"最亮的星：{best_name}（亮度 {best_size}）")

# ---------- 画图 ----------
turtle.speed(0)
turtle.bgcolor("#0B0A1A")
turtle.pensize(2)
turtle.pencolor("#5A5480")
turtle.penup()

first = True
for name, (x, y), size in zip(names, points, sizes):
    turtle.goto(x, y)
    if first:
        turtle.pendown()
        first = False
    turtle.dot(size * 2, "#FFE9A8")

# ---------- 标注最亮的星 ----------
bx, by = best_point
turtle.penup()
turtle.goto(bx + 12, by + 8)
turtle.pendown()
turtle.pencolor("#EC6FA9")
turtle.write(best_name, font=("", 16, "bold"))

turtle.hideturtle()
