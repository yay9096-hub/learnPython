# Day 52 · CSV 成绩单
SCORES = "成绩.csv"
RANKING = "排名.csv"

RAW = [
    "姓名,语文,数学,英语",
    "星野樱,88,92,79",
    "月见琉璃,95,78,91",
    "天野灯,72,85,68",
    "水城凛,90,99,94",
    "夜刀神澪,65,71,82",
]


# TODO 1: write_lines_csv(filename, rows) -> 把字符串列表写成 CSV 文件


# TODO 2: read_csv(filename) -> 列表套字典
#   第一行是表头；纯数字的字段要转成 int
#   提示：用 zip(header, parts) 配对


# TODO 3: add_total(rows) -> 给每行加一个「总分」字段


# TODO 4: subject_avg(rows, subject) -> 某一科平均分，保留 1 位小数


# TODO 5: top_student(rows) -> 总分最高的那一行，空表返回 None


# TODO 6: sort_by_total(rows) -> 按总分从高到低排序，返回新列表


# TODO 7: write_csv(filename, rows, header) -> 写回 CSV
#   先写表头，每个值记得 str()


# ---------- 主流程 ----------
# TODO 8: 造出 成绩.csv，读进来，加总分
# TODO 9: 打印三科平均分
# TODO 10: 打印总分第一名
# TODO 11: 按总分排序，带名次显示全部
# TODO 12: 写成 排名.csv，再读回来验证
# TODO 13: 问玩家一个名字，查他的各科成绩，查不到要提示
