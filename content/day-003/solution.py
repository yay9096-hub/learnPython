# Day 3 · 伤害计算器

atk = 88
defense = 25
crit_rate = 1.5

damage = atk - defense
crit_damage = round((atk - defense) * crit_rate, 1)

print("⚔️  战斗开始！")
print(f"普通攻击：造成 {damage} 点伤害")
print(f"暴击！！：造成 {crit_damage} 点伤害")
print(f"暴击比普通攻击多打了 {round(crit_damage - damage, 1)} 点")
