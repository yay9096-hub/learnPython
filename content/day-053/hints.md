## 提示 1 · 今天唯一的新招：用字典分组累加

按月和按分类，用的是**同一个套路**：

```python
def group_by_month(records):
    """按月统计支出。返回 {月份: 该月支出总额}。"""
    result = {}
    for r in records:
        if r["type"] != "支出":     # ← 只统计支出
            continue
        month = r["date"][:7]        # ← 前 7 个字符就是 "2026-09"
        if month in result:
            result[month] = round(result[month] + r["amount"], 2)
        else:
            result[month] = r["amount"]
    return result
```

三个关键点：

- **`continue` 跳过收入** —— 判题专门检查「零花钱」有没有混进支出统计
- **`r["date"][:7]`** 切出月份（Day 26 的切片）
- **「有就加、没有就设」** —— Day 50 加道具时用过同一招

按分类只要把 `month` 换成 `r["category"]`，其余一模一样。

## 提示 2 · 校验函数只 raise

```python
def validate_amount(text):
    """把文字转成金额。只 raise，不 try。"""
    try:
        amount = float(text)
    except ValueError:
        raise ValueError(f"金额得是数字，你输入的是「{text}」")
    if amount <= 0:
        raise ValueError(f"金额必须大于 0（收到的是 {amount}）")
    return round(amount, 2)
```

⚠️ 这里的 `try` 是**为了把 `float()` 的错误换成一句人话**，
换完立刻 `raise` 出去 —— 不是把错吞掉。

分类校验记得列出可选值（判题会检查错误信息里有没有）：

```python
def validate_category(cat):
    if cat not in CATEGORIES:
        options = " / ".join(CATEGORIES)
        raise ValueError(f"不认识的分类「{cat}」，只能是：{options}")
    return cat
```

## 提示 3 · 主流程用 try 接住

```python
cat_text = input("分类（零食/文具/交通/娱乐/零花钱）：").strip()
amount_text = input("金额：").strip()
note = input("备注：").strip()

try:
    category = validate_category(cat_text)
    amount = validate_amount(amount_text)
    add_record(book, "2026-09-08", "支出", category, amount, note)
    print(f"  ✓ 记好了：{category} {amount} 元")
except ValueError as e:
    print(f"  ✗ 记不了：{e}")
```

**里层 raise、外层 try** —— 这就是 Day 46 建立的分工。

报表里标出花钱最多的分类：

```python
groups = group_by_category(records)
top = top_category(records)
for cat in sorted(groups, key=lambda c: groups[c], reverse=True):
    mark = "  ← 花得最多" if cat == top else ""
    print(f"    {cat}：{groups[cat]} 元{mark}")
```

⚠️ 所有金额显示都要 `round(x, 2)` —— 浮点数会有 `0.1 + 0.2 = 0.30000000000000004`
这种意外。
