# Day 64 · 队伍数据可视化
import matplotlib.pyplot as plt

names = ["星野樱", "月见琉璃", "天野灯", "水城凛", "风见幽香"]
hp    = [340, 280, 310, 250, 360]
atk   = [88, 95, 72, 110, 90]

print("📊 === 队伍数据 === 📊")

# TODO 1: 在终端打印文字版摘要：总血量、平均攻击、最强的是谁


# TODO 2: plt.figure(figsize=(9, 4)) 设置整张图的尺寸


# TODO 3: 左边一格（subplot 1 行 2 列的第 1 个）
#   用 barh 画血量，加标题和 xlabel


# TODO 4: 右边一格（第 2 个）
#   用 bar 画攻击力，加标题和 ylabel
#   用循环 plt.text 在每根柱子上标出数值
#   记得 plt.ylim 把上限拉高一点，不然数字顶出去


# TODO 5: plt.tight_layout() 然后 plt.show()
