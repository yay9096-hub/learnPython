# Day 17 · 十连抽 🎴

> 「Day 10 你做了抽卡机，但只能**单抽** —— 因为那时候还不会循环。
> 我当时说『学了循环你会有更优雅的写法』。今天兑现。」

---

## 📌 知识卡 1 · 十连 = 循环十次

```python runnable 十连抽
import random

for i in range(10):
    rarity = random.choice(["SSR", "SR", "SR", "R", "R", "R", "R", "R"])
    print(f"第 {i + 1} 抽：{rarity}")
```

就这么简单。**把单抽的代码缩进到循环里，就是十连。**

注意 `i + 1` —— `i` 从 0 开始，但人类数数从 1 开始，所以显示时加 1。
这个小细节以后天天遇到。

---

## 📌 知识卡 2 · 边循环边统计

光抽不算数，得知道**出了几个 SSR**。这就要用到**累加器模式**：

```python runnable 统计 SSR 数量
import random

ssr_count = 0                      # ① 循环前先归零

for i in range(10):
    rarity = random.choice(["SSR", "SR", "SR", "R", "R", "R", "R", "R"])
    print(f"第 {i + 1} 抽：{rarity}")

    if rarity == "SSR":
        ssr_count += 1             # ② 循环里累加

print(f"十连结束，出了 {ssr_count} 个 SSR")   # ③ 循环后使用
```

**统计三步走**，跟 Day 14 的计数器是同一个模式：

| 步骤 | 位置 |
|---|---|
| ① 初始化（归零） | 循环**外面**，循环之前 |
| ② 累加 | 循环**里面** |
| ③ 使用结果 | 循环**外面**，循环之后 |

⚠️ 把 ① 写进循环里，每圈都归零，永远统计不出来 —— 这是最常见的错误。

---

## 📌 知识卡 3 · `break` —— 抽到就收手

有时候不需要跑完全程。比如「一直抽，抽到 SSR 就停」：

```python runnable 抽到 SSR 就停
import random

for i in range(100):
    rarity = random.choice(["SSR", "SR", "R", "R", "R"])
    print(f"第 {i + 1} 抽：{rarity}")

    if rarity == "SSR":
        print("🎉 出货了！收手！")
        break
```

`break` 的意思是「**立刻跳出整个循环**」，后面几圈全部不跑了。

多跑几次，每次停的位置都不一样 ✨

> 🧠 `break` 只能跳出**它所在的那一层**循环。
> 嵌套循环里的 `break` 只跳出内层，外层还会继续。

---

## 📌 知识卡 4 · `continue` —— 这一圈不算，下一圈

`continue` 是「**跳过这一圈剩下的部分**，直接开始下一圈」：

```python runnable 只报告稀有卡，普通卡跳过
import random

for i in range(10):
    rarity = random.choice(["SSR", "SR", "R", "R", "R"])

    if rarity == "R":
        continue                        # 普通卡，不报了

    print(f"第 {i + 1} 抽：{rarity} ⭐")

print("（普通卡已自动跳过）")
```

| | 效果 |
|---|---|
| `break` | 整个循环**结束** |
| `continue` | 这一圈**跳过**，循环继续 |

> 💡 `continue` 常用来「过滤掉不想处理的情况」，让后面的代码不用套一层 `if`。

---

## 📌 知识卡 5 · `while True` + `break`

这是个非常常用的组合：「一直做下去，直到某个条件出现」。

```python runnable 抽到 SSR 为止，看看要几抽
import random

count = 0

while True:                            # 永远成立 —— 靠 break 出来
    count += 1
    rarity = random.choice(["SSR", "SR", "R", "R", "R", "R", "R", "R"])

    if rarity == "SSR":
        break

print(f"第 {count} 抽出的 SSR")
```

`while True` 本身是个**死循环** —— 唯一的出口就是 `break`。

⚠️ 用它的时候必须**先想好出口在哪**，否则真的会停不下来。
（放心，网站有输出上限保护，随便试。）

---

## 📌 知识卡 6 · 找最值

统计的另一个常见变种：**找出最大的那个**。

```python runnable 十连里最高战力是多少
import random

best = 0                              # 先设一个不可能赢的初始值

for i in range(10):
    power = random.randint(50, 999)
    print(f"第 {i + 1} 抽：战力 {power}")

    if power > best:
        best = power                  # 遇到更大的就换掉

print(f"最强的一张：{best} 战力")
```

套路：**先设一个「肯定会被超过」的初始值，遇到更大的就替换。**

---

## 🛠 今天的任务 · 十连抽

做一个完整的十连抽系统：

| 要求 | 说明 |
|---|---|
| 用 `for` 循环抽 10 次 | 每次显示第几抽、稀有度、角色、战力 |
| 稀有度用 `random.choice` | SSR 概率要低（清单里多放几个 R） |
| 战力用 `random.randint(50, 999)` | 每张卡不一样 |
| 统计 SSR 数量 | 存进一个变量，最后报出来 |
| 找出最高战力 | 最后报出「最强的一张」 |
| 用一次 `break` 或 `continue` | 比如抽到 SSR 就特别提示，或者跳过某些显示 |
| 十连结束后出总结 | 输出里要有「十连结束」 |

> 💡 判题会把随机固定住来检查统计对不对，所以**统计逻辑必须真的正确** ——
> 不能凭感觉写个数字糊弄过去 😉
