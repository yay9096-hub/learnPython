# Day 69 · 个人学习仪表盘
import json
import matplotlib.pyplot as plt

DATA = "我的学习记录.json"
REPORT = "学习报告.txt"
CHART = "学习图表.png"

STAGE_NAMES = {
    1: "会说话", 2: "会判断和重复", 3: "会管理数据", 4: "会拆分问题",
    5: "会和外界打交道", 6: "会造东西", 7: "会做出好看的",
}


# TODO 1: load_records(filename) -> 列表，文件不存在返回 []


# TODO 2: overview(records) -> 字典
#   done / total / minutes / avg / runs / errors / rate


# TODO 3: by_stage(records) -> {章号: (完成数, 总数, 总时长)}


# TODO 4: bar(value, total, width=20) -> 文字进度条
#   ⚠️ total 为 0 时不能崩


# TODO 5: highlights(records) -> (最投入的, 最顺的, 最费劲的)
#   没数据返回 (None, None, None)


# TODO 6: build_report(records) -> 整份报告的字符串（不要 print）
#   套路：lines = [] 一路 append，最后 "\n".join(lines)


# TODO 7: draw_charts(records, filename) -> 画四格图并 savefig
#   ⚠️ savefig 要在 show 之前


# ---------- 主流程 ----------
# TODO 8: 读数据；一天都没完成就提示并结束
# TODO 9: 打印报告 + 写进 REPORT 文件
# TODO 10: 画图并存成 CHART
