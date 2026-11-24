## 提示 1 · 三个列表用同一个编号对齐

```python
for i in range(len(names)):
    print(f"  {names[i]} · HP {hps[i]} · ATK {atks[i]}")
```

`range(len(names))` 给出 `0 1 2 3 4`，
同一个 `i` 从三个列表里取，取出来的就是同一个人的三项数据。

⚠️ 这里**不能**用 `for name in names:` ——
那样只拿得到名字，拿不到对应的血量和攻击。

## 提示 2 · 现成的统计函数

```python
total_hp = sum(hps)
avg_atk = round(sum(atks) / len(atks), 1)

top_hp = max(hps)
low_hp = min(hps)
```

但 `max(hps)` 只给你**数值**，不给名字。想知道是谁，用 `.index()`：

```python
top_hp = max(hps)
top_name = names[hps.index(top_hp)]
```

念一遍：「找出最大值在 hps 里的**位置**，再用这个位置去 names 里取名字」。

## 提示 3 · 条件统计只能靠循环

`sum()` 只会闷头加，没法「只加满足条件的」。所以：

```python
strong = 0
for hp in hps:
    if hp > 300:
        strong += 1

print(f"血量超过 300 的有 {strong} 人")
```

**这就是累加器仍然重要的原因** —— `sum()` 是快捷方式，累加器是万能的。

最后把结果都打印出来：

```python
print(f"总血量：{total_hp}")
print(f"平均攻击力：{avg_atk}")
print(f"血量最高：{top_name}（{top_hp}）")
print(f"血量最低：{low_name}（{low_hp}）")
print(f"血量超过 300 的有 {strong} 人")
```

自己对一下答案：1600 / 86.2 / 夜刀神澪 420 / 水城凛 250 / 3 人。
