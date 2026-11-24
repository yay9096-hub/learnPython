## 提示 1 · 先写一个「只有 A 打 B」的版本

别想着一口气写完。先让 A 单方面打 B：

```python
while hp_b > 0:
    turn += 1
    dmg = random.randint(20, 50)
    hp_b -= dmg
    total_a += dmg
    print(f"第 {turn} 回合：{name_a} 造成 {dmg} 点伤害 → {name_b} 剩 {hp_b} HP")
```

跑一次，确认血量在往下掉、回合数在涨、最后能停下来。

**能跑通了，再加 B 的反击。**

## 提示 2 · 加上 B 的反击和那个 break

B 的四步跟 A 一模一样，只是把 a 和 b 对调：

```python
while hp_a > 0 and hp_b > 0:
    turn += 1

    # --- A 出手 ---
    dmg = random.randint(20, 50)
    hp_b -= dmg
    total_a += dmg
    print(f"第 {turn} 回合：{name_a} 造成 {dmg} 点伤害 → {name_b} 剩 {hp_b} HP")

    if hp_b <= 0:
        break                        # ← B 倒下了，别让它还手

    # --- B 出手 ---
    dmg = random.randint(20, 50)
    hp_a -= dmg
    total_b += dmg
    print(f"第 {turn} 回合：{name_b} 造成 {dmg} 点伤害 → {name_a} 剩 {hp_a} HP")
```

那个 `break` 是今天的重点 —— 没有它，B 死了还能反击一次，
两个人就会一起归零，变成假的「同归于尽」。

## 提示 3 · 判胜负要按顺序

```python
if hp_a <= 0 and hp_b <= 0:
    print("🤝 同归于尽！")
elif hp_a > 0:
    print(f"🏆 {name_a} 获胜！打了 {turn} 个回合，共造成 {total_a} 点伤害")
else:
    print(f"🏆 {name_b} 获胜！打了 {turn} 个回合，共造成 {total_b} 点伤害")
```

⚠️ 「同归于尽」必须放**最前面**（Day 12 的分支顺序）：
它是最特殊的情况，放后面就永远轮不到它了。
