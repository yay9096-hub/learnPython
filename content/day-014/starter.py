# Day 14 · 猜数字游戏
import random

answer = random.randint(1, 100)
count = 0
guess = 0        # 先给它一个值，不然循环条件里用不了

print("🎯 我想好了一个 1~100 的数字，你猜！")

# TODO: 用 while 循环，只要还没猜对就一直问
#   循环里要做四件事：
#     ① 问一个数字（记得 int()）
#     ② count += 1
#     ③ 猜大了提示「太大」，猜小了提示「太小」
#     ④ 猜对了循环自然就停了


# TODO: 循环结束后，恭喜她并报出用了几次

