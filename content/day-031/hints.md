## 提示 1 · 遍历时每一项都是字典

```python
for m in team:
    print(f"  {m['name']} · HP {m['hp']} · ATK {m['atk']} · {m['element']}属性")
```

`m` 每一圈是**一整个字典**，所以用 `m['name']` 取字段。

⚠️ 不是 `m[0]` —— 那是列表的取法。字典要用**字段名**。
⚠️ f-string 里层用**单引号**，外层是双引号，不然打架。

统计也是同一个循环里顺手做：

```python
total_hp = 0
total_atk = 0
for m in team:
    total_hp += m["hp"]
    total_atk += m["atk"]

avg_atk = round(total_atk / len(team), 1)
```

## 提示 2 · 排序和筛选

排序有个固定句式，照抄改字段名就行：

```python
team.sort(key=lambda m: m["atk"], reverse=True)
```

念作：「排序时，每一项 `m` 拿它的 `atk` 去比，从大到小」。

筛选是「建空列表 → 遍历 → 符合就 append」：

```python
strong = []
for m in team:
    if m["atk"] >= 88:
        strong.append(m)

print(f"攻击力 88 以上的有 {len(strong)} 人：")
for m in strong:
    print(f"  {m['name']}（{m['atk']}）")
```

## 提示 3 · 新增、批量改、按属性查

新增成员要 append **一整个字典**：

```python
team.append({"name": "雾岛遥", "hp": 300, "atk": 80, "element": "光"})
```

全员加血 —— 遍历时直接改，原数据真的会变：

```python
for m in team:
    m["hp"] += 50
```

按属性查询（跟筛选是同一个套路）：

```python
want = input("想查哪个属性的成员？").strip()

found = []
for m in team:
    if m["element"] == want:
        found.append(m)

if len(found) > 0:
    print(f"🔎 {want}属性成员共 {len(found)} 人：")
    for m in found:
        print(f"  {m['name']} · HP {m['hp']}")
else:
    print(f"🔎 没有这个属性的成员：「{want}」")
```

⚠️ 注意统计要在**加血之前**算，不然总血量就对不上答案了。
