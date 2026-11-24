# Day 31 · 队伍数据库 🗃

> 「Day 25 你用**三个平行列表**存队伍，排个序就对不上号了。
> Day 29 的字典能装一个角色，但装不下一整队。
>
> 今天把两个合起来：**一个列表，里面装着一堆字典**。
> 这是真实世界里最常见的数据形状 —— 你以后看到的 API、数据库、Excel，全长这样。」

---

## 📌 知识卡 1 · 列表套字典

```python runnable 一队人，每人一份档案
team = [
    {"name": "星野樱", "hp": 340, "atk": 88, "element": "火"},
    {"name": "月见琉璃", "hp": 280, "atk": 95, "element": "水"},
    {"name": "天野灯", "hp": 310, "atk": 72, "element": "风"},
]

print(len(team))
print(team[0])
```

拆开看这个结构：

- 最外面是**列表** `[ ]` → 所以能 `len()`、能 `team[0]`、能 `for`、能排序
- 里面每一项是**字典** `{ }` → 所以能 `["name"]`、能 `.items()`

---

## 📌 知识卡 2 · 逐层剥开

```python runnable 一层一层取
team = [
    {"name": "星野樱", "hp": 340},
    {"name": "月见琉璃", "hp": 280},
]

print(team[0])
print(team[0]["name"])
print(team[1]["hp"])
```

读法是**从左往右一层层剥**：

`team[0]["name"]`
→ `team[0]` 先拿到第一个字典
→ 再 `["name"]` 从这个字典里取名字

> 🧠 看到多层方括号别慌，**从左边开始，一次剥一层**，每剥一层就 `print` 一下看看是什么。

---

## 📌 知识卡 3 · 遍历：每一项都是字典 ⭐

```python runnable 遍历队伍
team = [
    {"name": "星野樱", "hp": 340, "atk": 88},
    {"name": "月见琉璃", "hp": 280, "atk": 95},
    {"name": "天野灯", "hp": 310, "atk": 72},
]

for member in team:
    print(f"{member['name']} · HP {member['hp']} · ATK {member['atk']}")
```

`member` 每一圈都是**一整个字典**，所以后面用 `member['name']` 取字段。

⚠️ f-string 里层记得用**单引号**，不然引号打架。

对比 Day 25 的平行列表版本 —— **再也不用担心对不上号了**，
因为一个人的所有数据本来就绑在一起。

---

## 📌 知识卡 4 · 统计和筛选

Day 25 那一套全能用，只是取值时多剥一层：

```python runnable 统计
team = [
    {"name": "星野樱", "hp": 340, "atk": 88},
    {"name": "月见琉璃", "hp": 280, "atk": 95},
    {"name": "天野灯", "hp": 310, "atk": 72},
]

total_hp = 0
for member in team:
    total_hp += member["hp"]

print(f"总血量：{total_hp}")
```

筛选出符合条件的，装进一个新列表：

```python runnable 筛选出高攻击的
team = [
    {"name": "星野樱", "atk": 88},
    {"name": "月见琉璃", "atk": 95},
    {"name": "天野灯", "atk": 72},
]

strong = []
for member in team:
    if member["atk"] >= 80:
        strong.append(member)

print(f"高攻击成员有 {len(strong)} 人：")
for m in strong:
    print(f"  {m['name']}（{m['atk']}）")
```

**「建空列表 → 遍历 → 符合条件才 append」** —— 这是筛选的固定套路。

---

## 📌 知识卡 5 · 按某个字段排序

Day 27 你要先手动打包成 `[战力, 名字]` 才能排。
现在有了字典，可以直接告诉 Python「**按哪个字段排**」：

```python runnable key= 指定按哪个字段排 ⭐
team = [
    {"name": "星野樱", "atk": 88},
    {"name": "月见琉璃", "atk": 95},
    {"name": "天野灯", "atk": 72},
]

team.sort(key=lambda m: m["atk"], reverse=True)

for m in team:
    print(f"{m['name']} —— {m['atk']}")
```

`key=lambda m: m["atk"]` 读作：「排序时，每一项 `m` 拿它的 `atk` 去比」。

> 💡 `lambda` 是一种「一次性的小函数」，第四章会正式讲。
> 今天你只要记住这个**固定句式**：
> `列表.sort(key=lambda 项: 项["字段名"], reverse=True)`
>
> 换个字段排就改字段名，别的都不用动。

---

## 📌 知识卡 6 · 新增和修改

```python runnable 增员和升级
team = [{"name": "星野樱", "hp": 340}]

team.append({"name": "水城凛", "hp": 250})      # 新成员
print(len(team))

team[0]["hp"] = 500                            # 改第一个人的血量
print(team[0])

for m in team:                                 # 全员加血
    m["hp"] += 100

print(team)
```

⚠️ `for m in team:` 里改 `m["hp"]`，**原列表里的数据真的会变** ——
因为 `m` 指的就是列表里那个字典本身，不是复制品。

（这个性质有时很方便，有时会坑人。今天先记住有这回事。）

---

## 🛠 今天的任务 · 队伍数据库

给你一支 6 人队伍，做一套查询分析：

```python
team = [
    {"name": "星野樱",   "hp": 340, "atk": 88,  "element": "火"},
    {"name": "月见琉璃", "hp": 280, "atk": 95,  "element": "水"},
    {"name": "天野灯",   "hp": 310, "atk": 72,  "element": "风"},
    {"name": "水城凛",   "hp": 250, "atk": 110, "element": "水"},
    {"name": "夜刀神澪", "hp": 420, "atk": 66,  "element": "暗"},
    {"name": "风见幽香", "hp": 360, "atk": 90,  "element": "火"},
]
```

| 要求 | 说明 |
|---|---|
| 逐行显示全队 | 名字、HP、ATK、属性四项都要 |
| 算总血量和平均攻击 | 平均保留 1 位小数 |
| 按攻击力从高到低排序并显示 | 用 `key=lambda` |
| 筛选出攻击力 >= 88 的成员 | 装进 `strong`，报出人数 |
| 新增一名成员 | 用 `.append()` 加一个字典 |
| 全员血量 +50 | 遍历时直接改 |
| 问玩家查哪个属性 | `input()`，列出该属性的所有成员 |
| 查不到要提示「没有这个属性的成员」 | |

> 💡 自己先算：总血量 1960、平均攻击 86.8、攻击最高水城凛(110)、
> 攻击 >= 88 的有 4 人（88/95/110/90）。
