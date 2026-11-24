# Day 7 · RPG 开场白系统

# ========== 第一幕 · 标题画面 ==========
print("""
╔══════════════════════════════════╗
║                                  ║
║      ✦  派 森 学 院 物 语  ✦     ║
║        ~ Pyson Academy ~         ║
║                                  ║
╚══════════════════════════════════╝
""")

# ========== 第二幕 · 角色创建 ==========
name = input("旅人，你叫什么名字？").strip()
age = int(input("你今年多大？"))
element = input("你的属性是？（fire / water / wind）").strip()
lucky = int(input("最后，说一个幸运数字："))

hp = age * 20 + lucky
mp = age * 10 + lucky * 2
rank = len(name)
title = element.upper()

# ========== 第三幕 · 角色卡 ==========
stars = "★" * rank

print(f"\n{stars} 角色创建完成 {stars}")
print(f"【{title} 之子】{name} · {rank} 阶魔导士")
print("HP: " + str(hp), "MP: " + str(mp), f"Lv.{rank}", sep="  |  ")
print(f"\n樱花从窗外飘进来，落在你的肩上。\n{name}，你的故事从这里开始。")
