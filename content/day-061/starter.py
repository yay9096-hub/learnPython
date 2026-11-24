# Day 61 · 好用的类


class Role:
    """一个角色。"""

    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk

    # TODO 1: __str__(self) -> 一行漂亮的卡片文字（名字/HP/ATK）

    # TODO 2: __repr__(self) -> Role('名字', 血量, 攻击) 这种样子

    # TODO 3: __eq__(self, other) -> 名字相同就相等
    #   ⚠️ 先用 isinstance 检查 other 是不是 Role

    # TODO 4: __lt__(self, other) -> 按攻击力比大小


class Team:
    """一支队伍。"""

    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, role):
        """加一个成员。"""
        self.members.append(role)
        return len(self.members)

    # TODO 5: __str__(self) -> 队伍名和人数

    # TODO 6: __len__(self) -> 成员数

    # TODO 7: __contains__(self, name) -> 按名字判断在不在队里


# ---------- 主流程 ----------
# TODO 8: 直接 print(角色)（不许用 .status()）
# TODO 9: 打印一个装着角色的列表，展示 __repr__
# TODO 10: 演示 ==（同名不同血相等、跟字符串比 False）
# TODO 11: 演示 Role(...) in 角色列表
# TODO 12: 用 sorted() / max() / min() 排序，不写 key=
# TODO 13: 演示 len(team) 和 "名字" in team
# TODO 14: 演示 if team:（再造一个空队伍对比）
#   ⚠️ 主流程里不许出现 .members
