# Day 48 · 翻开日记 📖

> 「昨天写进去了，今天读回来。
>
> 而且不只是读 —— 还要能**数有多少行**、**找出某一天**、
> **统计写了多少字**。文件一旦读进来，Day 23~34 学的全部本事就都能用上了。」

---

## 📌 知识卡 1 · 三种读法

先准备一个文件：

```python runnable 准备素材
lines = [
    "2026-09-02 今天学会了写文件",
    "2026-09-03 写文件比想象中简单",
    "2026-09-04 刷新页面文件还在，有点感动",
]

with open("日记.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("素材准备好了")
```

**读法一：`read()` —— 整个读成一个字符串**

```python runnable read 整个读
with open("日记.txt", encoding="utf-8") as f:
    text = f.read()

print(type(text))
print(f"一共 {len(text)} 个字")
print(text)
```

**读法二：`readlines()` —— 读成列表**

```python runnable readlines 读成列表
with open("日记.txt", encoding="utf-8") as f:
    lines = f.readlines()

print(type(lines))
print(f"一共 {len(lines)} 行")
print(lines)
```

⚠️ 注意打印出来的列表里 **每一项末尾都带着 `\n`**。

**读法三：`for line in f` —— 逐行遍历（最常用）**

```python runnable 直接遍历文件对象
with open("日记.txt", encoding="utf-8") as f:
    for line in f:
        print(f"→ {line}")
```

看到行与行之间多了空行吗？也是 `\n` 造成的。

---

## 📌 知识卡 2 · ⚠️ 那个多出来的换行符

```python runnable 看清楚它长什么样
with open("日记.txt", encoding="utf-8") as f:
    lines = f.readlines()

print(repr(lines[0]))
print(repr(lines[-1]))
```

`repr()` 会把看不见的字符显示出来 —— 前几行末尾都有 `\n`。

**解决办法：`.rstrip()`**

```python runnable rstrip 削掉行尾
with open("日记.txt", encoding="utf-8") as f:
    for line in f:
        clean = line.rstrip("\n")
        print(f"→ {clean}")
```

也可以用 Day 5 的 `.strip()`（首尾都削），处理文件时更常用：

```python runnable strip 一步到位
with open("日记.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f]

print(lines)
```

> 🧠 **从文件读出来的每一行，第一件事就是 `.strip()`。**
> 这几乎是条肌肉记忆。

---

## 📌 知识卡 3 · 用哪种读法

| 读法 | 得到 | 什么时候用 |
|---|---|---|
| `f.read()` | 一个大字符串 | 要整体处理（统计字数、搜索） |
| `f.readlines()` | 列表 | 需要**反复用**这些行（排序、切片） |
| `for line in f` | 一行一行 | **只过一遍**，文件很大也不怕 |

```python runnable 大文件为什么要用第三种
with open("日记.txt", encoding="utf-8") as f:
    count = 0
    for line in f:
        if line.strip():
            count += 1

print(f"非空行数：{count}")
```

第三种**一次只把一行放进内存**。文件有 10GB 也跑得动，
而 `read()` 会试图把 10GB 全塞进内存 —— 电脑会直接卡死。

---

## 📌 知识卡 4 · 读进来就能用上前面所有本事 ⭐

```python runnable 读文件 + 第三章的全部技能
with open("日记.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

print(f"共 {len(lines)} 篇")
print(f"最早一篇：{lines[0]}")
print(f"最新一篇：{lines[-1]}")

total_chars = 0
for line in lines:
    total_chars += len(line)
print(f"一共写了 {total_chars} 个字")

for line in lines:
    if "文件" in line:
        print(f"  提到「文件」：{line}")
```

`len` / `[0]` / `[-1]` / 累加 / `in` 判断 —— **全是第三章的老朋友**。

文件只是数据的**来源**，读进来之后处理方式完全一样。

---

## 📌 知识卡 5 · 拆解每一行

日记的格式是「日期 空格 内容」，可以用 Day 28 的 `split` 拆开：

```python runnable split 拆出日期和内容
with open("日记.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(" ", 1)
        date = parts[0]
        content = parts[1] if len(parts) > 1 else ""
        print(f"  日期：{date}")
        print(f"  内容：{content}")
```

⚠️ `split(" ", 1)` 里那个 `1` 表示**最多拆一次** ——
这样内容里的空格不会被继续拆开。

---

## 📌 知识卡 6 · 带行号

```python runnable enumerate 加行号
with open("日记.txt", encoding="utf-8") as f:
    for i, line in enumerate(f, start=1):
        print(f"{i}. {line.strip()}")
```

`enumerate(f, start=1)` —— 那个 `start=1` 让编号从 1 开始，
不用再写 `i + 1` 了（Day 38 学的关键字参数）。

---

## 🛠 今天的任务 · 日记阅读器

先造一个日记文件，然后写一套读取分析工具：

| 函数 | 返回 | 说明 |
|---|---|---|
| `read_all(filename)` | 字符串 | 整个文件内容 |
| `read_lines(filename)` | 列表 | 每项一行，**已经 strip 过、去掉空行** |
| `count_lines(filename)` | 数字 | 有多少篇（非空行） |
| `count_chars(filename)` | 数字 | 一共多少字（不算换行符） |
| `find_by_date(filename, date)` | 字符串 / None | 找出某一天的日记，找不到返回 None |
| `search(filename, keyword)` | 列表 | 所有含关键词的行 |
| `show_numbered(filename)` | 无 | 带行号打印全部 |

主流程要求：

- 先用 `"w"` 造一个至少 5 篇的日记文件
- 打印总篇数和总字数
- 用 `show_numbered` 带行号列出全部
- 用 `find_by_date` 查一个**存在**的日期和一个**不存在**的日期
- 问玩家一个关键词，用 `search` 找出所有相关的行；一条都没有要提示

> 💡 读出来的每一行记得 `.strip()`，否则统计字数会多算换行符。
