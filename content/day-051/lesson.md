# Day 51 · 学习打卡 ⏰

> 「你每天在这个网站上的连续打卡天数，是怎么算出来的？
>
> 今天你自己写一个。学完这一课，你就明白首页上那个
> 『🔥 连续 9 天』背后到底发生了什么。」

---

## 📌 知识卡 1 · 拿到今天和此刻

```python runnable 今天几号
from datetime import date, datetime

today = date.today()
now = datetime.now()

print(today)
print(now)
print(type(today))
```

| 类型 | 装什么 | 怎么拿 |
|---|---|---|
| `date` | 只有年月日 | `date.today()` |
| `datetime` | 年月日 + 时分秒 | `datetime.now()` |

```python runnable 拆开看每一部分
from datetime import datetime

now = datetime.now()
print(f"年：{now.year}")
print(f"月：{now.month}")
print(f"日：{now.day}")
print(f"时：{now.hour}")
print(f"分：{now.minute}")
```

---

## 📌 知识卡 2 · `strftime` —— 变成好看的文字 ⭐

```python runnable 各种格式
from datetime import datetime

now = datetime.now()

print(now.strftime("%Y-%m-%d"))
print(now.strftime("%Y年%m月%d日"))
print(now.strftime("%H:%M:%S"))
print(now.strftime("%Y-%m-%d %H:%M"))
```

常用的几个占位符：

| 符号 | 含义 | 例子 |
|---|---|---|
| `%Y` | 四位年 | 2026 |
| `%m` | 两位月 | 09 |
| `%d` | 两位日 | 02 |
| `%H` | 小时（24 制） | 14 |
| `%M` | 分钟 | 30 |
| `%S` | 秒 | 45 |

> 💡 记不住？记住 `"%Y-%m-%d"` 这一个就够用了 —— 它是国际标准格式，
> 而且**按这个格式排序，正好就是按时间排序**（因为年在前、位数固定）。

---

## 📌 知识卡 3 · 文字变回日期

```python runnable 存进文件的是文字，读回来要转回日期
from datetime import date

text = "2026-09-02"
d = date.fromisoformat(text)

print(d)
print(type(d))
print(d.year)
```

⚠️ `fromisoformat` 只认 `YYYY-MM-DD` 这一种格式。
别的格式要用 `datetime.strptime(文本, 格式)`：

```python runnable strptime 认任意格式
from datetime import datetime

d = datetime.strptime("2026年09月02日", "%Y年%m月%d日")
print(d.date())
```

> 🧠 一对好记的名字：
> **`strftime` 是 format（日期 → 文字），`strptime` 是 parse（文字 → 日期）。**

---

## 📌 知识卡 4 · `timedelta` —— 日期加减 ⭐

```python runnable 算昨天和一周后
from datetime import date, timedelta

today = date.today()

print(f"今天：{today}")
print(f"昨天：{today - timedelta(days=1)}")
print(f"一周后：{today + timedelta(days=7)}")
print(f"30 天前：{today - timedelta(days=30)}")
```

两个日期**相减**得到的也是 `timedelta`：

```python runnable 算相隔多少天
from datetime import date

a = date(2026, 9, 2)
b = date(2026, 9, 10)

gap = b - a
print(gap)
print(gap.days)
print(type(gap))
```

`.days` 拿到天数 —— **这是算连续打卡的关键**。

---

## 📌 知识卡 5 · 算连续打卡 ⭐

思路：把打卡日期排好序，看**相邻两天是不是差 1 天**。

```python runnable 连续打卡算法
from datetime import date

records = ["2026-08-28", "2026-08-30", "2026-08-31",
           "2026-09-01", "2026-09-02"]

days = sorted(date.fromisoformat(t) for t in set(records))
print(days)

longest = 1
current = 1
for i in range(1, len(days)):
    gap = (days[i] - days[i - 1]).days
    if gap == 1:
        current = current + 1
    else:
        current = 1
    if current > longest:
        longest = current

print(f"最长连续：{longest} 天")
```

三个要点：

1. **`set(records)`** 先去重 —— 一天打两次卡只能算一天（Day 32 的集合）
2. **`sorted(...)`** 排序 —— 不排序算出来是乱的（Day 27）
3. **`gap == 1`** 才叫连续；差 2 天以上就断了，`current` 归 1

⚠️ 空列表时 `len(days)` 是 0，`longest = 1` 就错了。真实代码要先判断。

---

## 📌 知识卡 6 · 存进文件的日期

日期不能直接存进 json（Day 50 的坑），要先转成文字：

```python runnable 日期存 json 的正确姿势
import json
from datetime import date

record = {
    "date": date.today().isoformat(),
    "minutes": 40,
    "topic": "datetime",
}

with open("打卡.json", "w", encoding="utf-8") as f:
    json.dump([record], f, ensure_ascii=False, indent=2)

with open("打卡.json", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded)
d = date.fromisoformat(loaded[0]["date"])
print(f"读回来还是日期：{d.year} 年")
```

`.isoformat()` 是 `strftime("%Y-%m-%d")` 的快捷写法，**存日期就用它**。

---

## 🛠 今天的任务 · 学习打卡系统

| 函数 | 说明 |
|---|---|
| `load_records(filename)` | 读打卡记录（json 列表）。文件不存在返回 `[]` |
| `save_records(filename, records)` | 存回 json |
| `check_in(records, day_text, minutes, topic)` | 加一条打卡。**同一天不能重复打卡**，已有就返回原列表 |
| `total_minutes(records)` | 总学习分钟数 |
| `longest_streak(records)` | 最长连续天数。**空记录返回 0** |
| `current_streak(records, today_text)` | 当前连击：从 today 往回数连续了几天；今天没打卡返回 0 |
| `show_records(records)` | 按日期排序显示全部，带日期和时长 |

主流程要求：

- 先 `load_records`（文件不存在）
- 用 `check_in` 补录至少 5 天的记录，其中要**故意断开一天**
- 试着给同一天打两次卡，验证不会重复
- 打印总时长、最长连击、当前连击
- 用 `show_records` 显示全部
- 问玩家今天学了多少分钟，打卡并存盘
- 再读回来验证

> 💡 判题会用固定日期，不依赖真实的「今天」，放心写。
