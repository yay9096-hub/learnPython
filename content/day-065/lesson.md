# Day 65 · 我的学习曲线 📈

> 「今天有个惊喜。
>
> 右边「📁 文件」里多了一个 `我的学习记录.json` ——
> **那是你从 Day 1 到现在，每一天真实的学习数据**：
> 用了多久、运行了多少次、报了多少次错、看了几次提示。
>
> 今天用它画出你自己的成长曲线。」

---

## 📌 知识卡 1 · 先看看数据长什么样

```python runnable 读自己的数据
import json

with open("我的学习记录.json", encoding="utf-8") as f:
    records = json.load(f)

print(f"一共 {len(records)} 天的记录")
print(records[0])
```

每条记录长这样：

| 字段 | 意思 |
|---|---|
| `day` | 第几天 |
| `title` | 那天做的项目 |
| `stage` | 第几章 |
| `status` | `done` 已完成 / `opened` 打开过 / `locked` 还没开 |
| `minutes` | 花了多少分钟 |
| `runs` | 点了多少次运行 |
| `errors` | 报了多少次错 |
| `hints` | 看了几次提示 |

> 💡 数据可能有的天是 0 —— 那是你还没做到的部分，很正常。

---

## 📌 知识卡 2 · 折线图：看趋势 ⭐

柱状图适合**比大小**，折线图适合**看趋势**。

```python runnable 每天用了多久
import json
import matplotlib.pyplot as plt

with open("我的学习记录.json", encoding="utf-8") as f:
    records = json.load(f)

done = [r for r in records if r["status"] == "done"]

days = [r["day"] for r in done]
minutes = [r["minutes"] for r in done]

plt.figure(figsize=(9, 3.5))
plt.plot(days, minutes, marker="o", color="#8B5CF6")
plt.title("每天学习时长")
plt.xlabel("第几天")
plt.ylabel("分钟")
plt.grid(alpha=0.3)
plt.show()
```

`plt.plot(x列表, y列表)` —— 两个列表**必须一样长**，一一对应。

`marker="o"` 在每个数据点上画个圆点，看得清楚是哪几天。

---

## 📌 知识卡 3 · 两条线画一起

```python runnable 运行次数 vs 报错次数
import json
import matplotlib.pyplot as plt

with open("我的学习记录.json", encoding="utf-8") as f:
    records = json.load(f)

done = [r for r in records if r["status"] == "done"]
days = [r["day"] for r in done]
runs = [r["runs"] for r in done]
errors = [r["errors"] for r in done]

plt.figure(figsize=(9, 3.5))
plt.plot(days, runs, marker="o", label="运行次数", color="#8B5CF6")
plt.plot(days, errors, marker="s", label="报错次数", color="#EC6FA9")

plt.title("运行与报错")
plt.xlabel("第几天")
plt.legend()
plt.grid(alpha=0.3)
plt.show()
```

两个新东西：

- **`label="..."`** 给每条线起个名字
- **`plt.legend()`** 把这些名字显示成图例

⚠️ **只写 `label` 不写 `legend()` 是看不见的** —— 两个要配套。

---

## 📌 知识卡 4 · 累计曲线 ⭐

「每天多少分钟」是波动的，「累计总共多少分钟」是**一路向上**的 ——
后者看着特别有成就感。

```python runnable 累计学习时长
import json
import matplotlib.pyplot as plt

with open("我的学习记录.json", encoding="utf-8") as f:
    records = json.load(f)

done = [r for r in records if r["status"] == "done"]

days = []
cumulative = []
total = 0
for r in done:
    total += r["minutes"]
    days.append(r["day"])
    cumulative.append(round(total, 1))

plt.figure(figsize=(9, 3.5))
plt.plot(days, cumulative, marker="o", color="#34D399")
plt.fill_between(days, cumulative, alpha=0.2, color="#34D399")

plt.title(f"累计学习时长（共 {round(total)} 分钟）")
plt.xlabel("第几天")
plt.ylabel("累计分钟")
plt.grid(alpha=0.3)
plt.show()
```

`total += r["minutes"]` —— Day 17 的累加器，一路加上去。

`plt.fill_between(x, y, alpha=0.2)` 把线下面填个淡色，好看很多。

---

## 📌 知识卡 5 · 饼图：看构成

```python runnable 各章占了多少时间
import json
import matplotlib.pyplot as plt

with open("我的学习记录.json", encoding="utf-8") as f:
    records = json.load(f)

by_stage = {}
for r in records:
    if r["status"] != "done":
        continue
    key = f"第 {r['stage']} 章"
    by_stage[key] = by_stage.get(key, 0) + r["minutes"]

if by_stage:
    labels = list(by_stage.keys())
    values = list(by_stage.values())

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, autopct="%1.0f%%",
            colors=["#8B5CF6", "#EC6FA9", "#34D399", "#F59E0B",
                    "#60A5FA", "#F87171", "#A78BFA"])
    plt.title("各章学习时长占比")
    plt.show()
else:
    print("还没有完成的天数，先去学几天再回来 😉")
```

- `labels=` 每一块的名字
- `autopct="%1.0f%%"` 自动在每块上标百分比（`%1.0f` 是「小数点后 0 位」，
  最后的 `%%` 才是那个百分号）

⚠️ 饼图**不要超过 6~7 块** —— 再多就看不清了，那时候柱状图更合适。

---

## 📌 知识卡 6 · 数据可能是空的 ⚠️

```python runnable 空数据要挡住
import matplotlib.pyplot as plt

days = []
minutes = []

if len(days) == 0:
    print("还没有数据可以画")
else:
    plt.plot(days, minutes)
    plt.show()
```

如果她只学了 3 天，`done` 就只有 3 条 —— 图还是能画，只是短。
但如果**一天都没完成**，`plt.plot([], [])` 会画出一张空白图。

**真实数据一定要防空**。这是数据分析的基本功。

---

## 🛠 今天的任务 · 我的学习报告

读 `我的学习记录.json`，做一份 **2×2 的四格报告**：

| 位置 | 图 | 要求 |
|---|---|---|
| 左上 | **每天学习时长**折线图 | `marker="o"`，有标题和坐标轴标签 |
| 右上 | **累计学习时长**折线图 | 用 `fill_between` 填色，标题里带上总分钟数 |
| 左下 | **运行 vs 报错**双折线 | 两条线，有 `label` 和 `legend()` |
| 右下 | **各章时长占比**饼图 | 有 `autopct` 百分比 |

另外在终端打印一份文字摘要：

- 已完成天数 / 总天数
- 总学习分钟数、平均每天多少分钟
- 运行总次数、报错总次数
- **报错率**（报错 ÷ 运行，百分比）
- 花时间最长的那一天是哪天、做的什么

硬性要求：

- **必须防空**：一天都没完成时不能崩，要打印一句提示
- 每张图都有标题
- `tight_layout()` 收尾

> 💡 这张图值得截下来存进作品陈列馆 ——
> **它记录的是你自己走过的路。**
