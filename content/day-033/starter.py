# Day 33 · 星座连线图
import turtle

names  = ["天枢", "天璇", "天玑", "天权", "玉衡", "开阳", "摇光"]
points = [(-160, 40), (-100, 70), (-40, 60), (10, 20), (70, 10), (130, 40), (180, 90)]
sizes  = [10, 8, 9, 7, 11, 9, 12]

print("✨ === 北斗七星 === ✨")

# TODO 1: 用 zip 把三组数据配对遍历，一行显示
#   提示：for name, (x, y), size in zip(names, points, sizes):


# TODO 2: 算出 x 的平均值和 y 的平均值（星座中心），保留 1 位小数


# TODO 3: 找出最亮的星（size 最大），名字和亮度都要


# TODO 4: 用 turtle 把七颗星按坐标连成折线
#   记得 penup -> goto 第一个点 -> pendown


# TODO 5: 在最亮那颗星旁边 write 上名字
