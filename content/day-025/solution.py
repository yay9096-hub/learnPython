# Day 25 · 队伍属性统计
names = ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"]
hps   = [340, 280, 310, 250, 420]
atks  = [88, 95, 72, 110, 66]

print("📊 === 队伍属性面板 === 📊")

# ---------- 逐行显示 ----------
for i in range(len(names)):
    print(f"  {names[i]} · HP {hps[i]} · ATK {atks[i]}")

print("─" * 30)

# ---------- 基础统计 ----------
total_hp = sum(hps)
avg_atk = round(sum(atks) / len(atks), 1)

# ---------- 最强最弱 ----------
top_hp = max(hps)
top_name = names[hps.index(top_hp)]

low_hp = min(hps)
low_name = names[hps.index(low_hp)]

# ---------- 条件统计 ----------
strong = 0
for hp in hps:
    if hp > 300:
        strong += 1

# ---------- 报告 ----------
print(f"队伍人数：{len(names)}")
print(f"总血量：{total_hp}")
print(f"平均攻击力：{avg_atk}")
print(f"血量最高：{top_name}（{top_hp}）")
print(f"血量最低：{low_name}（{low_hp}）")
print(f"血量超过 300 的有 {strong} 人")
