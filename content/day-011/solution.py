# Day 11 · 魔法结界
print("🔮 === 樱花结界 · 守卫处 === 🔮")

password = input("报上口令：")

if password == "sakura":
    print("✨ 口令正确，欢迎进入结界")
else:
    print("⛔ 口令错误，拒绝入内")

mp = int(input("报上你的魔力值："))

if mp >= 50:
    print(f"魔力 {mp} 点，足够施法！")
else:
    print(f"魔力只有 {mp} 点，不足以施法")
