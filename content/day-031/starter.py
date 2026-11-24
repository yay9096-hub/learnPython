# Day 31 · 队伍数据库
team = [
    {"name": "星野樱",   "hp": 340, "atk": 88,  "element": "火"},
    {"name": "月见琉璃", "hp": 280, "atk": 95,  "element": "水"},
    {"name": "天野灯",   "hp": 310, "atk": 72,  "element": "风"},
    {"name": "水城凛",   "hp": 250, "atk": 110, "element": "水"},
    {"name": "夜刀神澪", "hp": 420, "atk": 66,  "element": "暗"},
    {"name": "风见幽香", "hp": 360, "atk": 90,  "element": "火"},
]

print("🗃 === 队伍数据库 === 🗃")

# TODO 1: 遍历 team 逐行显示（名字 / HP / ATK / 属性）


# TODO 2: 算总血量 total_hp 和平均攻击 avg_atk（保留 1 位小数）


# TODO 3: 按攻击力从高到低排序，再显示一次
#   team.sort(key=lambda m: m["atk"], reverse=True)


# TODO 4: 筛选出攻击力 >= 88 的成员 -> strong，报出人数


# TODO 5: 用 append() 新增一名成员（记得是一整个字典）


# TODO 6: 遍历给全员血量 +50


# TODO 7: 问玩家查哪个属性，列出该属性的所有成员
#   一个都没有要提示「没有这个属性的成员」
