# Day 51 · 学习打卡系统
import json
from datetime import date

RECORDS = "打卡记录.json"


# TODO 1: load_records(filename) -> 列表。文件不存在返回 []


# TODO 2: save_records(filename, records) -> 存成 json


# TODO 3: check_in(records, day_text, minutes, topic) -> 加一条
#   同一天不能重复打卡（先检查有没有这个日期）
#   每条形如 {"date": ..., "minutes": ..., "topic": ...}


# TODO 4: total_minutes(records) -> 总分钟数


# TODO 5: longest_streak(records) -> 最长连续天数，空记录返回 0
#   套路：去重 -> 转成 date -> 排序 -> 看相邻两天差几天


# TODO 6: current_streak(records, today_text) -> 当前连击
#   从 today 往回数；今天没打卡返回 0


# TODO 7: show_records(records) -> 按日期排序显示


# ---------- 主流程 ----------
# TODO 8: load_records（文件不存在）
# TODO 9: 补录至少 5 天，其中故意断开一天
# TODO 10: 同一天打两次卡，验证不重复
# TODO 11: 打印总时长、最长连击、当前连击
# TODO 12: show_records 显示全部
# TODO 13: 问玩家今天学了多少分钟，打卡并存盘，再读回来验证
