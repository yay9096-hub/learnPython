# Day 30 · 图鉴系统
book = {
    "星野樱": 820,
    "月见琉璃": 995,
    "天野灯": 640,
    "水城凛": 998,
    "夜刀神澪": 770,
}

print("📖 === 角色图鉴 === 📖")

# ---------- 显示全部 ----------
for name, power in book.items():
    print(f"  {name} —— 战力 {power}")

print("─" * 30)
print(f"已收录 {len(book)} 人")

# ---------- 统计 ----------
total = sum(book.values())
avg = round(total / len(book), 1)
print(f"总战力：{total}")
print(f"平均战力：{avg}")

# ---------- 最强 ----------
best_name = ""
best_power = 0
for name, power in book.items():
    if power > best_power:
        best_power = power
        best_name = name

print(f"最强：{best_name}（{best_power}）")

# ---------- 条件统计 ----------
strong = 0
for name, power in book.items():
    if power >= 800:
        strong += 1

print(f"战力 800 以上：{strong} 人")

# ---------- 收录新角色 ----------
book["风见幽香"] = 905
print(f"\n✨ 新收录：风见幽香（905）")
print(f"图鉴现在有 {len(book)} 人")

# ---------- 查询 ----------
who = input("\n想查谁？").strip()

if who in book:
    print(f"🔎 {who} 的战力是 {book[who]}")
else:
    print(f"🔎 图鉴中暂无此人：「{who}」")
