# Day 14 · 猜数字游戏
import random

answer = random.randint(1, 100)
count = 0
guess = 0

print("🎯 我想好了一个 1~100 的数字，你猜！")

while guess != answer:
    guess = int(input("猜一个数字："))
    count += 1

    if guess > answer:
        print("📉 太大了！再试试")
    elif guess < answer:
        print("📈 太小了！再试试")

print(f"🎉 猜对啦！答案就是 {answer}，你一共用了 {count} 次")
