# Day 10 · 命运抽卡机
import random
import turtle

print("🎴 ===== 命 运 抽 卡 机 ===== 🎴")

player = input("旅人，报上你的名字：").strip()

rarity = random.choice(["SSR", "SR", "SR", "R", "R", "R", "R", "R"])
char = random.choice(["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"])
element = random.choice(["火", "水", "风", "雷", "光", "暗"])
atk = random.randint(50, 999)
stars = "★" * len(rarity)

print(f"\n{player}，你的卡片降临了 ——")
print("=" * 34)
print(f"  稀有度：{rarity} {stars}")
print(f"  角  色：{char}")
print(f"  属  性：{element}")
print(f"  攻击力：{atk}")
print("=" * 34)

# ---------- 把卡框画出来 ----------
color = random.choice(["#F59E0B", "#EC6FA9", "#8B5CF6", "#34D399"])

turtle.speed(0)
turtle.bgcolor("#1A1625")
turtle.pensize(6)
turtle.pencolor(color)

turtle.penup()
turtle.goto(-110, -160)
turtle.pendown()

turtle.forward(220)
turtle.left(90)
turtle.forward(320)
turtle.left(90)
turtle.forward(220)
turtle.left(90)
turtle.forward(320)

turtle.penup()
turtle.goto(-80, 40)
turtle.pendown()
turtle.pencolor("#FFE9A8")
turtle.write(char, font=("", 26, "bold"))

turtle.penup()
turtle.goto(-80, -20)
turtle.pendown()
turtle.pencolor(color)
turtle.write(f"{rarity} · {element} · ATK {atk}", font=("", 14, "normal"))

turtle.hideturtle()
