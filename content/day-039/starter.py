# Day 39 · 角色属性生成器
import random


# TODO 1: roll_stats(level) -> 返回三个值 hp, mp, atk
#   hp  = randint(50, 100) + level * 20
#   mp  = randint(20, 60)  + level * 10
#   atk = randint(10, 30)  + level * 5


# TODO 2: judge_stats(hp, mp, atk) -> 返回两个值 (评级, 总和)
#   总和 >=400 "优秀"，>=300 "普通"，其余 "偏弱"


# TODO 3: make_role(name, level) -> 返回一个字典
#   至少含 name / level / hp / mp / atk / rank
#   内部要调用 roll_stats 和 judge_stats


# TODO 4: check_name(name) -> 返回两个值 (是否合法, 说明)
#   长度 2~8 算合法


# ---------- 主流程 ----------
# TODO 5: 解包接住 roll_stats 的三个值并打印
# TODO 6: 解包接住 judge_stats 的两个值并打印
# TODO 7: 用 make_role 造至少 3 个角色，遍历打印
# TODO 8: 用 check_name 验 3 个名字（太短 / 太长 / 正常）
