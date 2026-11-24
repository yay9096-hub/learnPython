# Day 20 · 回合制战斗模拟
import random

name_a = "星野樱"
name_b = "暗影骑士"
hp_a = 200
hp_b = 200

turn = 0
total_a = 0      # A 造成的总伤害
total_b = 0      # B 造成的总伤害

print(f"⚔️  {name_a}  VS  {name_b}")
print("─" * 30)

# TODO: while 循环，只要双方都还活着就继续
#   每一回合：
#     ① turn += 1
#     ② A 出手：算伤害、扣 B 的血、累加 total_a、打印战况
#     ③ 如果 B 倒下了就 break（不然死人还能反击！）
#     ④ B 出手：同样四步


print("─" * 30)
# TODO: 判断谁获胜（先判同归于尽，再判 A、B）
