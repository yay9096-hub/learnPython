# Day 33 · 坐标与打包 📦

> 「其实你已经用过好多次解包了 ——
> `for i, member in enumerate(team)`、`for name, power in book.items()`、
> `for atk, name in pairs`。
>
> 今天把这个『一次拿好几个』的原理讲清楚。
> 这也是下周学函数的地基。」

---

## 📌 知识卡 1 · 元组：不能改的列表

```python runnable 圆括号
point = (100, 50)

print(point)
print(point[0])
print(len(point))
```

用法跟列表几乎一样 —— 能取值、能 `len()`、能遍历、能切片。

**唯一的区别：建好就不能改。**

```python runnable 元组改不了（会报错）
point = (100, 50)
point[0] = 999
```

| | 列表 `[]` | 元组 `()` |
|---|---|---|
| 能改吗 | ✅ 能 | ❌ **不能** |
| 有顺序吗 | ✅ 有 | ✅ 有 |
| 能编号取吗 | ✅ 能 | ✅ 能 |

> 🧠 什么时候用元组？
> **表示「一个整体」的时候** —— 坐标 `(x, y)`、颜色 `(r, g, b)`、日期 `(2026, 9, 1)`。
> 这些东西改掉其中一个就没意义了，所以干脆不让改。

---

## 📌 知识卡 2 · 解包：一次拆给多个变量 ⭐

```python runnable 解包
point = (100, 50)

x, y = point

print(f"x 是 {x}，y 是 {y}")
```

左边写几个变量，右边就拆成几份 —— **个数必须一样**：

```python runnable 个数对不上会报错
point = (100, 50, 30)
x, y = point
```

列表也能解包：

```python runnable 列表一样能拆
data = ["星野樱", 340]
name, hp = data
print(name, hp)
```

回头看 Day 27 那句 `for atk, name in pairs:` —— **就是在解包**，
每一圈把 `[820, "星野樱"]` 拆成两个变量。

---

## 📌 知识卡 3 · 多重赋值和交换

```python runnable 一行给两个变量赋值
a, b = 1, 2
print(a, b)
```

其实右边 `1, 2` 就是个元组（圆括号可以省略）。

最经典的用法 —— **一行交换两个变量**：

```python runnable 交换
a = 1
b = 2

a, b = b, a
print(a, b)
```

别的语言要写三行（借一个临时变量），Python 一行搞定。

> 💡 Day 22 那句 `top, chances = 50, 10` 就是多重赋值，
> 当时说「原理第三章讲」—— 就是这个。

---

## 📌 知识卡 4 · 一堆坐标点

```python runnable 列表里装元组
path = [(0, 0), (100, 50), (150, -30), (-80, 60)]

for point in path:
    print(point)

print("---")

for x, y in path:
    print(f"x={x}, y={y}")
```

第二种写法**边遍历边解包**，直接拿到 x 和 y —— 清爽多了。

拿去画画（Day 8 的 turtle）：

```python runnable 按坐标画一条折线
import turtle

path = [(-150, -50), (-50, 80), (50, -60), (150, 40)]

turtle.speed(0)
turtle.pensize(3)
turtle.pencolor("#8B5CF6")
turtle.penup()

first = True
for x, y in path:
    turtle.goto(x, y)
    if first:
        turtle.pendown()
        first = False
    turtle.dot(10, "#EC6FA9")
```

---

## 📌 知识卡 5 · `zip()` —— 把两个列表配成对 ⭐

Day 25 你用 `for i in range(len(names))` 配对两个列表。
有更漂亮的办法：

```python runnable zip 配对
names = ["星野樱", "月见琉璃", "天野灯"]
hps = [340, 280, 310]

for name, hp in zip(names, hps):
    print(f"{name} 的血量是 {hp}")
```

`zip()` 把两个列表**一一配成对**，再解包出来。

对比一下：

```python runnable 两种写法
names = ["樱", "琉璃"]
hps = [340, 280]

for i in range(len(names)):
    print(names[i], hps[i])

for name, hp in zip(names, hps):
    print(name, hp)
```

后者不用管编号，也不会数错。**三个列表也能一起 zip。**

```python runnable 三个一起配
names = ["樱", "琉璃"]
hps = [340, 280]
atks = [88, 95]

for name, hp, atk in zip(names, hps, atks):
    print(f"{name}: HP {hp} ATK {atk}")
```

⚠️ 长度不一样时，`zip` 按**最短的**来，多的直接丢掉。

想看看 zip 出来到底是什么，`list()` 一下：

```python runnable zip 的真面目
names = ["樱", "琉璃"]
hps = [340, 280]
print(list(zip(names, hps)))
```

**是一串元组** —— 所以才能解包。

---

## 🛠 今天的任务 · 星座连线图

给你一组星座数据：

```python
names  = ["天枢", "天璇", "天玑", "天权", "玉衡", "开阳", "摇光"]
points = [(-160, 40), (-100, 70), (-40, 60), (10, 20), (70, 10), (130, 40), (180, 90)]
sizes  = [10, 8, 9, 7, 11, 9, 12]
```

| 要求 | 说明 |
|---|---|
| 用 `zip()` 把三组数据配对遍历 | 一行显示 `天枢 (-160, 40) 亮度 10` |
| 遍历时把坐标**解包**成 x, y | `for name, (x, y), size in zip(...)` |
| 算出所有 x 的平均值和 y 的平均值 | 就是「星座中心」，保留 1 位小数 |
| 找出最亮的星（size 最大） | 名字和亮度都要 |
| 用 turtle 把七颗星按坐标连成折线 | 每颗星画一个 `dot`，大小用 size |
| 在最亮那颗旁边写上名字 | `turtle.write()` |
| 深色背景 | 星空嘛 |

> 💡 自己先算：x 平均 12.9、y 平均 47.1、最亮是摇光（12）。
