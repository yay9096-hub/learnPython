## 提示 1 · 先把「抽」的部分写完

这一关看着长，其实前半段就是五行：

```python
player = input("旅人，报上你的名字：").strip()
rarity = random.choice(["SSR", "SR", "SR", "R", "R", "R"])
char = random.choice(["星野樱", "月见琉璃", "天野灯"])
element = random.choice(["火", "水", "风", "雷"])
atk = random.randint(50, 999)
```

写到这里先运行一次，用 `print(rarity)` 看看有没有抽出东西来。

## 提示 2 · 卡面就是 Day 2 学的 f-string

```python
print(f"\n{player}，你的卡片降临了 ——")
print("=" * 34)
print(f"  稀有度：{rarity}")
print(f"  角  色：{char}")
print(f"  属  性：{element}")
print(f"  攻击力：{atk}")
print("=" * 34)
```

`"=" * 34` 是 Day 5 的重复魔法，做分隔线最省事。

## 提示 3 · 卡框就是一个长方形

长方形 = 四条边，每条边之后左转 90 度：

```python
color = random.choice(["#F59E0B", "#EC6FA9", "#8B5CF6"])

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
```

然后挪到框里写角色名：

```python
turtle.penup()
turtle.goto(-80, 40)
turtle.pendown()
turtle.pencolor("#FFE9A8")
turtle.write(char, font=("", 26, "bold"))
```
