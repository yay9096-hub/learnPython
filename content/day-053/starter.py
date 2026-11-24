# Day 53 · 我的记账本
import json

BOOK = "账本.json"
CSV = "账本.csv"
CATEGORIES = ["零食", "文具", "交通", "娱乐", "零花钱"]


# TODO 1: load_book(filename) -> 列表。不存在或损坏都返回 []


# TODO 2: save_book(filename, records) -> 存成 json


# TODO 3: validate_amount(text) -> float
#   转不了 -> raise ValueError；<=0 -> raise ValueError
#   ⚠️ 只 raise，不要 try


# TODO 4: validate_category(cat) -> str
#   不在 CATEGORIES 里 -> raise ValueError（信息里列出可选值）


# TODO 5: add_record(records, day, kind, category, amount, note) -> records
#   每笔形如 {"date","type","category","amount","note"}


# TODO 6: total_by_kind(records, kind) -> 某一类的总额


# TODO 7: balance(records) -> 收入 - 支出


# TODO 8: group_by_month(records) -> {月份: 该月支出总额}
#   月份 = r["date"][:7]


# TODO 9: group_by_category(records) -> {分类: 总额}，只算支出


# TODO 10: top_category(records) -> 花钱最多的分类，没记录返回 None


# TODO 11: show_report(records) -> 打印完整报表


# TODO 12: export_csv(filename, records) -> 导出 CSV


# ---------- 主流程 ----------
# TODO 13: load_book（文件不存在）
# TODO 14: 补录至少 6 笔，跨两个月，含收入和支出，至少 3 种分类
# TODO 15: 打印收入/支出/结余、按月统计、按分类统计
# TODO 16: 问玩家记一笔，用 try 接住非法输入
# TODO 17: 存盘 + 读回来验证 + 导出 CSV
