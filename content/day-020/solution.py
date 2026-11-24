# Day 20 · 回合制战斗模拟
import random

name_a = "星野樱"
name_b = "暗影骑士"
hp_a = 200
hp_b = 200

turn = 0
total_a = 0
total_b = 0

print(f"⚔️  {name_a}  VS  {name_b}")
print("─" * 30)

while hp_a > 0 and hp_b > 0:
    turn += 1

    dmg = random.randint(20, 50)
    hp_b -= dmg
    total_a += dmg
    print(f"第 {turn} 回合：{name_a} 造成 {dmg} 点伤害 → {name_b} 剩 {hp_b} HP")

    if hp_b <= 0:
        break

    dmg = random.randint(20, 50)
    hp_a -= dmg
    total_b += dmg
    print(f"第 {turn} 回合：{name_b} 造成 {dmg} 点伤害 → {name_a} 剩 {hp_a} HP")

print("─" * 30)

if hp_a <= 0 and hp_b <= 0:
    print("🤝 同归于尽！")
elif hp_a > 0:
    print(f"🏆 {name_a} 获胜！打了 {turn} 个回合，共造成 {total_a} 点伤害")
else:
    print(f"🏆 {name_b} 获胜！打了 {turn} 个回合，共造成 {total_b} 点伤害")
