## 提示 1 · 先写一个共用的小工具

三个算法都要用到「去重 + 转成日期 + 排序」，先抽出来：

```python
def _sorted_days(records):
    """把记录里的日期去重、转成 date、排好序。"""
    texts = set()
    for r in records:
        texts.add(r["date"])
    return sorted(date.fromisoformat(t) for t in texts)
```

三步缺一不可：

- **`set()` 去重** —— 一天打两次卡只能算一天
- **`date.fromisoformat()`** —— 变成真正的日期才能相减
- **`sorted()`** —— 不排序算出来是乱的

打卡不重复也很简单：

```python
def check_in(records, day_text, minutes, topic):
    """打一次卡。同一天已经打过就不重复加。"""
    for r in records:
        if r["date"] == day_text:
            return records
    records.append({"date": day_text, "minutes": minutes, "topic": topic})
    return records
```

## 提示 2 · 最长连续：看相邻两天差几天

```python
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
```

三个细节：

- 循环**从 1 开始** —— 因为要和前一个比
- `(a - b).days` 拿到相差的天数
- 差 1 才叫连续，否则 `current` 归 1 重新数
- **空列表要先挡住**，否则 `longest = 1` 就错了

## 提示 3 · 当前连击：从今天往回走

```python
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
```

⚠️ **今天没打卡就是 0** —— 这是「当前连击」和「最长连续」最大的区别。

显示时按日期排序（日期是 `YYYY-MM-DD` 格式，直接按文字排就对）：

```python
def show_records(records):
    if len(records) == 0:
        print("  📭 还没有打卡记录")
        return
    ordered = sorted(records, key=lambda r: r["date"])
    for r in ordered:
        print(f"  {r['date']}  {r['minutes']} 分钟  · {r['topic']}")
```

> 💡 这就是首页那个「🔥 连续 N 天」背后的算法。
