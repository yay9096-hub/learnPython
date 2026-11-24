# Day 28 · 弹幕分析器 💬

> 「到现在为止，列表都是你自己一个个敲进去的。
> 但真实世界的数据是**一大段文字** —— 一屏弹幕、一首歌词、一份名单。
> 今天学会把文字**拆成列表**，然后用前几天学的全部本事去分析它。」

---

## 📌 知识卡 1 · `.split()` —— 文字变列表 ⭐

```python runnable 按空格拆
line = "牛啊 前排 牛啊 打卡 牛啊"

words = line.split()
print(words)
print(len(words))
```

`.split()` 不加参数时，**按空格拆**（连续多个空格算一个）。

拆出来是一个**列表** —— 于是前五天学的所有列表本事，立刻全都能用了：

```python runnable 拆完就能统计
line = "牛啊 前排 牛啊 打卡 牛啊"
words = line.split()

print(f"一共 {len(words)} 条")
print(f"「牛啊」出现了 {words.count('牛啊')} 次")
print(f"第一条：{words[0]}")
print(f"最后一条：{words[-1]}")
```

---

## 📌 知识卡 2 · 按别的符号拆

括号里放什么，就按什么拆：

```python runnable 按逗号拆
csv = "星野樱,995,火"
parts = csv.split(",")
print(parts)
```

```python runnable 按换行拆（多行文本）
poem = """春眠不觉晓
处处闻啼鸟
夜来风雨声"""

lines = poem.split("\n")
print(lines)
print(f"一共 {len(lines)} 行")
```

`"\n"` 是 Day 6 学的换行符。按它拆，就把多行文本变成了一行一项的列表。

> 💡 处理表格数据（CSV）、日志、配置文件，全靠 `.split()` 起步。

---

## 📌 知识卡 3 · ⚠️ 中文没有空格怎么办

```python runnable 中文句子拆不开
line = "今天天气真好"
print(line.split())
```

拆不动 —— 因为中文词之间没空格。

拆成**单个字**可以用 `list()`：

```python runnable 拆成单字
line = "今天天气真好"
chars = list(line)
print(chars)
print(f"「天」出现了 {chars.count('天')} 次")
```

真正的中文分词很复杂（要靠专门的库），今天我们的弹幕**都用空格分好**，
或者按**单字**统计 —— 够用了。

---

## 📌 知识卡 4 · `.join()` —— 列表变文字（反过来）

```python runnable 拼回去
words = ["牛啊", "前排", "打卡"]

print(" ".join(words))
print(" | ".join(words))
print("".join(words))
```

写法有点怪：**是「连接符」调用 `.join()`，把列表放括号里**。

念作：「用『空格』把这个列表连起来」。

```python runnable split 和 join 是一对
line = "牛啊 前排 打卡"

words = line.split()          # 文字 → 列表
back = " ".join(words)        # 列表 → 文字

print(words)
print(back)
print(line == back)
```

⚠️ `.join()` 只能拼**字符串**列表。有数字要先转：

```python runnable 数字要先转成文字
nums = [1, 2, 3]

texts = []
for n in nums:
    texts.append(str(n))

print("-".join(texts))
```

---

## 📌 知识卡 5 · 组合拳：找出刷得最多的词

把前几天的本事全用上：

```python runnable 词频 Top 1
line = "牛啊 前排 牛啊 打卡 牛啊 前排"
words = line.split()

seen = []          # 已经数过的词，避免重复统计
best_word = ""
best_count = 0

for w in words:
    if w in seen:
        continue                    # Day 17 的 continue
    seen.append(w)

    n = words.count(w)              # Day 24 的 count
    if n > best_count:              # Day 20 的找最值
        best_count = n
        best_word = w

print(f"刷得最多的是「{best_word}」，共 {best_count} 次")
```

这段用到了 **Day 17 的 continue、Day 20 的找最值、Day 24 的 count** ——
新知识只有一个 `.split()`，其余全是复习。

> 🧠 编程学到后面就是这样：**新东西越来越少，组合越来越多。**

---

## 📌 知识卡 6 · 几个清洗数据的小工具

真实数据总是脏的，这几个方法专门用来擦干净：

```python runnable 清洗三件套
raw = "  牛啊 , 前排,打卡  "

print(f"[{raw.strip()}]")
print(raw.replace(" ", ""))
print(raw.strip().replace(" ", "").split(","))
```

- `.strip()` 削首尾空格（Day 5 学过）
- `.replace(旧, 新)` 替换（Day 5 学过）
- 串起来用，一步步把脏数据擦干净

---

## 🛠 今天的任务 · 弹幕分析器

给你一段弹幕，做一份分析报告：

```python
danmaku = "牛啊 前排 牛啊 打卡 awsl 牛啊 前排 泪目 awsl 前排 牛啊 打卡"
```

| 要求 | 说明 |
|---|---|
| 拆成列表 | 用 `.split()`，存进 `words` |
| 报出总条数 | `len()` |
| 找出所有**不重复**的词 | 存进 `unique`，用循环 + `in` 去重 |
| 报出不重复的词有几个 | |
| 每个词各刷了几次 | 用循环 + `.count()` 逐个打印 |
| 找出刷得最多的词和次数 | 存进 `best_word` / `best_count` |
| 用 `.join()` 把不重复的词拼成一行 | 用 `" / "` 连接，打印出来 |

> 💡 自己先数一下：总共 12 条、不重复的有 5 个、刷得最多的是「牛啊」4 次。
