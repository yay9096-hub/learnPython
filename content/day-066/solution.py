# Day 66 · 日志分析器
import re

LOG = """
2026-09-01 Day 1 用了 42 分钟，联系 sakura@example.com
2026-09-02 Day 2 用了 35 分钟，参考了 https://docs.python.org/zh-cn/3/
2026-09-03 Day 3 用了 58 分钟，问了老师 13812345678
2026-09-04 Day 11 用了 40 分钟，笔记在 http://note.example.cn/py
2026-09-05 Day 12 用了 45 分钟，同学 ruri@test.org 也在学
"""


def find_dates(text):
    """找出所有 YYYY-MM-DD 格式的日期。"""
    return re.findall(r"\d{4}-\d{2}-\d{2}", text)


def find_numbers(text):
    """找出所有整数，返回数字列表。"""
    return [int(n) for n in re.findall(r"\d+", text)]


def find_emails(text):
    """找出所有邮箱地址。"""
    return re.findall(r"[\w.]+@[\w.]+\w", text)


def find_urls(text):
    """找出所有网址，http 和 https 都要。"""
    return re.findall(r"https?://[\w./\-]+", text)


def find_day_minutes(text):
    """找出所有「Day N 用了 M 分钟」，返回 [(N, M), ...] 的数字元组。"""
    pairs = re.findall(r"Day (\d+) 用了 (\d+) 分钟", text)
    return [(int(d), int(m)) for d, m in pairs]


def mask_phones(text):
    """把 11 位手机号的中间四位换成 ****。"""
    return re.sub(r"(\d{3})\d{4}(\d{4})", r"\1****\2", text)


def count_chinese(text):
    """数出中文字符总数。"""
    return len(re.findall(r"[\u4e00-\u9fa5]", text))


# ---------- 主流程 ----------
print("🔍 === 日志分析器 === 🔍")

dates = find_dates(LOG)
print(f"\n日期（{len(dates)} 个）：{dates}")

numbers = find_numbers(LOG)
print(f"数字（{len(numbers)} 个）：前五个 {numbers[:5]}")

emails = find_emails(LOG)
print(f"邮箱（{len(emails)} 个）：{emails}")

urls = find_urls(LOG)
print(f"网址（{len(urls)} 个）：{urls}")

print(f"中文字符：{count_chinese(LOG)} 个")

print("\n--- 学习时长 ---")
pairs = find_day_minutes(LOG)
total = 0
for day, minutes in pairs:
    print(f"  Day {day}：{minutes} 分钟")
    total += minutes

avg = round(total / len(pairs), 1) if pairs else 0
print(f"  总时长 {total} 分钟，平均 {avg} 分钟")

print("\n--- 打码之后 ---")
print(mask_phones(LOG))

first = re.search(r"\d{4}-\d{2}-\d{2}", LOG)
if first:
    print(f"日志从 {first.group(0)} 开始")
else:
    print("日志里没有日期")
