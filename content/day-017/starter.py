# Day 17 · 十连抽
import random

RARITIES = ["SSR", "SR", "SR", "R", "R", "R", "R", "R"]
NAMES = ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪"]

print("🎴 ===== 十 连 抽 ===== 🎴")

# TODO 1: 循环外先准备两个统计变量
#   ssr_count = 0      记录出了几个 SSR
#   best = 0           记录最高战力


# TODO 2: for 循环抽 10 次
#   每一抽：
#     ① rarity = random.choice(RARITIES)
#     ② char   = random.choice(NAMES)
#     ③ power  = random.randint(50, 999)
#     ④ 打印 第 i+1 抽 的结果
#     ⑤ 如果是 SSR，ssr_count += 1，并给个特别提示
#     ⑥ 如果 power 比 best 大，就更新 best


# TODO 3: 循环结束后打印总结（要包含「十连结束」四个字）

