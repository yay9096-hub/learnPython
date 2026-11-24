# Day 31 · 队伍数据库
team = [
    {"name": "星野樱",   "hp": 340, "atk": 88,  "element": "火"},
    {"name": "月见琉璃", "hp": 280, "atk": 95,  "element": "水"},
    {"name": "天野灯",   "hp": 310, "atk": 72,  "element": "风"},
    {"name": "水城凛",   "hp": 250, "atk": 110, "element": "水"},
    {"name": "夜刀神澪", "hp": 420, "atk": 66,  "element": "暗"},
    {"name": "风见幽香", "hp": 360, "atk": 90,  "element": "火"},
]

print("🗃 === 队伍数据库 === 🗃")

# ---------- 全员名册 ----------
for m in team:
    print(f"  {m['name']} · HP {m['hp']} · ATK {m['atk']} · {m['element']}属性")

# ---------- 统计 ----------
total_hp = 0
total_atk = 0
for m in team:
    total_hp += m["hp"]
    total_atk += m["atk"]

avg_atk = round(total_atk / len(team), 1)

print("─" * 40)
print(f"总血量：{total_hp}")
print(f"平均攻击：{avg_atk}")

# ---------- 按攻击排序 ----------
team.sort(key=lambda m: m["atk"], reverse=True)

print("\n⚔️ 攻击力排行：")
for i, m in enumerate(team):
    print(f"  第 {i + 1} 名 {m['name']} —— {m['atk']}")

# ---------- 筛选 ----------
strong = []
for m in team:
    if m["atk"] >= 88:
        strong.append(m)

print(f"\n攻击力 88 以上的有 {len(strong)} 人：")
for m in strong:
    print(f"  {m['name']}（{m['atk']}）")

# ---------- 新增成员 ----------
team.append({"name": "雾岛遥", "hp": 300, "atk": 80, "element": "光"})
print(f"\n✨ 新成员加入！队伍现在 {len(team)} 人")

# ---------- 全员加血 ----------
for m in team:
    m["hp"] += 50

print("💊 全员血量 +50")

# ---------- 按属性查询 ----------
want = input("\n想查哪个属性的成员？（火/水/风/暗/光）").strip()

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
