# Day 41 · 队伍管理函数库
TEAM = [
    {"name": "星野樱",   "hp": 340, "atk": 88,  "element": "火"},
    {"name": "月见琉璃", "hp": 280, "atk": 95,  "element": "水"},
    {"name": "天野灯",   "hp": 310, "atk": 72,  "element": "风"},
    {"name": "水城凛",   "hp": 250, "atk": 110, "element": "水"},
    {"name": "风见幽香", "hp": 360, "atk": 90,  "element": "火"},
]


# ================= 算的部分（不打印） =================

def total_hp(team):
    """返回队伍总血量。空队伍返回 0。"""
    total = 0
    for m in team:
        total += m["hp"]
    return total


def avg_atk(team):
    """返回平均攻击力（保留 1 位）。空队伍返回 0，避免除以零。"""
    if len(team) == 0:
        return 0
    total = 0
    for m in team:
        total += m["atk"]
    return round(total / len(team), 1)


def strongest(team):
    """返回攻击力最高的成员。空队伍返回 None。"""
    if len(team) == 0:
        return None
    best = team[0]
    for m in team:
        if m["atk"] > best["atk"]:
            best = m
    return best


def filter_by_element(team, element):
    """挑出指定属性的成员，返回新列表。"""
    result = []
    for m in team:
        if m["element"] == element:
            result.append(m)
    return result


def filter_by_atk(team, min_atk):
    """挑出攻击力达到 min_atk 的成员，返回新列表。"""
    result = []
    for m in team:
        if m["atk"] >= min_atk:
            result.append(m)
    return result


def find_member(team, name):
    """按名字找人。找不到返回 None。"""
    for m in team:
        if m["name"] == name:
            return m
    return None


# ================= 打印的部分 =================

def show_team(team):
    """逐行打印队伍成员。"""
    if len(team) == 0:
        print("  （没有成员）")
        return
    for m in team:
        print(f"  {m['name']}  HP {m['hp']}  ATK {m['atk']}  {m['element']}属性")


def show_report(team):
    """把各个统计零件拼成一份报告。"""
    print(f"  人数：{len(team)}")
    print(f"  总血量：{total_hp(team)}")
    print(f"  平均攻击：{avg_atk(team)}")
    top = strongest(team)
    if top is None:
        print("  最强：（队伍是空的）")
    else:
        print(f"  最强：{top['name']}（{top['atk']}）")


# ================= 主流程 =================
print("🧰 === 队伍管理系统 === 🧰")

print("\n--- 全队名册 ---")
show_team(TEAM)

print("\n--- 队伍报告 ---")
show_report(TEAM)

print("\n--- 火属性成员 ---")
show_team(filter_by_element(TEAM, "火"))

print("\n--- 攻击力 90 以上 ---")
show_team(filter_by_atk(TEAM, 90))

who = input("\n想查谁？").strip()
found = find_member(TEAM, who)
if found is None:
    print(f"  查无此人：「{who}」")
else:
    print(f"  找到了：{found['name']} HP {found['hp']} ATK {found['atk']}")

print("\n--- 空队伍测试（不应该崩）---")
show_report([])
