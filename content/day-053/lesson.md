# Day 53 · 记账本 💰

> 「今天不学新语法。
> 把 Day 45~52 学的全部东西 —— 异常、文件、json、日期、统计 ——
> 拧成一个**你真的能拿去用**的程序。
>
> 这个记账本可以记你的零花钱，是真的能用的那种。」

---

## 🔍 第五章到目前为止的武器

| 天 | 学到的 | 今天用在哪 |
|---|---|---|
| D45 | `try` / `except` | 输入金额乱打也不崩 |
| D46 | `raise` | 金额是负数、分类不认识就报错 |
| D47 | 写文件 | — |
| D48 | 读文件 | — |
| D49 | 文件不存在 | 第一次打开账本 |
| D50 | `json` | 整个账本存盘读盘 |
| D51 | `datetime` | 每笔账带日期、按月统计 |
| D52 | CSV | 导出成 Excel 能打开的表 |

**八天的东西，今天一次用完。**

---

## 🧩 复习卡 · 三个最容易忘的

### 1. json 存日期要先转成文字

```python runnable 日期不能直接存
import json
from datetime import date

record = {"date": date.today().isoformat(), "amount": 25.5}
print(json.dumps(record, ensure_ascii=False))
```

### 2. 读文件前先想「不存在怎么办」

```python runnable 第一次打开的标准姿势
import json

def load(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

print(load("还没有的账本.json"))
```

### 3. 钱要用小数，而且要注意精度

```python runnable 浮点数的经典意外
print(0.1 + 0.2)
print(round(0.1 + 0.2, 2))
```

计算机存小数有精度误差，**涉及钱的地方一律 `round(x, 2)` 再显示**。

---

## 📌 知识卡 · 按月分组的套路 ⭐

这是今天唯一的新技巧。日期是 `2026-09-02`，**前 7 个字符就是月份**：

```python runnable 切片取月份
records = [
    {"date": "2026-08-15", "amount": 30},
    {"date": "2026-09-02", "amount": 25},
    {"date": "2026-09-10", "amount": 40},
]

by_month = {}
for r in records:
    month = r["date"][:7]
    if month in by_month:
        by_month[month] = by_month[month] + r["amount"]
    else:
        by_month[month] = r["amount"]

for month, total in by_month.items():
    print(f"{month}：{total} 元")
```

`r["date"][:7]` 拿到 `"2026-09"`（Day 26 的切片）。

**「用字典分组累加」这个套路**，以后统计任何东西都用得上：
按月、按分类、按人、按标签 —— 全是这一招。

---

## 🎯 今天的作品 · 我的记账本

### 数据结构

每笔账是一个字典：

```python
{"date": "2026-09-02", "type": "支出", "category": "零食", "amount": 12.5, "note": "奶茶"}
```

### 必须有的函数

| 函数 | 说明 |
|---|---|
| `load_book(filename)` | 读账本。文件不存在或损坏都返回 `[]` |
| `save_book(filename, records)` | 存成 json |
| `validate_amount(text)` | 把文字转成金额。**不是数字或 ≤0 就 `raise ValueError`** |
| `validate_category(cat)` | 分类必须在预设列表里，否则 `raise ValueError` |
| `add_record(records, day, kind, category, amount, note)` | 加一笔，返回 records |
| `total_by_kind(records, kind)` | 某一类（收入/支出）的总额 |
| `balance(records)` | 结余 = 总收入 − 总支出 |
| `group_by_month(records)` | 返回 `{月份: 该月支出总额}` |
| `group_by_category(records)` | 返回 `{分类: 总额}`，只统计支出 |
| `top_category(records)` | 花钱最多的分类，没有记录返回 `None` |
| `show_report(records)` | 打印完整报表 |
| `export_csv(filename, records)` | 导出成 CSV |

### 主流程要求

- 开局 `load_book`（文件不存在）
- 补录至少 **6 笔**账，跨**两个月**，包含收入和支出，分类至少 3 种
- 打印总收入、总支出、结余
- 按月统计并显示
- 按分类统计并显示，标出花得最多的分类
- 问玩家记一笔（分类 + 金额 + 备注），用 `try` 接住非法输入
- 存盘，再读回来验证
- 导出 `账本.csv`

### 硬性要求

- 两个 `validate_` 函数只 `raise`，不 `try`（Day 46 的分工）
- 所有金额显示都 `round(x, 2)`
- 全程不能崩

> 💡 做完之后去「📁 文件」里点开 `账本.json` 和 `账本.csv` ——
> **那是两个你真的可以拿去用的文件。**
