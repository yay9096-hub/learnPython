# Day 69 · 个人学习仪表盘 📋

> 「这是最后一个命题项目。
>
> 你要把学过的**全部东西**用在一起：读文件、处理数据、画图、
> 生成报告、存档 —— 做一个真正拿得出手的作品。
>
> 数据还是你自己的。」

---

## 🔍 第七章你拿到的武器

| 天 | 学到的 |
|---|---|
| D64 | matplotlib 基础：柱状图、标题、坐标轴、subplot |
| D65 | 折线图、饼图、图例、真实数据分析 |
| D66 | 正则表达式：从文本里精准提取 |
| D67 | 递归分形：科赫雪花 |
| D68 | 二维列表：棋盘、方阵 |

加上前六章的一切 —— **今天全用上。**

---

## 📌 知识卡 · 三个收尾技巧

今天没有大块新知识，只有三个让作品更完整的小技巧。

### 1. 保存图片到文件 ⭐

```python runnable savefig 把图存下来
import matplotlib.pyplot as plt

plt.figure(figsize=(6, 3))
plt.bar(["A", "B", "C"], [3, 7, 5], color="#8B5CF6")
plt.title("示例")
plt.tight_layout()

plt.savefig("示例图.png", dpi=110)
plt.show()

print("图存好了，去右边「📁 文件」看看")
```

`plt.savefig(文件名, dpi=110)` —— **要写在 `plt.show()` 之前**，
`show()` 之后图就被清掉了。

`dpi` 是清晰度，110 左右刚好。

### 2. 生成文字报告

```python runnable 用 join 拼一份多行报告
lines = []
lines.append("=" * 40)
lines.append("        我的学习报告")
lines.append("=" * 40)
lines.append("完成天数：42")
lines.append("总时长：1860 分钟")
lines.append("=" * 40)

report = "\n".join(lines)
print(report)

with open("学习报告.txt", "w", encoding="utf-8") as f:
    f.write(report)
```

**先把每一行 append 进列表，最后 join 一次** ——
比一路 `text += ...` 干净得多。

### 3. 文字版进度条

```python runnable 不用图也能做可视化
def bar(value, total, width=20):
    """画一条文字进度条。"""
    if total <= 0:
        return "░" * width
    filled = int(value / total * width)
    filled = max(0, min(filled, width))
    percent = int(value / total * 100)
    return "█" * filled + "░" * (width - filled) + f" {percent}%"


print("第一章 " + bar(10, 10))
print("第二章 " + bar(8, 12))
print("第三章 " + bar(0, 12))
```

⚠️ 里面的 `min` / `max` 夹取（Day 57）和防除零（Day 41）一个都不能少 ——
真实数据什么情况都有。

---

## 🎯 今天的作品 · 学习仪表盘

读 `我的学习记录.json`（右边「📁 文件」里已经有了），产出**三样东西**：

### 一、终端里的文字仪表盘

```
╔══════════════════════════════════════╗
║        派森酱学院 · 学习仪表盘         ║
╚══════════════════════════════════════╝

  总览
    完成天数    12 / 70
    总时长      486 分钟（8.1 小时）
    平均每天    40.5 分钟
    运行次数    213    报错 58 次（27.2%）

  各章进度
    第 1 章  ██████████ 100%  (10/10)
    第 2 章  ██░░░░░░░░  16%  (2/12)
    第 3 章  ░░░░░░░░░░   0%  (0/12)
    ...

  记录
    最投入的一天   Day 3「伤害计算器」58 分钟
    最顺的一天     Day 5（0 次报错）
    最费劲的一天   Day 3（7 次报错）
```

### 二、一张四格图表（`plt.savefig` 存成 PNG）

| 位置 | 内容 |
|---|---|
| 左上 | 每天时长折线图 |
| 右上 | 各章完成度**横向柱状图** |
| 左下 | 累计时长曲线（带 `fill_between`） |
| 右下 | 运行 vs 报错双折线（带图例） |

### 三、一份文字报告文件

把终端里那份仪表盘**原样写进 `学习报告.txt`**。

---

### 必须实现的函数

| 函数 | 说明 |
|---|---|
| `load_records(filename)` | 读数据。文件不存在返回 `[]` |
| `overview(records)` | 返回一个**字典**：完成数、总数、总时长、平均、运行数、报错数、报错率 |
| `by_stage(records)` | 返回 `{章号: (完成数, 总数, 总时长)}` |
| `bar(value, total, width=20)` | 文字进度条，**要防除零** |
| `highlights(records)` | 返回 `(最投入的, 最顺的, 最费劲的)` 三条记录；没数据返回 `(None, None, None)` |
| `build_report(records)` | 返回整份报告的**字符串**（不是 print！） |
| `draw_charts(records, filename)` | 画四格图并 `savefig` |

### 硬性要求

- **一天都没完成时不能崩** —— 打印一句提示就结束
- `build_report` 只**返回字符串**，打印交给主流程
- 报告要同时**打印到终端**和**写进文件**
- 图表每格都有标题，最后 `tight_layout()`

> 🏆 做完这一关，你就有了一个**能截图发给别人看**的完整作品。
