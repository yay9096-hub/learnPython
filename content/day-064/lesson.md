# Day 64 · 第一张图表 📊

> 「第三章你算出过一堆数字：总血量、平均攻击、排行榜。
> 但一串数字看着累 —— **一张图三秒就懂**。
>
> 今天用的 `matplotlib` 不是玩具，是**真正的科学家和数据分析师在用的库**。
> NASA 发布的图、论文里的图表，很多都是它画的。」

---

## 📌 知识卡 1 · 你的第一张图 ⭐

```python runnable 三行画一张柱状图
import matplotlib.pyplot as plt

plt.bar(["樱", "琉璃", "灯"], [88, 95, 72])
plt.show()
```

点 ▶ 之后**切到右边的「📊 图表」标签页** —— 图就在那里。

> 💡 第一次运行会慢几秒 —— 绘图库有 12MB，要载入一下。
> 之后就快了。

三行拆开看：

| 行 | 干什么 |
|---|---|
| `import matplotlib.pyplot as plt` | 把绘图工具搬进来，简称 `plt` |
| `plt.bar(名字列表, 数值列表)` | 画柱状图 |
| `plt.show()` | 显示出来 |

`as plt` 是给它起个短名字 —— **全世界的 Python 代码都这么写**，
你看别人的代码也会是 `plt`。

---

## 📌 知识卡 2 · ⚠️ 没有标题的图等于没画

```python runnable 光秃秃的图（不合格）
import matplotlib.pyplot as plt

plt.bar(["樱", "琉璃", "灯"], [88, 95, 72])
plt.show()
```

看着是有图了，但：**这是什么？88 是什么单位？横轴是人还是月份？**

```python runnable 加上说明才算完整
import matplotlib.pyplot as plt

plt.bar(["樱", "琉璃", "灯"], [88, 95, 72])

plt.title("队伍攻击力对比")
plt.xlabel("角色")
plt.ylabel("攻击力")

plt.show()
```

三件套：

| 函数 | 说的是 |
|---|---|
| `plt.title("...")` | 这张图讲什么 |
| `plt.xlabel("...")` | 横轴是什么 |
| `plt.ylabel("...")` | 竖轴是什么 |

> 🧠 一条职业习惯：**画完图先问自己「别人看得懂吗」。**
> 看不懂的图，画得再漂亮也是废图。

---

## 📌 知识卡 3 · 颜色和样式

```python runnable 换个颜色
import matplotlib.pyplot as plt

plt.bar(["樱", "琉璃", "灯"], [88, 95, 72], color="#8B5CF6")
plt.title("队伍攻击力")
plt.show()
```

每根柱子不同颜色 —— 传一个**颜色列表**：

```python runnable 每根柱子一个色
import matplotlib.pyplot as plt

names = ["樱", "琉璃", "灯", "凛"]
values = [88, 95, 72, 110]
colors = ["#8B5CF6", "#EC6FA9", "#34D399", "#F59E0B"]

plt.bar(names, values, color=colors)
plt.title("队伍攻击力")
plt.ylabel("攻击力")
plt.show()
```

⚠️ 颜色列表要**跟数据一样长**，不然会循环使用。

---

## 📌 知识卡 4 · 横着画：`barh`

名字太长时，竖着画会挤成一团：

```python runnable 竖着画：名字挤在一起
import matplotlib.pyplot as plt

names = ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"]
values = [88, 95, 72, 110, 66]

plt.bar(names, values)
plt.title("竖着画")
plt.show()
```

```python runnable 横着画：清爽多了
import matplotlib.pyplot as plt

names = ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"]
values = [88, 95, 72, 110, 66]

plt.barh(names, values, color="#A78BFA")
plt.title("横着画")
plt.xlabel("攻击力")
plt.show()
```

`barh` 里的 `h` 是 horizontal（水平）。**名字长就横着画** —— 这是个实用经验。

---

## 📌 知识卡 5 · 图的大小和网格

```python runnable 调大小、加网格
import matplotlib.pyplot as plt

names = ["樱", "琉璃", "灯", "凛"]
values = [88, 95, 72, 110]

plt.figure(figsize=(7, 4))
plt.bar(names, values, color="#8B5CF6")
plt.title("队伍攻击力对比")
plt.ylabel("攻击力")
plt.grid(axis="y", alpha=0.3)
plt.show()
```

- `plt.figure(figsize=(宽, 高))` —— 单位是英寸，`(7, 4)` 是个常用尺寸
- `plt.grid(axis="y", alpha=0.3)` —— 加淡淡的横向网格线，方便读数值
- `alpha` 是透明度，0 全透明、1 不透明

⚠️ `plt.figure(...)` 要写在**画之前**。

---

## 📌 知识卡 6 · 在柱子上标数值 ⭐

```python runnable 让读者不用猜
import matplotlib.pyplot as plt

names = ["樱", "琉璃", "灯", "凛"]
values = [88, 95, 72, 110]

plt.figure(figsize=(7, 4))
plt.bar(names, values, color="#8B5CF6")

for i in range(len(names)):
    plt.text(i, values[i] + 2, str(values[i]), ha="center")

plt.title("队伍攻击力对比")
plt.ylabel("攻击力")
plt.ylim(0, 130)
plt.show()
```

`plt.text(x, y, 文字)` 在指定位置写字：

- `x` 用 `i`（第几根柱子，从 0 开始）
- `y` 用 `values[i] + 2`（比柱子高一点点）
- `ha="center"` 让文字水平居中对齐

`plt.ylim(0, 130)` 把竖轴范围拉高一点，不然数字会顶到图外面。

---

## 📌 知识卡 7 · 一次画好几张

```python runnable subplot 分成两格
import matplotlib.pyplot as plt

names = ["樱", "琉璃", "灯"]
hp = [340, 280, 310]
atk = [88, 95, 72]

plt.figure(figsize=(9, 3.5))

plt.subplot(1, 2, 1)
plt.bar(names, hp, color="#EC6FA9")
plt.title("血量")

plt.subplot(1, 2, 2)
plt.bar(names, atk, color="#8B5CF6")
plt.title("攻击力")

plt.tight_layout()
plt.show()
```

`plt.subplot(行数, 列数, 第几个)` —— `(1, 2, 1)` 是「1 行 2 列的第 1 格」。

`plt.tight_layout()` 自动调整间距，防止标题重叠。**多图时记得加。**

---

## 🛠 今天的任务 · 队伍数据可视化

数据（starter 里给好了）：

```python
names = ["星野樱", "月见琉璃", "天野灯", "水城凛", "风见幽香"]
hp    = [340, 280, 310, 250, 360]
atk   = [88, 95, 72, 110, 90]
```

| 要求 | 说明 |
|---|---|
| 设置图的尺寸 | `plt.figure(figsize=(...))` |
| 分成两格 | 用 `subplot`，左边血量、右边攻击力 |
| 左边用**横向**柱状图 | 名字长，用 `barh` |
| 右边用**竖向**柱状图 | 用 `bar` |
| 两张图都有标题 | `plt.title(...)` |
| 两张图都有坐标轴标签 | `xlabel` 或 `ylabel` |
| 右图在柱子上标出数值 | 用 `plt.text(...)` 循环标 |
| 用不同颜色 | 两张图的配色要区分开 |
| `tight_layout()` + `show()` | 收尾 |

另外在**终端里**也打印一份文字版摘要：总血量、平均攻击、最强的是谁。

> 💡 图画好之后切到「📊 图表」标签看。不满意就改颜色改尺寸再跑 ——
> **调图是个反复试的过程，这很正常。**
