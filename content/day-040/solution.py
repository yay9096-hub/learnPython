# Day 40 · 血量管理实验室


def damage_wrong(hp, dmg):
    """错误示范：只改了局部变量，外面感觉不到。"""
    hp = hp - dmg
    print(f"    （函数内部看到的血量：{hp}）")


def damage_right(hp, dmg):
    """正确做法：把新血量交回去。"""
    return hp - dmg


def damage_dict(role, dmg):
    """字典是「可变对象」，改内容外面真的会变，不用 return。"""
    role["hp"] = role["hp"] - dmg


def heal_team(team, amount):
    """给整队人加血。列表和字典都是可变的，直接改就行。"""
    for member in team:
        member["hp"] = member["hp"] + amount


def rename_wrong(name):
    """错误示范：字符串也改不动外面的。"""
    name = "改过的名字"
    print(f"    （函数内部看到的名字：{name}）")


# ---------- 主流程 ----------
print("🕳 === 血量管理实验室 === 🕳")

print("\n① 不 return —— 改不动")
hp = 500
print(f"  调用前：{hp}")
damage_wrong(hp, 63)
print(f"  调用后：{hp}   ← 一点没变")

print("\n② 用 return 接住 —— 改得动")
hp = 500
print(f"  调用前：{hp}")
hp = damage_right(hp, 63)
print(f"  调用后：{hp}   ← 变了！")

print("\n③ 传字典 —— 不用 return 也改得动")
role = {"name": "星野樱", "hp": 500}
print(f"  调用前：{role['hp']}")
damage_dict(role, 63)
print(f"  调用后：{role['hp']}   ← 也变了！")

print("\n④ 整队加血")
team = [
    {"name": "星野樱", "hp": 340},
    {"name": "月见琉璃", "hp": 280},
    {"name": "天野灯", "hp": 310},
]
print("  加血前：")
for m in team:
    print(f"    {m['name']} {m['hp']}")

heal_team(team, 50)

print("  加血后：")
for m in team:
    print(f"    {m['name']} {m['hp']}")

print("\n⑤ 字符串也改不动")
name = "星野樱"
print(f"  调用前：{name}")
rename_wrong(name)
print(f"  调用后：{name}   ← 没变")

print("\n💡 我的结论：数字和文字要用 return 把结果交回来才算数，")
print("   列表和字典改内容就能直接生效。")
