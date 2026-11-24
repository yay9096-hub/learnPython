# Day 23 · 队伍名单
print("📋 === 派森学院 · 队伍名单 === 📋")

team = ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"]

print(f"当前队伍共 {len(team)} 人")
print(f"队长：{team[0]}")
print(f"替补：{team[-1]}")

print("\n--- 点名 ---")
for i, member in enumerate(team):
    print(f"{i + 1} 号：{member}")

print("\n⚡ 人员变动：月见琉璃转学了，由风见幽香顶替")
team[1] = "风见幽香"

print("\n--- 重新点名 ---")
for i, member in enumerate(team):
    print(f"{i + 1} 号：{member}")

print(f"\n队伍依然是 {len(team)} 人")
