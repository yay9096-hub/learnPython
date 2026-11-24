# Day 35 · 战斗播报零件库


def show_line():
    """打印一条分隔线，宽度 28。"""
    print("─" * 28)


def show_title():
    """打印带上下分隔线的战斗标题。"""
    show_line()
    print("      ⚔️  战 斗 开 始  ⚔️")
    show_line()


def show_hero():
    """打印我方角色信息。"""
    print("【我方】星野樱 · 樱花剑姬")
    print("  HP 340 / 340    ATK 88")


def show_enemy():
    """打印敌方角色信息。"""
    print("【敌方】暗影魔像")
    print("  HP 500 / 500    ATK 66")


def show_victory():
    """打印胜利画面。"""
    show_line()
    for i in range(3):
        print("✨" * (i + 1) + " VICTORY " + "✨" * (i + 1))
    print("  获得经验 120 · 金币 45")
    show_line()


# ---------- 主流程 ----------
show_title()
show_hero()
show_line()
show_enemy()
show_victory()
