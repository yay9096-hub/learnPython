# Day 22 · 猜数字 · 进化版
import random

print("🎯 ===== 猜 数 字 · 进 化 版 ===== 🎯")

games = 0
wins = 0
best = 999

# ---------- 选难度 ----------
level = ""
while level not in ["1", "2", "3"]:
    print("选择难度：")
    print("  1) 简单   1~50，  10 次机会")
    print("  2) 普通   1~100，  7 次机会")
    print("  3) 困难   1~500， 12 次机会")
    level = input("你的选择（1/2/3）：").strip()
    if level not in ["1", "2", "3"]:
        print("❓ 请输入 1、2 或 3\n")

if level == "1":
    top, chances = 50, 10
elif level == "2":
    top, chances = 100, 7
else:
    top, chances = 500, 12

# ---------- 游戏主循环 ----------
while True:
    games += 1
    answer = random.randint(1, top)
    guess = -1
    tries = 0

    print(f"\n=== 第 {games} 局 · 我想好了 1~{top} 的一个数，你有 {chances} 次机会 ===")

    while guess != answer and tries < chances:
        tries += 1
        guess = int(input(f"第 {tries}/{chances} 次，猜："))

        if guess > answer:
            print("  📉 太大了")
        elif guess < answer:
            print("  📈 太小了")

    if guess == answer:
        wins += 1
        print(f"🎉 猜对啦！这局用了 {tries} 次")
        if tries < best:
            best = tries
    else:
        print(f"💀 次数用完了，答案是 {answer}")

    again = input("再来一局吗？(y/n)：").strip().lower()
    if again != "y":
        break

# ---------- 战报 ----------
print("\n" + "═" * 34)
print("📊 战报")
print(f"  总局数：{games}")
print(f"  胜利：{wins}    失败：{games - wins}")
if wins > 0:
    print(f"  最佳成绩：{best} 次猜中")
else:
    print("  最佳成绩：还没赢过呢，再来！")
print("═" * 34)
