## 提示 1 · items() 是遍历字典的标准写法

```python
for name, power in book.items():
    print(f"  {name} —— 战力 {power}")
```

一次拿到**键和值**，比 `for name in book:` 再 `book[name]` 直接得多。

记住这个形状：`for 键, 值 in 字典.items():`

## 提示 2 · values() 拿去统计

```python
total = sum(book.values())
avg = round(total / len(book), 1)

print(f"总战力：{total}")
print(f"平均战力：{avg}")
```

Day 25 学的 `sum` / `max` / `min` 全都能直接用在 `.values()` 上。

找最强的（Day 20 的老套路，但字典版更清爽）：

```python
best_name = ""
best_power = 0

for name, power in book.items():
    if power > best_power:
        best_power = power
        best_name = name
```

不用像 Day 25 那样操心两个列表对不对得上 —— **键和值天生绑在一起**。

## 提示 3 · 收录和查询

收录新角色就是赋值：

```python
book["风见幽香"] = 905
print(f"图鉴现在有 {len(book)} 人")
```

查询记得先检查：

```python
who = input("想查谁？").strip()

if who in book:
    print(f"🔎 {who} 的战力是 {book[who]}")
else:
    print(f"🔎 图鉴中暂无此人：「{who}」")
```

条件统计（800 以上几人）：

```python
strong = 0
for name, power in book.items():
    if power >= 800:
        strong += 1
```

注意是 `>=` 不是 `>` —— 「800 以上」包含 800 本身。
