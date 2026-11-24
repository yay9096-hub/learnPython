## 提示 1 · 先把「算」和「打印」分开

今天的核心原则：**一个函数只做一件事**。

算的函数长这样（注意：没有 print）：

```python
def total_hp(team):
    """返回队伍总血量。空队伍返回 0。"""
    total = 0
    for m in team:
        total += m["hp"]
    return total
```

空队伍会自然返回 0（循环一次都不跑），不用特意处理。

但平均值**必须**处理空队伍 —— 否则除以零直接崩：

```python
def avg_atk(team):
    """返回平均攻击力。空队伍返回 0，避免除以零。"""
    if len(team) == 0:
        return 0
    total = 0
    for m in team:
        total += m["atk"]
    return round(total / len(team), 1)
```

## 提示 2 · 筛选和查找的两个固定套路

**筛选**（要全部符合的）—— 建空列表，跑完再返回：

```python
def filter_by_element(team, element):
    """挑出指定属性的成员，返回新列表。"""
    result = []
    for m in team:
        if m["element"] == element:
            result.append(m)
    return result
```

**查找**（只要第一个）—— 找到就立刻返回：

```python
def find_member(team, name):
    """按名字找人。找不到返回 None。"""
    for m in team:
        if m["name"] == name:
            return m
    return None
```

⚠️ 两个区别：筛选**跑完全程**，查找**找到就跑路**。
最后那个 `return None` 要写在**循环外面**（跟 for 对齐）。

找最强的记得保护空队伍：

```python
def strongest(team):
    """返回攻击力最高的成员。空队伍返回 None。"""
    if len(team) == 0:
        return None
    best = team[0]
    for m in team:
        if m["atk"] > best["atk"]:
            best = m
    return best
```

## 提示 3 · 报告函数只做调度

```python
def show_report(team):
    """把各个统计零件拼成一份报告。"""
    print(f"  人数：{len(team)}")
    print(f"  总血量：{total_hp(team)}")
    print(f"  平均攻击：{avg_atk(team)}")
    top = strongest(team)
    if top is None:
        print("  最强：（队伍是空的）")
    else:
        print(f"  最强：{top['name']}（{top['atk']}）")
```

它自己几乎不干活，全在**调别的函数** —— 这正是拆分的意义。

主流程里筛选的结果可以直接喂给 `show_team`：

```python
print("\n--- 火属性成员 ---")
show_team(filter_by_element(TEAM, "火"))

print("\n--- 攻击力 90 以上 ---")
show_team(filter_by_atk(TEAM, 90))
```

一个函数的返回值直接当另一个函数的参数 —— **积木就是这么搭起来的**。

最后别忘了空队伍测试：

```python
print("\n--- 空队伍测试（不应该崩）---")
show_report([])
```
