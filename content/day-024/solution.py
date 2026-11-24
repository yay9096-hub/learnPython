# Day 24 · 背包系统
print("🎒 === 冒险者背包 === 🎒")

bag = []
loot = ["铁剑", "护符", "红药水", "面包"]

# ---------- 批量捡 ----------
for item in loot:
    bag.append(item)
    print(f"✅ 捡到了 {item}！背包现在有 {len(bag)} 件")

print(f"当前背包：{bag}\n")

# ---------- 玩家自己捡一件 ----------
new_item = input("你还想捡点什么？").strip()
bag.append(new_item)
print(f"✅ 捡到了 {new_item}！背包现在有 {len(bag)} 件")
print(f"当前背包：{bag}\n")

# ---------- 扔东西 ----------
drop = input("想扔掉什么？").strip()

if drop in bag:
    bag.remove(drop)
    print(f"🗑 扔掉了 {drop}")
else:
    print(f"❓ 背包里没有 {drop}，扔不了")

print(f"当前背包：{bag}\n")

# ---------- 掏出最后一件 ----------
last = bag.pop()
print(f"✋ 掏出了 {last}")

print(f"\n最终背包：{bag}")
print(f"一共 {len(bag)} 件")
