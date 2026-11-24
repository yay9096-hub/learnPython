## 提示 1 · read_csv 是今天的地基

```python
def read_csv(filename):
    """把 CSV 读成列表套字典。纯数字的字段自动转成 int。"""
    with open(filename, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) == 0:
        return []

    header = lines[0].split(",")          # 第一行是表头
    rows = []
    for line in lines[1:]:                # 从第二行开始才是数据
        parts = line.split(",")
        row = {}
        for key, value in zip(header, parts):
            value = value.strip()
            if value.isdigit():
                row[key] = int(value)     # ← 关键：数字要转
            else:
                row[key] = value
        rows.append(row)
    return rows
```

三个关键点：

- `lines[0]` 表头、`lines[1:]` 数据（Day 26 的切片）
- `zip(header, parts)` 把表头和值配成对（Day 33）
- **`isdigit()` 判断后 `int()` 转换** —— 不转的话排序会按文字排，
  「9」会排在「10」前面

一旦变成列表套字典，Day 23~34 的全部本事就都能用了。

## 提示 2 · 统计和排序都是老朋友

```python
SUBJECTS = ["语文", "数学", "英语"]


def add_total(rows):
    """给每一行加一个「总分」字段。"""
    for row in rows:
        total = 0
        for s in SUBJECTS:
            total += row[s]
        row["总分"] = total
    return rows


def subject_avg(rows, subject):
    """某一科的平均分。空表返回 0。"""
    if len(rows) == 0:
        return 0
    total = 0
    for row in rows:
        total += row[subject]
    return round(total / len(rows), 1)


def sort_by_total(rows):
    """按总分从高到低排序，返回新列表。"""
    return sorted(rows, key=lambda r: r["总分"], reverse=True)
```

⚠️ 用 `sorted(...)` **返回新列表**，别用 `rows.sort()` 改原数据 ——
判题会检查原列表有没有被弄乱。

## 提示 3 · 写 CSV：表头 + 每行 join

```python
def write_csv(filename, rows, header):
    """把列表套字典写回 CSV。先写表头，值都转成文字。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for row in rows:
            values = []
            for key in header:
                values.append(str(row[key]))     # ← join 只能拼字符串
            f.write(",".join(values) + "\n")
```

两个坑：

- **必须先写表头**，否则读回来第一条数据会被当成表头
- 每个值要 `str(...)` —— 数字直接 join 会报 TypeError（Day 28 的老坑）

主流程最后要**读回来验证**：

```python
write_csv(RANKING, ranked, ["姓名", "语文", "数学", "英语", "总分"])
check = read_csv(RANKING)
print(f"读回来 {len(check)} 行，第一名还是 {check[0]['姓名']} ✓")
```

自己写出去、自己能读回来 —— 这才算真的搞定了 CSV ✨
