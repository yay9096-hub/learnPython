# Day 27 · 战力排行榜
names  = ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪", "风见幽香"]
powers = [820, 995, 640, 998, 770, 905]

print("🏆 === 战力排行榜 === 🏆")

# ---------- 打包 ----------
pairs = []
for i in range(len(names)):
    pairs.append([powers[i], names[i]])

# ---------- 排序 ----------
pairs.sort(reverse=True)

# ---------- 榜单 ----------
print("─" * 32)
for i, pair in enumerate(pairs):
    print(f"第 {i + 1} 名 · {pair[1]} · 战力 {pair[0]}")
print("─" * 32)

# ---------- 前三名 ----------
print("🥇 登上领奖台的是：")
for power, name in pairs[:3]:
    print(f"   {name}（{power}）")

print(f"\n榜首：{pairs[0][1]}  |  榜尾：{pairs[-1][1]}")

# ---------- 查名次 ----------
ranked_names = []
for power, name in pairs:
    ranked_names.append(name)

who = input("\n想查谁的名次？").strip()

if who in ranked_names:
    place = ranked_names.index(who) + 1
    print(f"🔎 {who} 排第 {place} 名")
else:
    print(f"🔎 榜上无名：查无此人「{who}」")
