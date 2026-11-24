# Day 38 · 角色生成器


# TODO 1: create_role(name, hp=100, mp=50, atk=30, element="无", level=1)
#   返回一个字典，把这些都装进去（再加一个空的 "skills" 列表）


# TODO 2: show_role(role, width=20, char="█")
#   打印角色卡，血条用 char 画，总宽 width
#   血条长度可以用 int(role["hp"] / 400 * width)


# TODO 3: add_skill(role, skill, skills=None)
#   给角色加技能。⚠️ 默认值必须是 None，不能是 []
#   进函数后 if skills is None: skills = role["skills"]


# ---------- 主流程 ----------
# TODO 4: 只给名字造一个路人
# TODO 5: 全部参数造一个主角
# TODO 6: 用关键字参数只改 element 和 level
# TODO 7: 给某个角色加 2 个技能
# TODO 8: show_role 至少调 3 次，其中一次改 width 或 char
