# Day 17 · 十连抽
import random

RARITIES = ["SSR", "SR", "SR", "R", "R", "R", "R", "R"]
NAMES = ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"]

print("🎴 ===== 十 连 抽 ===== 🎴")

ssr_count = 0
best = 0

for i in range(10):
    rarity = random.choice(RARITIES)
    char = random.choice(NAMES)
    power = random.randint(50, 999)

    print(f"第 {i + 1} 抽：[{rarity}] {char} · 战力 {power}")

    if power > best:
        best = power

    if rarity != "SSR":
        continue

    ssr_count += 1
    print("        ✨✨ SSR！金光闪闪！✨✨")

print("=" * 34)
print(f"十连结束！本次出了 {ssr_count} 个 SSR")
print(f"最强的一张：战力 {best}")
