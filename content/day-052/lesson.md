# Day 52 · CSV 成绩单 📊

> 「CSV 是这个世界上**最常见**的数据格式。
> 你们老师导出的成绩表、银行的账单、任何 Excel 另存为的表格 —— 都是它。
>
> 它长得极其朴素：**第一行是表头，后面每行一条记录，字段用逗号分开。**」

---

## 📌 知识卡 1 · CSV 到底长什么样

```python runnable 造一个成绩单
rows = [
    "姓名,语文,数学,英语",
    "星野樱,88,92,79",
    "月见琉璃,95,78,91",
    "天野灯,72,85,68",
]

with open("成绩.csv", "w", encoding="utf-8") as f:
    f.write("\n".join(rows) + "\n")

with open("成绩.csv", encoding="utf-8") as f:
    print(f.read())
```

去右边「📁 文件」点开 `成绩.csv` 看看 —— **就是纯文本**，没有任何魔法。

Excel、WPS、Google Sheets 打开这个文件，都会显示成一张漂亮的表格。

---

## 📌 知识卡 2 · 读 CSV：拆表头 + 拆每一行

```python runnable 手工解析
with open("成绩.csv", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

header = lines[0].split(",")
print(f"表头：{header}")

for line in lines[1:]:
    parts = line.split(",")
    print(parts)
```

关键是 `lines[0]` 是表头，`lines[1:]` 才是数据（Day 26 的切片）。

---

## 📌 知识卡 3 · ⚠️ 读出来全是文字

```python runnable 不转换就出事
with open("成绩.csv", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

parts = lines[1].split(",")
print(parts)
print(parts[1] + parts[2])
```

`88 + 92` 变成了 `"8892"` —— 因为它们是**文字**。

这是 Day 4 那个坑的第 N 次出现 😄

```python runnable 转成数字再算
with open("成绩.csv", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

parts = lines[1].split(",")
chinese = int(parts[1])
math = int(parts[2])
print(chinese + math)
```

---

## 📌 知识卡 4 · 变成字典列表就好用了 ⭐

一堆 `parts[1]`、`parts[2]` 太难读。转成 Day 31 那种「列表套字典」：

```python runnable CSV -> 列表套字典
def read_csv(filename):
    """把 CSV 读成列表套字典。数字字段自动转成 int。"""
    with open(filename, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        parts = line.split(",")
        row = {}
        for key, value in zip(header, parts):
            if value.isdigit():
                row[key] = int(value)
            else:
                row[key] = value
        rows.append(row)
    return rows


students = read_csv("成绩.csv")
print(students[0])
print(students[0]["语文"] + students[0]["数学"])
```

`zip(header, parts)` 把**表头和这一行的值配成对**（Day 33 学的）—— 非常顺手。

**一旦变成列表套字典，Day 23~34 学的全部本事立刻能用**：
排序、筛选、统计、`key=lambda`……

---

## 📌 知识卡 5 · 写 CSV

```python runnable 列表套字典 -> CSV
def write_csv(filename, rows, header):
    """把列表套字典写成 CSV。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for row in rows:
            values = []
            for key in header:
                values.append(str(row[key]))
            f.write(",".join(values) + "\n")


data = [
    {"姓名": "星野樱", "总分": 259},
    {"姓名": "月见琉璃", "总分": 264},
]
write_csv("总分.csv", data, ["姓名", "总分"])

with open("总分.csv", encoding="utf-8") as f:
    print(f.read())
```

两个要点：

- **先写表头**，再写数据
- 每个值都要 `str(...)` —— `join` 只能拼字符串（Day 28 的坑）

---

## 📌 知识卡 6 · CSV 的一个真实麻烦

```python runnable 内容里有逗号就完蛋
line = "星野樱,88,\"她说：你好，再见\",79"
print(line.split(","))
```

备注里的逗号把字段拆散了。真实的 CSV 用引号包住这种字段，
解析规则比想象中复杂。

Python 有内置的 `csv` 模块专门处理这些：

```python runnable 标准库版（了解一下）
import csv

with open("成绩.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(dict(row))
```

`csv.DictReader` 自动把表头变成键 —— **一行搞定我们上面写的一整个函数**。

> 💡 今天要求你**手写解析**，因为亲手拆一遍才明白 CSV 到底是什么。
> 但真实项目里，直接用 `csv` 模块。

---

## 🛠 今天的任务 · 成绩单处理

| 函数 | 说明 |
|---|---|
| `write_lines_csv(filename, rows)` | 把若干行字符串写成 CSV 文件 |
| `read_csv(filename)` | 读成**列表套字典**，纯数字的字段转成 `int` |
| `add_total(rows)` | 给每行加一个 `总分` 字段（三科之和） |
| `subject_avg(rows, subject)` | 某一科的平均分，保留 1 位小数 |
| `top_student(rows)` | 总分最高的那一行（字典），空表返回 `None` |
| `sort_by_total(rows)` | 按总分从高到低排序，返回**新列表** |
| `write_csv(filename, rows, header)` | 把列表套字典写回 CSV |

主流程要求：

- 先造出 `成绩.csv`（至少 5 名学生、三科）
- 读进来，加总分
- 打印三科各自的平均分
- 打印总分第一名
- 按总分排序，带名次显示全部
- 把排序结果写成 `排名.csv`，**再读回来**验证
- 问玩家一个学生名字，查他的各科成绩，查不到要提示

> 💡 CSV 里读出来的数字**必须转 `int`**，不然排序会按文字排 ——
> "9" 会排在 "10" 前面。
