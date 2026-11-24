# Day 48 · 日记阅读器
DIARY = "我的日记.txt"

ENTRIES = [
    "2026-09-02 今天学会了写文件，程序终于能记住东西了",
    "2026-09-03 写文件比想象中简单，就是别忘了 encoding",
    "2026-09-04 刷新页面文件还在，有点感动",
    "2026-09-05 读文件也学会了，w 和 a 别搞混",
    "2026-09-06 明天要做错题本，感觉能派上大用场",
]

# TODO 1: 先用 "w" 把 ENTRIES 写进 DIARY，每篇一行


# TODO 2: read_all(filename) -> 整个文件的字符串


# TODO 3: read_lines(filename) -> 列表，每项 strip 过、去掉空行


# TODO 4: count_lines(filename) -> 非空行数


# TODO 5: count_chars(filename) -> 总字数（不算换行符）


# TODO 6: find_by_date(filename, date) -> 那一天的日记，找不到返回 None


# TODO 7: search(filename, keyword) -> 所有含关键词的行（列表）


# TODO 8: show_numbered(filename) -> 带行号打印全部


# ---------- 主流程 ----------
# TODO 9: 打印总篇数和总字数
# TODO 10: show_numbered 列出全部
# TODO 11: find_by_date 查一个存在的、一个不存在的日期
# TODO 12: 问玩家关键词，用 search 找，一条没有要提示
