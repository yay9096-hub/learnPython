# Day 65 · 我的学习报告
import json
import matplotlib.pyplot as plt

DATA = "我的学习记录.json"

# TODO 1: 读 DATA，挑出 status == "done" 的记录 -> done
#   ⚠️ 一条都没有时要打印提示并停下来（别让后面的图崩）


# TODO 2: 终端摘要
#   已完成天数/总天数、总分钟、平均每天、运行总数、报错总数
#   报错率（报错 ÷ 运行 × 100，保留 1 位）
#   花时间最长的那天是哪天、做的什么


# TODO 3: plt.figure(figsize=(11, 7))，然后画 2x2 四格

#   左上 subplot(2,2,1)：每天学习时长折线图（marker="o"）

#   右上 subplot(2,2,2)：累计时长折线图 + fill_between
#     累计用循环：total += r["minutes"]

#   左下 subplot(2,2,3)：运行 vs 报错双折线，要 label + legend()

#   右下 subplot(2,2,4)：各章时长占比饼图，autopct="%1.0f%%"


# TODO 4: plt.tight_layout() + plt.show()
