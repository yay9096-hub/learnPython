# Day 41 · 队伍管理函数库
TEAM = [
    {"name": "星野樱",   "hp": 340, "atk": 88,  "element": "火"},
    {"name": "月见琉璃", "hp": 280, "atk": 95,  "element": "水"},
    {"name": "天野灯",   "hp": 310, "atk": 72,  "element": "风"},
    {"name": "水城凛",   "hp": 250, "atk": 110, "element": "水"},
    {"name": "风见幽香", "hp": 360, "atk": 90,  "element": "火"},
]

# ⚠️ 下面这几个「算」的函数里，一个 print 都不要写

# TODO 1: total_hp(team) -> 总血量，空队返回 0


# TODO 2: avg_atk(team) -> 平均攻击，空队返回 0（小心除以零！）


# TODO 3: strongest(team) -> 攻击力最高的那个字典，空队返回 None


# TODO 4: filter_by_element(team, element) -> 新列表


# TODO 5: filter_by_atk(team, min_atk) -> 新列表


# TODO 6: find_member(team, name) -> 字典，找不到返回 None


# ---------- 下面两个才负责打印 ----------

# TODO 7: show_team(team) -> 逐行打印全队


# TODO 8: show_report(team) -> 调用上面的函数拼一份报告


# ---------- 主流程 ----------
# TODO 9: 打印全队 + 报告
# TODO 10: 按属性筛一次、按攻击力筛一次，各打印结果
# TODO 11: 问一个名字，用 find_member 查，查不到提示「查无此人」
# TODO 12: 用空列表 [] 调一次 show_report，验证不会崩
