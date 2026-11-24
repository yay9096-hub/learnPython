# Day 30 · 图鉴系统 📖

> 「昨天的字典只装了**一个**角色。
> 今天装一整本图鉴 —— 然后学会**把它整个遍历一遍**。」

---

## 📌 知识卡 1 · 一本图鉴

```python runnable 名字 -> 战力
book = {
    "星野樱": 820,
    "月见琉璃": 995,
    "天野灯": 640,
}

print(book)
print(book["月见琉璃"])
```

键是名字，值是战力 —— 想查谁直接报名字，不用先找位置。
**这就是字典比列表强的地方。**

---

## 📌 知识卡 2 · 直接遍历拿到的是「键」

```python runnable for 直接遍历字典
book = {"星野樱": 820, "月见琉璃": 995, "天野灯": 640}

for name in book:
    print(name)
```

⚠️ 拿到的是**键**，不是值。想要值，再用键去取：

```python runnable 用键取值
book = {"星野樱": 820, "月见琉璃": 995, "天野灯": 640}

for name in book:
    print(f"{name} 的战力是 {book[name]}")
```

能用，但有点绕。有更直接的办法 👇

---

## 📌 知识卡 3 · `.items()` —— 一次拿到键和值 ⭐

```python runnable items 是最常用的
book = {"星野樱": 820, "月见琉璃": 995, "天野灯": 640}

for name, power in book.items():
    print(f"{name} 的战力是 {power}")
```

`for 键, 值 in 字典.items():` —— **这是遍历字典最常用的写法**，记住它。

跟 Day 27 的 `for atk, name in pairs:` 是同一件事：**一次拿两个**（解包）。

---

## 📌 知识卡 4 · `.keys()` 和 `.values()`

```python runnable 三兄弟
book = {"星野樱": 820, "月见琉璃": 995, "天野灯": 640}

print(list(book.keys()))
print(list(book.values()))
print(list(book.items()))
```

| 方法 | 给你什么 | 常用来 |
|---|---|---|
| `.keys()` | 所有键 | 看有哪些成员 |
| `.values()` | 所有值 | **拿去统计** |
| `.items()` | 键值成对 | **遍历** |

`.values()` 拿去做统计特别顺手（Day 25 学的那套全能用）：

```python runnable 字典 + 统计
book = {"星野樱": 820, "月见琉璃": 995, "天野灯": 640}

print(f"总战力：{sum(book.values())}")
print(f"最高战力：{max(book.values())}")
print(f"平均战力：{round(sum(book.values()) / len(book), 1)}")
```

> 💡 `.keys()` / `.values()` / `.items()` 返回的不是真列表，
> 想切片或排序要先 `list(...)` 包一下。直接遍历和 `sum()` 则不用。

---

## 📌 知识卡 5 · 边遍历边判断

Day 25 的条件统计，换到字典上一模一样：

```python runnable 找出战力超过 800 的
book = {"星野樱": 820, "月见琉璃": 995, "天野灯": 640, "水城凛": 998}

strong = 0
for name, power in book.items():
    if power > 800:
        print(f"⭐ {name}（{power}）")
        strong += 1

print(f"共 {strong} 人达到 800 以上")
```

找出最强的是谁：

```python runnable 找最值（这次不用平行列表了）
book = {"星野樱": 820, "月见琉璃": 995, "天野灯": 640}

best_name = ""
best_power = 0

for name, power in book.items():
    if power > best_power:
        best_power = power
        best_name = name

print(f"最强：{best_name}（{best_power}）")
```

对比 Day 25 那段 —— **字典版清爽多了**，不用担心两个列表对不上号。

---

## 📌 知识卡 6 · 新增、删除、检查

```python runnable 图鉴的日常维护
book = {"星野樱": 820, "月见琉璃": 995}

book["夜刀神澪"] = 770                # 收录新角色
print(f"收录后：{len(book)} 人")

if "天野灯" in book:                   # 先检查
    del book["天野灯"]
else:
    print("图鉴里本来就没有天野灯")

for name, power in book.items():
    print(f"  {name}: {power}")
```

⚠️ **不要在遍历字典的同时增删它** —— 会报错。
真要边遍历边删，先把要删的收集到一个列表里，遍历完再删。

---

## 🛠 今天的任务 · 图鉴系统

给你一本图鉴（名字 → 战力），做一套完整的管理功能：

```python
book = {
    "星野樱": 820,
    "月见琉璃": 995,
    "天野灯": 640,
    "水城凛": 998,
    "夜刀神澪": 770,
}
```

| 要求 | 说明 |
|---|---|
| 用 `.items()` 逐行显示整本图鉴 | `星野樱 —— 战力 820` |
| 报出收录人数 | `len()` |
| 用 `.values()` 算总战力和平均战力 | 平均值保留 1 位小数 |
| 找出战力最高的是谁 | 名字和数值都要 |
| 统计战力 >= 800 的有几人 | 循环 + `if` |
| 收录一个新角色 | 直接赋值，收录后再报一次人数 |
| 问玩家查谁 | `input()`，用 `in` 或 `.get()` 安全查询 |
| 查不到要提示「图鉴中暂无此人」 | |

> 💡 自己先算：5 人、总战力 4223、平均 844.6、最强水城凛(998)、800 以上有 3 人。
