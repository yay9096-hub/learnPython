# Day 53 · 我的记账本
import json

BOOK = "账本.json"
CSV = "账本.csv"
CATEGORIES = ["零食", "文具", "交通", "娱乐", "零花钱"]


def load_book(filename):
    """读账本。文件不存在或格式损坏都返回空列表。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_book(filename, records):
    """把账本存成 json。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def validate_amount(text):
    """把文字转成金额。只 raise，不 try。"""
    try:
        amount = float(text)
    except ValueError:
        raise ValueError(f"金额得是数字，你输入的是「{text}」")
    if amount <= 0:
        raise ValueError(f"金额必须大于 0（收到的是 {amount}）")
    return round(amount, 2)


def validate_category(cat):
    """检查分类。不认识就抛错，信息里列出可选值。"""
    if cat not in CATEGORIES:
        options = " / ".join(CATEGORIES)
        raise ValueError(f"不认识的分类「{cat}」，只能是：{options}")
    return cat


def add_record(records, day, kind, category, amount, note):
    """记一笔账。"""
    records.append({
        "date": day,
        "type": kind,
        "category": category,
        "amount": round(amount, 2),
        "note": note,
    })
    return records


def total_by_kind(records, kind):
    """某一类（收入 / 支出）的总额。"""
    total = 0
    for r in records:
        if r["type"] == kind:
            total += r["amount"]
    return round(total, 2)


def balance(records):
    """结余 = 总收入 - 总支出。"""
    return round(total_by_kind(records, "收入") - total_by_kind(records, "支出"), 2)


def group_by_month(records):
    """按月统计支出。返回 {月份: 该月支出总额}。"""
    result = {}
    for r in records:
        if r["type"] != "支出":
            continue
        month = r["date"][:7]
        if month in result:
            result[month] = round(result[month] + r["amount"], 2)
        else:
            result[month] = r["amount"]
    return result


def group_by_category(records):
    """按分类统计支出。返回 {分类: 总额}。"""
    result = {}
    for r in records:
        if r["type"] != "支出":
            continue
        cat = r["category"]
        if cat in result:
            result[cat] = round(result[cat] + r["amount"], 2)
        else:
            result[cat] = r["amount"]
    return result


def top_category(records):
    """花钱最多的分类。没有支出记录返回 None。"""
    groups = group_by_category(records)
    if len(groups) == 0:
        return None
    best = None
    best_amount = -1
    for cat, amount in groups.items():
        if amount > best_amount:
            best_amount = amount
            best = cat
    return best


def show_report(records):
    """打印完整报表。"""
    print(f"  收入：{total_by_kind(records, '收入')} 元")
    print(f"  支出：{total_by_kind(records, '支出')} 元")
    print(f"  结余：{balance(records)} 元")

    print("\n  按月支出：")
    months = group_by_month(records)
    for month in sorted(months):
        print(f"    {month}：{months[month]} 元")

    print("\n  按分类支出：")
    groups = group_by_category(records)
    top = top_category(records)
    for cat in sorted(groups, key=lambda c: groups[c], reverse=True):
        mark = "  ← 花得最多" if cat == top else ""
        print(f"    {cat}：{groups[cat]} 元{mark}")


def export_csv(filename, records):
    """把账本导出成 CSV。"""
    header = ["date", "type", "category", "amount", "note"]
    with open(filename, "w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for r in records:
            values = []
            for key in header:
                values.append(str(r[key]))
            f.write(",".join(values) + "\n")


# ---------- 主流程 ----------
print("💰 === 我的记账本 === 💰")

book = load_book(BOOK)
print(f"\n读到 {len(book)} 条历史记录")

add_record(book, "2026-08-05", "收入", "零花钱", 100, "月初零花钱")
add_record(book, "2026-08-12", "支出", "零食", 12.5, "奶茶")
add_record(book, "2026-08-20", "支出", "文具", 28, "笔记本和笔")
add_record(book, "2026-09-01", "收入", "零花钱", 100, "月初零花钱")
add_record(book, "2026-09-03", "支出", "零食", 8.5, "冰淇淋")
add_record(book, "2026-09-05", "支出", "娱乐", 45, "电影票")

print("\n--- 账本报表 ---")
show_report(book)

print("\n--- 记一笔新的 ---")
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

save_book(BOOK, book)
reloaded = load_book(BOOK)
print(f"\n存盘后读回 {len(reloaded)} 条，结余 {balance(reloaded)} 元")

export_csv(CSV, reloaded)
print(f"已导出 {CSV}，去「📁 文件」里看看 ✨")
