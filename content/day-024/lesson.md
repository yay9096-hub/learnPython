# Day 24 · 背包系统 🎒

> 「昨天的队伍名单是**固定 5 人**。
> 但背包不一样 —— 捡到东西要变长，用掉要变短。
> 今天学会让列表**动起来**。」

---

## 📌 知识卡 1 · `.append()` —— 往末尾加

```python runnable 捡东西
bag = []

bag.append("木剑")
print(bag)

bag.append("红药水")
print(bag)

bag.append("面包")
print(bag)
```

`.append()` 永远加在**最后面**，一次加一个。

注意写法：`列表.append(东西)` —— 跟 Day 5 的 `.upper()` 一样，是挂在东西身上的**方法**。

### ⚠️ 一个和 Day 5 不同的地方

Day 5 学过「方法不改原变量，要用 `=` 接住」：

```python runnable 字符串方法：要接住
s = "fire"
s.upper()
print(s)
```

但**列表方法直接改原列表，不用接**：

```python runnable 列表方法：不用接
bag = ["木剑"]
bag.append("药水")
print(bag)
```

```python runnable 接了反而错（跑一下看）
bag = ["木剑"]
bag = bag.append("药水")
print(bag)
```

打印出 `None`！因为 `.append()` **不返回任何东西**，它是直接在原列表上动手。

> 🧠 记住这条分界：
> **字符串方法造新的（要接住）；列表方法改原来的（别接）。**

---

## 📌 知识卡 2 · 配合循环：批量捡

```python runnable 一次捡一堆
bag = []
loot = ["铁剑", "护符", "红药水", "蓝药水"]

for item in loot:
    bag.append(item)
    print(f"捡到了 {item}！背包现在有 {len(bag)} 件")

print(bag)
```

---

## 📌 知识卡 3 · `.remove()` —— 按内容删

```python runnable 用掉一瓶药水
bag = ["木剑", "红药水", "面包", "红药水"]

bag.remove("红药水")
print(bag)
```

⚠️ 两个坑：

1. `.remove()` **只删第一个匹配的**，重复的还会剩下
2. 删一个**不存在**的东西会报错：

```python runnable 删不存在的会报错
bag = ["木剑", "面包"]
bag.remove("屠龙刀")
```

所以删之前要先用 `in` 确认（Day 13 学过）：

```python runnable 安全地删
bag = ["木剑", "面包"]
item = "屠龙刀"

if item in bag:
    bag.remove(item)
    print(f"扔掉了 {item}")
else:
    print(f"背包里没有 {item}")
```

> 💡 **先检查再操作**，是写健壮程序的基本功。

---

## 📌 知识卡 4 · `.pop()` —— 弹出并拿到手

```python runnable 掏出最后一件
bag = ["木剑", "面包", "红药水"]

last = bag.pop()
print(f"掏出了：{last}")
print(f"背包剩下：{bag}")
```

`.pop()` 跟 `.remove()` 的区别：

| | 按什么删 | 会不会给你 |
|---|---|---|
| `.remove("面包")` | 按**内容** | 不给，直接扔了 |
| `.pop()` | 按**位置**（默认最后一个） | **会把它交给你** |

也可以指定位置：

```python runnable 掏出指定位置的
bag = ["木剑", "面包", "红药水"]
first = bag.pop(0)
print(f"掏出了：{first}")
print(bag)
```

---

## 📌 知识卡 5 · `.insert()` —— 插队

```python runnable 插到最前面
bag = ["木剑", "面包"]

bag.insert(0, "钥匙")
print(bag)
```

`insert(位置, 东西)`：`0` 就是插到最前面。

---

## 📌 知识卡 6 · 统计有几个

```python runnable count 数重复的
bag = ["红药水", "木剑", "红药水", "红药水"]
print(bag.count("红药水"))
```

一张小抄，今天全在这里：

| 方法 | 干什么 |
|---|---|
| `.append(x)` | 末尾加一个 |
| `.insert(i, x)` | 插到第 i 个位置 |
| `.remove(x)` | 按内容删第一个匹配的 |
| `.pop()` / `.pop(i)` | 弹出并返回 |
| `.count(x)` | 数有几个 |
| `x in 列表` | 在不在里面 |
| `len(列表)` | 一共几个 |

---

## 🛠 今天的任务 · 背包系统

做一个能交互的背包：

| 要求 | 说明 |
|---|---|
| 背包从空开始 | `bag = []` |
| 用 `for` 批量捡 4 件初始装备 | 用 `.append()` |
| 问玩家想捡什么，加进背包 | `input()`，再 `.append()` |
| 问玩家想扔什么 | `input()` |
| 扔之前先用 `in` 检查 | 有就扔（`.remove()`），没有就提示「没有」 |
| 用 `.pop()` 掏出最后一件并显示 | 打印「掏出了 xxx」 |
| 每一步都打印背包内容和件数 | 让人看得见变化 |

> 💡 判题会跑两遍：一遍扔一个**背包里有**的东西，一遍扔一个**没有**的。
> 两种情况都要处理好，**不能崩**。
