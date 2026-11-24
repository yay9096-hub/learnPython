# Day 66 · 日志分析器
import re

LOG = """
2026-09-01 Day 1 用了 42 分钟，联系 sakura@example.com
2026-09-02 Day 2 用了 35 分钟，参考了 https://docs.python.org/zh-cn/3/
2026-09-03 Day 3 用了 58 分钟，问了老师 13812345678
2026-09-04 Day 11 用了 40 分钟，笔记在 http://note.example.cn/py
2026-09-05 Day 12 用了 45 分钟，同学 ruri@test.org 也在学
"""

print("🔍 === 日志分析器 === 🔍")

# TODO 1: find_dates(text) -> 所有 YYYY-MM-DD 日期

# TODO 2: find_numbers(text) -> 所有整数（要转成 int）

# TODO 3: find_emails(text) -> 所有邮箱

# TODO 4: find_urls(text) -> 所有网址（http 和 https 都要）

# TODO 5: find_day_minutes(text) -> [(天数, 分钟), ...]，都要是 int
#   模式参考：r"Day (\d+) 用了 (\d+) 分钟"

# TODO 6: mask_phones(text) -> 手机号中间四位变成 ****
#   用 re.sub 和 \1 \2 分组引用

# TODO 7: count_chinese(text) -> 中文字符总数


# ---------- 主流程 ----------
# TODO 8: 每个函数各调一次并打印结果
# TODO 9: 用 find_day_minutes 算总时长和平均时长
# TODO 10: 打印打码后的完整文本
# TODO 11: 用 re.search 找第一个日期，找不到要提示
