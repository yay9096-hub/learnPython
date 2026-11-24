# Day 10 · 命运抽卡机 🎴

> 「第一章的最后一天。
> 今天给程序加上最后一味调料 —— **随机**。
> 加上它，你的程序每次运行结果都不一样，这才有玩头。」

---

## 📌 知识卡 1 · `random` 工具箱

跟 turtle 一样，先搬进来：

```python runnable 掷个骰子（多跑几次试试）
import random

print(random.randint(1, 6))
```

**连点几次 ▶**，每次数字都不一样 ✨

`random.randint(a, b)` 给你一个 a 到 b 之间的随机整数，
⚠️ **两端都包含** —— `randint(1, 6)` 可能是 1，也可能是 6。

```python runnable 随机属性值
import random

hp = random.randint(200, 500)
mp = random.randint(80, 260)
print(f"HP: {hp}  MP: {mp}")
```

---

## 📌 知识卡 2 · `random.choice` —— 从一堆里挑一个

```python runnable 随机稀有度
import random

rarity = random.choice(["SSR", "SR", "R", "N"])
print(f"稀有度：{rarity}")
```

方括号 `[ ]` 里用逗号隔开的一串东西，叫**列表**。
它是 Python 里超重要的一个概念，第三章会专门讲。
今天你只要知道：**它就是一个备选清单**，`choice` 会从里面随便挑一个。

```python runnable 随机角色 + 随机属性
import random

name = random.choice(["星野樱", "月见琉璃", "天野灯", "水城凛"])
element = random.choice(["火", "水", "风", "雷", "光", "暗"])
print(f"{name} · {element}属性")
```

---

## 📌 知识卡 3 · 想让 SSR 更稀有？

最简单的办法：**在清单里多放几份常见的**。

```python runnable 调概率的土办法（但很好用）
import random

rarity = random.choice(["SSR", "SR", "SR", "R", "R", "R", "R", "R"])
print(rarity)
```

8 个里只有 1 个 SSR，所以抽中的概率是 1/8。
多跑几次感受一下手气 (๑•̀ㅂ•́)و

> 🧠 学了循环和条件判断之后，你会有更优雅的写法。
> 但「土办法」能解决问题就是好办法 —— **先能跑，再变好**。

---

## 📌 知识卡 4 · 随机 + turtle = 每次都不一样的画

这是今天最酷的部分：**把随机数喂给画笔**。

```python runnable 随机颜色的卡框（多跑几次）
import random
import turtle

color = random.choice(["#F59E0B", "#EC6FA9", "#8B5CF6", "#34D399"])

turtle.bgcolor("#1A1625")
turtle.pensize(6)
turtle.pencolor(color)

turtle.penup()
turtle.goto(-110, -150)
turtle.pendown()

turtle.forward(220)
turtle.left(90)
turtle.forward(300)
turtle.left(90)
turtle.forward(220)
turtle.left(90)
turtle.forward(300)
```

每次运行，卡框颜色都不一样。

也可以直接随机生成色号 —— `randint` 三次分别当红绿蓝：

```python runnable 完全随机的颜色
import random
import turtle

r = random.randint(0, 255)
g = random.randint(0, 255)
b = random.randint(0, 255)

turtle.pensize(10)
turtle.pencolor(r, g, b)
turtle.circle(100)
print(f"这次抽到的颜色：({r}, {g}, {b})")
```

---

## 🛠 今天的任务 · 命运抽卡机

做一台抽卡机。流程是：

**问名字 → 随机生成一张卡 → 打印卡面 → 用 turtle 把卡框画出来**

| 要求 | 说明 |
|---|---|
| 问玩家名字 | `input()`，存进 `player` |
| 随机稀有度 | `random.choice`，存进 `rarity` |
| 随机角色名 | `random.choice`，存进 `char` |
| 随机属性 | `random.choice`，存进 `element` |
| 随机攻击力 | `random.randint(50, 999)`，存进 `atk` |
| 打印卡面 | 用 f-string，上面五项都要出现 |
| 画卡框 | turtle 画一个矩形，颜色随机 |
| 卡框里写上角色名 | `turtle.write()` |

> 🎉 做完这一关，第一章就通关了！
> 你已经会：输出、变量、运算、输入、字符串处理、排版、画图、随机 —— 八项技能。
