# Day 34 · 班级成绩管理系统
students = [
    {"name": "星野樱",   "chinese": 88, "math": 92, "english": 79},
    {"name": "月见琉璃", "chinese": 95, "math": 78, "english": 91},
    {"name": "天野灯",   "chinese": 72, "math": 85, "english": 68},
    {"name": "水城凛",   "chinese": 90, "math": 99, "english": 94},
    {"name": "夜刀神澪", "chinese": 65, "math": 71, "english": 82},
    {"name": "风见幽香", "chinese": 84, "math": 88, "english": 87},
]

SUBJECTS = ["chinese", "math", "english"]
CN = {"chinese": "语文", "math": "数学", "english": "英语"}

print("📊 === 班级成绩管理系统 === 📊")

# TODO 1: 给每个人加一个 total 字段（三科之和）


# TODO 2: 逐行显示成绩单（姓名 / 三科 / 总分）


# TODO 3: 每一科的最高分、最低分、平均分（保留 1 位小数）
#   提示：先把这一科所有人的分数收集成一个列表，再用 max/min/sum


# TODO 4: 按总分从高到低排序，显示排行榜带名次
#   students.sort(key=lambda s: s["total"], reverse=True)


# TODO 5: 等第统计
#   >=270 优秀 / >=240 良好 / >=210 及格 / 其余 待努力


# TODO 6: 问一个名字，显示完整成绩和名次；查不到提示「查无此人」
