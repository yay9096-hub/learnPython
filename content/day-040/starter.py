# Day 40 · 血量管理实验室
# 今天的目标是「亲眼看见」三种行为的差别


# TODO 1: damage_wrong(hp, dmg)
#   内部写 hp = hp - dmg，然后 print 一下，但【不要 return】


# TODO 2: damage_right(hp, dmg)
#   直接 return hp - dmg


# TODO 3: damage_dict(role, dmg)
#   改 role["hp"]，不用 return


# TODO 4: heal_team(team, amount)
#   传进来一个角色字典的列表，给每人加血，不用 return


# TODO 5: rename_wrong(name)
#   内部 name = "新名字"，演示字符串改不动


# ---------- 主流程 ----------
# TODO 6: 三种扣血各演示一次，每次打印调用【前】和【后】的血量
# TODO 7: heal_team 给至少 3 人的队伍加血，前后各打印一次
# TODO 8: rename_wrong 演示改不动
# TODO 9: 打印一句你自己的结论（要包含 return 这个词）
