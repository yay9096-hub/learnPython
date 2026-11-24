## 提示 1 · 统计变量要放在循环外面

这是今天唯一的难点，也是最容易错的地方：

```python
ssr_count = 0        # ← 循环外面，只执行一次
best = 0

for i in range(10):
    ...
    ssr_count += 1   # ← 循环里面，每次累加

print(ssr_count)     # ← 循环外面，用结果
```

如果把 `ssr_count = 0` 写进循环里，**每圈都会归零**，最后永远是 0 或 1。

> 🧠 口诀：**归零在外，累加在内，使用在外。**

## 提示 2 · 十连的骨架

```python
for i in range(10):
    rarity = random.choice(RARITIES)
    char = random.choice(NAMES)
    power = random.randint(50, 999)

    print(f"第 {i + 1} 抽：[{rarity}] {char} · 战力 {power}")
```

⚠️ 是 `i + 1` 不是 `i` —— `range(10)` 给的是 0~9，
显示给人看要从 1 开始。

## 提示 3 · 统计和找最值

统计 SSR：

```python
    if rarity == "SSR":
        ssr_count += 1
        print("        ✨✨ SSR！金光闪闪！✨✨")
```

找最高战力（这个套路记住，以后天天用）：

```python
    if power > best:
        best = power
```

念一遍：「如果这张比目前最好的还好，那它就是新的最好的」。

用 `continue` 的一种写法（效果一样，风格不同）：

```python
    if rarity != "SSR":
        continue                       # 不是 SSR，这一圈到此为止

    ssr_count += 1                     # 能走到这里的，一定是 SSR
    print("        ✨✨ SSR！✨✨")
```

最后别忘了循环**外面**的总结：

```python
print(f"十连结束！本次出了 {ssr_count} 个 SSR")
print(f"最强的一张：战力 {best}")
```
