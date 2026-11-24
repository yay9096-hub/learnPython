# Day 36 · 战斗系统 2.0


def show_line(char, width):
    """打印 width 个 char 组成的分隔线。"""
    print(char * width)


def show_role(name, hp, atk):
    """打印一行角色信息，附带血条。"""
    bar = "█" * (hp // 20)
    print(f"  {name}  HP {hp} {bar}  ATK {atk}")


def deal_damage(attacker, atk, defense):
    """按「攻击力 - 防御力」算伤害，最低保底 1 点。"""
    damage = atk - defense
    if damage < 1:
        damage = 1
    print(f"  {attacker} 造成了 {damage} 点伤害！")


def show_team(team):
    """打印整支队伍。"""
    print(f"  队伍共 {len(team)} 人：")
    for name in team:
        print(f"    · {name}")


# ---------- 主流程 ----------
show_line("=", 32)
print("        ⚔️  战 斗 记 录  ⚔️")
show_line("=", 32)

show_role("星野樱", 340, 88)
show_role("暗影魔像", 500, 66)

show_line("─", 32)

deal_damage("星野樱", 88, 25)
deal_damage("暗影魔像", 66, 40)
deal_damage("小史莱姆", 10, 99)

show_line("★", 20)

show_team(["星野樱", "月见琉璃", "天野灯", "水城凛"])

show_line("=", 32)
