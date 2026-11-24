# Day 21 · 文字冒险游戏
import random

# ========== 第一幕 · 角色创建 ==========
print("""
╔══════════════════════════════════╗
║      ✦  樱 之 森 冒 险 记  ✦      ║
╚══════════════════════════════════╝
""")

name = input("旅人，你叫什么名字？").strip()
hp = random.randint(80, 150)
atk = random.randint(20, 40)
steps = 0
turns = 0
ending = ""

print(f"\n{name}，你的旅程开始了。")
print(f"HP {hp} · 攻击力 {atk}\n")

# ========== 第二幕 · 岔路口 ==========
road = ""
while road not in ["1", "2"]:
    print("眼前是一个岔路口。")
    print("  1) 走进樱花森林")
    print("  2) 走进幽暗洞穴")
    road = input("你的选择（1/2）：").strip()
    if road not in ["1", "2"]:
        print("❓ 听不懂，请输入 1 或 2\n")

steps += 1

if road == "1":
    print("\n🌸 你走进森林，一只影狼挡住了去路。")
    choice = ""
    while choice not in ["1", "2"]:
        print("  1) 拔剑迎战")
        print("  2) 悄悄绕开")
        choice = input("你的选择（1/2）：").strip()
        if choice not in ["1", "2"]:
            print("❓ 听不懂，请输入 1 或 2\n")

    steps += 1

    if choice == "1":
        wolf_hp = 100
        while wolf_hp > 0 and hp > 0:
            turns += 1
            wolf_hp -= atk
            print(f"  第 {turns} 回合：你砍出 {atk} 点伤害，影狼剩 {wolf_hp} HP")
            if wolf_hp <= 0:
                break
            bite = random.randint(10, 25)
            hp -= bite
            print(f"  第 {turns} 回合：影狼咬了你 {bite} 点，你剩 {hp} HP")

        if hp > 0:
            ending = "勇者结局"
        else:
            ending = "陨落结局"
    else:
        ending = "平凡结局"

else:
    print("\n🕯 你走进洞穴，角落里有一个落满灰尘的宝箱。")
    choice = ""
    while choice not in ["1", "2"]:
        print("  1) 打开宝箱")
        print("  2) 转身离开")
        choice = input("你的选择（1/2）：").strip()
        if choice not in ["1", "2"]:
            print("❓ 听不懂，请输入 1 或 2\n")

    steps += 1

    if choice == "1":
        ending = "宝藏结局"
    else:
        ending = "平凡结局"

# ========== 第三幕 · 结局 ==========
print("\n" + "═" * 34)

if ending == "勇者结局":
    print(f"⚔️  【勇者结局】{name} 击败了影狼，成为森林的守护者！")
elif ending == "宝藏结局":
    print(f"💎 【宝藏结局】{name} 打开宝箱，从此富可敌国！")
elif ending == "陨落结局":
    print(f"💀 【陨落结局】{name} 倒在了影狼的爪下……")
else:
    print(f"🌾 【平凡结局】{name} 平安回到了村子，日子照常。")

print(f"你走了 {steps} 步，打了 {turns} 个回合，剩余 HP {hp}")
print("═" * 34)
