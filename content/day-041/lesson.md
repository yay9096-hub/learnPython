# Day 41 · 队伍管理函数库 🧰

> 「还记得 Day 31 吗？那一天你写了 60 多行，
> 显示、统计、排序、筛选、查询全挤在一起，改哪都提心吊胆。
>
> 今天把它拆成一套**函数库** —— 每个函数只做一件事，
> 然后像搭积木一样组合起来。」

---

## 📌 知识卡 1 · 一个函数只做一件事 ⭐

这是今天最重要的原则，叫**单一职责**。

看一个反面例子：

```python runnable 什么都干的函数（不好）
def do_everything(team):
    total = 0
    for m in team:
        print(f"{m['name']} HP {m['hp']}")
        total += m["hp"]
    print(f"总血量 {total}")
    return total

team = [{"name": "樱", "hp": 340}, {"name": "琉璃", "hp": 280}]
do_everything(team)
```

它又打印又统计。问题来了：
**我只想要总血量、不想打印**，怎么办？做不到。

拆开就灵活了：

```python runnable 拆成两个（好）
def total_hp(team):
    """只负责算，不打印。"""
    total = 0
    for m in team:
        total += m["hp"]
    return total

def show_team(team):
    """只负责打印，不算。"""
    for m in team:
        print(f"  {m['name']} HP {m['hp']}")

team = [{"name": "樱", "hp": 340}, {"name": "琉璃", "hp": 280}]

show_team(team)
print(f"总血量 {total_hp(team)}")

print(f"只要数字：{total_hp(team)}")
```

> 🧠 一条实用的判断标准：
> **函数名里如果出现「和」「并且」，多半就该拆了。**
> `show_and_count()` → 拆成 `show()` 和 `count()`。

---

## 📌 知识卡 2 · 筛选函数的固定套路

```python runnable 筛选：建空的 → 遍历 → 符合就装 → 交回去
def filter_by_element(team, element):
    """挑出指定属性的成员，返回一个新列表。"""
    result = []
    for m in team:
        if m["element"] == element:
            result.append(m)
    return result

team = [
    {"name": "樱", "element": "火"},
    {"name": "琉璃", "element": "水"},
    {"name": "幽香", "element": "火"},
]

fire = filter_by_element(team, "火")
print(len(fire))
for m in fire:
    print(f"  {m['name']}")
```

**四步固定不变**：建空列表 → 遍历 → 判断 → `return`。

以后所有「挑出符合条件的」都是这个形状，换的只是 `if` 里的条件。

⚠️ 注意它**返回新列表**，不改原队伍 —— 这样原数据永远安全。

---

## 📌 知识卡 3 · 让筛选条件更灵活

```python runnable 按数值门槛筛
def filter_by_atk(team, min_atk):
    """挑出攻击力达到 min_atk 的成员。"""
    result = []
    for m in team:
        if m["atk"] >= min_atk:
            result.append(m)
    return result

team = [
    {"name": "樱", "atk": 88},
    {"name": "琉璃", "atk": 95},
    {"name": "灯", "atk": 72},
]

print(len(filter_by_atk(team, 80)))
print(len(filter_by_atk(team, 90)))
print(len(filter_by_atk(team, 200)))
```

筛完还能**接着筛** —— 因为返回的还是列表：

```python runnable 筛选可以串起来
def filter_by_atk(team, min_atk):
    return [m for m in team if m["atk"] >= min_atk]

def filter_by_element(team, element):
    return [m for m in team if m["element"] == element]

team = [
    {"name": "樱", "atk": 88, "element": "火"},
    {"name": "幽香", "atk": 90, "element": "火"},
    {"name": "琉璃", "atk": 95, "element": "水"},
]

strong_fire = filter_by_element(filter_by_atk(team, 85), "火")
for m in strong_fire:
    print(m["name"])
```

> 💡 `[m for m in team if 条件]` 是**列表推导式** —— 用一行代替四行。
> 今天不要求你用，但看到别慌，它跟上面的四步循环完全等价。

---

## 📌 知识卡 4 · 查找函数：找不到怎么办

```python runnable 找到返回，找不到返回 None
def find_member(team, name):
    """按名字找人。找不到返回 None。"""
    for m in team:
        if m["name"] == name:
            return m
    return None

team = [{"name": "樱", "hp": 340}]

found = find_member(team, "樱")
print(found)

missing = find_member(team, "路人甲")
print(missing)

if missing is None:
    print("查无此人")
```

两个要点：

1. **找到就立刻 `return`** —— 不用等循环跑完（Day 37 的提前返回）
2. **找不到返回 `None`**，让调用方自己决定怎么处理

⚠️ 判断要用 `is None`，不要用 `== None`（Python 的习惯写法）。

---

## 📌 知识卡 5 · 大函数调用小函数

```python runnable 组装成报告
def total_hp(team):
    """算总血量。"""
    return sum(m["hp"] for m in team)

def strongest(team):
    """找出攻击力最高的成员，空队返回 None。"""
    if not team:
        return None
    best = team[0]
    for m in team:
        if m["atk"] > best["atk"]:
            best = m
    return best

def show_report(team):
    """把上面几个零件拼成一份报告。"""
    print(f"  人数：{len(team)}")
    print(f"  总血量：{total_hp(team)}")
    top = strongest(team)
    if top is not None:
        print(f"  最强：{top['name']}（{top['atk']}）")

team = [
    {"name": "樱", "hp": 340, "atk": 88},
    {"name": "琉璃", "hp": 280, "atk": 95},
]
show_report(team)
show_report([])
```

`show_report` 自己几乎没干活，全在**调度别的函数** ——
这正是「拆分问题」想达到的效果。

⚠️ 注意 `strongest` 对**空队伍**做了保护。函数库要经得起各种输入。

---

## 🛠 今天的任务 · 队伍管理函数库

写一套至少 7 个函数的库，然后组装成一个查询系统：

| 函数 | 返回 | 说明 |
|---|---|---|
| `total_hp(team)` | 数字 | 总血量，空队返回 0 |
| `avg_atk(team)` | 数字 | 平均攻击，**空队返回 0**（别除以零） |
| `strongest(team)` | 字典 / None | 攻击力最高的，空队返回 None |
| `filter_by_element(team, element)` | 列表 | 按属性筛 |
| `filter_by_atk(team, min_atk)` | 列表 | 攻击力达标的 |
| `find_member(team, name)` | 字典 / None | 按名字找 |
| `show_team(team)` | 无 | 只负责打印 |
| `show_report(team)` | 无 | 调用上面的函数拼一份报告 |

主流程要求：

- 打印全队 + 报告
- 按属性筛一次并打印结果
- 按攻击力筛一次并打印结果
- 问玩家一个名字，用 `find_member` 查，查不到提示「查无此人」
- **用空列表 `[]` 调用一次 `show_report`**，验证不会崩

> ⚠️ 算的函数（`total_hp` / `avg_atk` / `strongest` / 三个筛选查找）
> **一个 `print` 都不要写**。打印只在 `show_team` / `show_report` 里做。
