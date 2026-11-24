# Day 51 · 学习打卡系统
import json
from datetime import date

RECORDS = "打卡记录.json"
TODAY = "2026-09-06"


def load_records(filename):
    """读打卡记录。文件还不存在就返回空列表。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_records(filename, records):
    """把记录存成 json。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def check_in(records, day_text, minutes, topic):
    """打一次卡。同一天已经打过就不重复加。"""
    for r in records:
        if r["date"] == day_text:
            return records
    records.append({"date": day_text, "minutes": minutes, "topic": topic})
    return records


def total_minutes(records):
    """总共学了多少分钟。"""
    total = 0
    for r in records:
        total += r["minutes"]
    return total


def _sorted_days(records):
    """把记录里的日期去重、转成 date、排好序。"""
    texts = set()
    for r in records:
        texts.add(r["date"])
    return sorted(date.fromisoformat(t) for t in texts)


def longest_streak(records):
    """最长连续打卡天数。没有记录返回 0。"""
    days = _sorted_days(records)
    if len(days) == 0:
        return 0

    longest = 1
    current = 1
    for i in range(1, len(days)):
        if (days[i] - days[i - 1]).days == 1:
            current = current + 1
        else:
            current = 1
        if current > longest:
            longest = current
    return longest


def current_streak(records, today_text):
    """从今天往回数，连续打了几天。今天没打卡返回 0。"""
    days = _sorted_days(records)
    today = date.fromisoformat(today_text)
    if today not in days:
        return 0

    streak = 1
    i = days.index(today)
    while i > 0 and (days[i] - days[i - 1]).days == 1:
        streak = streak + 1
        i = i - 1
    return streak


def show_records(records):
    """按日期排序显示全部打卡。"""
    if len(records) == 0:
        print("  📭 还没有打卡记录")
        return
    ordered = sorted(records, key=lambda r: r["date"])
    for r in ordered:
        print(f"  {r['date']}  {r['minutes']} 分钟  · {r['topic']}")


# ---------- 主流程 ----------
print("⏰ === 学习打卡系统 === ⏰")

records = load_records(RECORDS)
print(f"\n读到 {len(records)} 条历史记录")

check_in(records, "2026-09-01", 40, "文件读写")
check_in(records, "2026-09-02", 35, "json 存档")
check_in(records, "2026-09-04", 50, "datetime")
check_in(records, "2026-09-05", 45, "连续打卡算法")
check_in(records, "2026-09-06", 40, "复习")

before = len(records)
check_in(records, "2026-09-06", 999, "重复打卡测试")
print(f"重复打卡前 {before} 条，之后 {len(records)} 条 —— 没有重复 ✓")

print(f"\n总学习时长：{total_minutes(records)} 分钟")
print(f"最长连续：{longest_streak(records)} 天")
print(f"当前连击：{current_streak(records, TODAY)} 天")

print("\n--- 全部记录 ---")
show_records(records)

minutes_text = input("\n今天又学了多少分钟？").strip()
try:
    minutes = int(minutes_text)
except ValueError:
    minutes = 0

check_in(records, "2026-09-07", minutes, "今日份")
save_records(RECORDS, records)

reloaded = load_records(RECORDS)
print(f"\n存盘后重新读回 {len(reloaded)} 条")
print(f"当前连击变成了 {current_streak(reloaded, '2026-09-07')} 天 🔥")
