## 提示 1 · 拆开就什么都能做了

```python
words = danmaku.split()
print(f"总共接收到 {len(words)} 条弹幕")
```

拆完 `print(words)` 看一眼，你会发现它就是一个普通列表 ——
Day 23~27 学的全部本事（`len`、`count`、`in`、切片、排序）**立刻全都能用**。

## 提示 2 · 去重的固定套路

**建一个空列表，遍历时「不在里面才加」**：

```python
unique = []
for w in words:
    if w not in unique:
        unique.append(w)

print(f"不重复的弹幕有 {len(unique)} 种")
```

念一遍：「如果这个词还没被收录过，就收录它」。

这个套路非常常用，记住它。（第 32 天会学到 `set`，一行就能去重，
但先手写一遍才知道它在干什么。）

## 提示 3 · 统计 + 找最值 + join

遍历**去重后**的词，去**原始列表**里数次数：

```python
best_word = ""
best_count = 0

for w in unique:
    n = words.count(w)
    bar = "█" * n                        # Day 5 的文字乘法，画个小柱状图
    print(f"  {w:<6} {bar} {n} 次")

    if n > best_count:                   # Day 20 的找最值
        best_count = n
        best_word = w
```

⚠️ 是在 `words`（12 条原始弹幕）里数，不是在 `unique` 里数 ——
`unique` 里每个词只有一份，数出来永远是 1。

最后拼一行：

```python
print(f"🏆 刷得最多的是「{best_word}」，共 {best_count} 次")
print(f"出现过的词：{' / '.join(unique)}")
```

> 💡 `{w:<6}` 是让文字左对齐占 6 格，柱状图才能对齐。不写也不影响判题。
