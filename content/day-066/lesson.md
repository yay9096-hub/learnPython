# Day 66 · 文本捕手 🔍

> 「Day 28 你用 `split` 拆过弹幕，Day 48 用 `in` 搜过日记。
> 但如果要找的是『**所有的日期**』『**所有的数字**』『**所有的邮箱**』呢？
>
> 用 `if` 和 `split` 能做，但要写一大堆。
> 今天学**正则表达式** —— 一行搞定。」

---

## 📌 知识卡 1 · 第一个正则

```python runnable 揪出所有数字
import re

text = "小樱今天学了 45 分钟，运行了 12 次，报错 3 次。"

numbers = re.findall(r"\d+", text)
print(numbers)
```

`re.findall(模式, 文本)` —— **找出所有匹配的，返回一个列表**。

拆开看这个模式：

| 部分 | 意思 |
|---|---|
| `r"..."` | 前面加 `r` 表示「原样字符串」，反斜杠不用转义 |
| `\d` | **一个数字**（0~9） |
| `+` | **一个或多个**（连着的数字算一整个） |

⚠️ 那个 `r` 很重要：

```python runnable 不加 r 的话反斜杠要写两遍
import re
text = "有 42 个"
print(re.findall(r"\d+", text))
print(re.findall("\d+", text))
```

两个一样，但第一个好读得多。**正则模式永远加 `r`。**

---

## 📌 知识卡 2 · 几个最常用的符号

```python runnable 三个基本字符类
import re

text = "Day 65 用了 45.5 分钟 abc_123"

print(re.findall(r"\d", text))
print(re.findall(r"\d+", text))
print(re.findall(r"[a-z]+", text))
print(re.findall(r"\w+", text))
```

| 符号 | 匹配什么 |
|---|---|
| `\d` | 一个数字 |
| `\w` | 一个字母、数字或下划线（中文也算） |
| `\s` | 一个空白（空格、换行、Tab） |
| `.` | **任意**一个字符 |
| `[abc]` | a 或 b 或 c 中的一个 |
| `[a-z]` | 小写字母中的一个 |
| `[^abc]` | **不是** a b c 的一个字符 |

量词（跟在后面，说「几个」）：

| 量词 | 意思 |
|---|---|
| `+` | 1 个或更多 |
| `*` | 0 个或更多 |
| `?` | 0 个或 1 个（可有可无） |
| `{4}` | 正好 4 个 |
| `{2,4}` | 2 到 4 个 |

```python runnable 量词对比
import re
text = "a aa aaa aaaa"
print(re.findall(r"a{2}", text))
print(re.findall(r"a{2,3}", text))
print(re.findall(r"a+", text))
```

---

## 📌 知识卡 3 · 揪日期 ⭐

```python runnable 找出所有日期
import re

log = """
2026-09-01 完成了 Day 1
2026-09-02 完成了 Day 2 和 Day 3
今天是 2026-09-15，一共学了 15 天
"""

dates = re.findall(r"\d{4}-\d{2}-\d{2}", log)
print(dates)
```

`\d{4}-\d{2}-\d{2}` 读作：**4 个数字、横杠、2 个数字、横杠、2 个数字**。

这就是正则的价值 —— **模式即描述**。你怎么描述它，就怎么写。

---

## 📌 知识卡 4 · 分组：只要其中一部分 ⭐

```python runnable 括号把想要的圈出来
import re

log = "2026-09-01 完成了 Day 1，2026-09-02 完成了 Day 2"

years = re.findall(r"(\d{4})-\d{2}-\d{2}", log)
print(years)

parts = re.findall(r"(\d{4})-(\d{2})-(\d{2})", log)
print(parts)
```

**括号 `( )` 标记「我要这部分」**：

- 一个括号 → 返回那部分的列表
- 多个括号 → 返回**元组**的列表（Day 33 的元组！）

```python runnable 分组 + 解包
import re

text = "樱 88 分，琉璃 95 分，灯 72 分"

pairs = re.findall(r"(\w+) (\d+) 分", text)
print(pairs)

for name, score in pairs:
    print(f"  {name}：{score}")
```

`for name, score in pairs:` —— 又是 Day 33 的解包。

---

## 📌 知识卡 5 · `re.sub` —— 替换 ⭐

```python runnable 把数字打码
import re

text = "我的手机是 13812345678，另一个是 13987654321"

masked = re.sub(r"\d", "*", text)
print(masked)

partial = re.sub(r"(\d{3})\d{4}(\d{4})", r"\1****\2", text)
print(partial)
```

`re.sub(模式, 替换成什么, 文本)`。

第二个例子里的 `\1` `\2` 指的是**第 1 个、第 2 个括号里匹配到的内容** ——
所以前三位和后四位保留，中间四位变成星号。

---

## 📌 知识卡 6 · 三个实用模式

```python runnable 邮箱、网址、中文
import re

text = """
联系方式：sakura@example.com 或者 admin@test.org
主页 https://example.com/page 和 http://test.cn
备注：这是中文说明文字
"""

print(re.findall(r"[\w.]+@[\w.]+", text))
print(re.findall(r"https?://[\w./]+", text))
print(re.findall(r"[\u4e00-\u9fa5]+", text))
```

- 邮箱：`[\w.]+@[\w.]+` —— 「一堆字符 @ 一堆字符」
- 网址：`https?://[\w./]+` —— `s?` 表示 s **可有可无**，所以 http 和 https 都能匹配
- 中文：`[\u4e00-\u9fa5]+` —— 汉字在 Unicode 里的范围

> 💡 正则很容易写得又长又难懂。**能用 `split` 和 `in` 解决的就别上正则** ——
> 但遇到「找出所有符合某种格式的东西」，它无可替代。

---

## 📌 知识卡 7 · 找到位置：`search` 和 `match`

```python runnable findall / search / sub 的分工
import re

text = "Day 65 用了 45 分钟"

print(re.findall(r"\d+", text))

m = re.search(r"Day (\d+)", text)
if m:
    print(m.group(0))
    print(m.group(1))
else:
    print("没找到")
```

| 函数 | 干什么 |
|---|---|
| `re.findall` | 找**全部**，返回列表（最常用） |
| `re.search` | 找**第一个**，返回一个匹配对象或 `None` |
| `re.sub` | **替换** |

⚠️ `re.search` 找不到时返回 `None`，**用之前一定要 `if m:` 判断**。

`m.group(0)` 是整个匹配，`m.group(1)` 是第 1 个括号里的部分。

---

## 🛠 今天的任务 · 日志分析器

给你一段混着各种信息的学习日志（starter 里有），写一套提取工具：

| 函数 | 说明 |
|---|---|
| `find_dates(text)` | 找出所有 `YYYY-MM-DD` 日期 |
| `find_numbers(text)` | 找出所有整数（返回**数字**列表，不是文字） |
| `find_emails(text)` | 找出所有邮箱 |
| `find_urls(text)` | 找出所有网址（http 和 https 都要） |
| `find_day_minutes(text)` | 找出所有「Day N 用了 M 分钟」，返回 `[(N, M), ...]` 的**数字**元组列表 |
| `mask_phones(text)` | 把手机号中间四位打码 |
| `count_chinese(text)` | 数出中文字符总数 |

主流程要求：

- 每个函数各调一次，把结果打印出来
- 用 `find_day_minutes` 的结果算出**总时长**和**平均时长**
- 打印打码后的完整文本
- 用 `re.search` 找出日志里的第一个日期，找不到要提示

> ⚠️ `find_numbers` 和 `find_day_minutes` 返回的必须是**数字**（`int`），
> 不是字符串 —— `re.findall` 给的都是文字，要自己转。
