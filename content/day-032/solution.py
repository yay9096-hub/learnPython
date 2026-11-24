# Day 32 · 好友分析
mine = ["星野樱", "月见琉璃", "天野灯", "水城凛", "月见琉璃", "星野樱"]
hers = ["月见琉璃", "水城凛", "夜刀神澪", "风见幽香"]
his  = ["天野灯", "水城凛", "雾岛遥"]

print("🔗 === 好友关系分析 === 🔗")

my_set = set(mine)
her_set = set(hers)
his_set = set(his)

print(f"我的好友列表原有 {len(mine)} 条，去重后 {len(my_set)} 人")
print(f"我的好友：{sorted(my_set)}")
print("─" * 40)

common = my_set & her_set
print(f"我和她的共同好友（{len(common)} 人）：{sorted(common)}")

everyone = my_set | her_set
print(f"我俩认识的所有人（{len(everyone)} 人）：{sorted(everyone)}")

only_mine = my_set - her_set
print(f"只有我认识的（{len(only_mine)} 人）：{sorted(only_mine)}")

only_hers = her_set - my_set
print(f"只有她认识的（{len(only_hers)} 人）：{sorted(only_hers)}")

print("─" * 40)
all_common = my_set & her_set & his_set
print(f"三人共同好友（{len(all_common)} 人）：{sorted(all_common)}")
