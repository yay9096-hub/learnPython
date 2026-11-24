# Day 58 · 队伍管理
# Role 已经给你了（Day 57 的简化版），今天只写 Team


class Role:
    """一个角色。血量永远夹在 0 和 max_hp 之间。"""

    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.alive = True

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        """受伤，返回实际扣掉的血。"""
        before = self.hp
        self.hp = max(0, self.hp - amount)
        self.alive = self.hp > 0
        return before - self.hp

    def heal(self, amount):
        """回血，返回实际回复量。倒下的治不了。"""
        if not self.alive:
            return 0
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before

    def status(self):
        state = "存活" if self.alive else "倒下"
        return f"{self.name}  HP {self.hp}/{self.max_hp}  ATK {self.atk}  [{state}]"


class Team:
    """一支队伍。"""

    # TODO 1: __init__(self, name) -> 属性 name 和空的 members

    # TODO 2: add(self, role) -> 加成员，返回人数

    # TODO 3: size(self) -> 人数

    # TODO 4: find(self, name) -> 找到返回成员，找不到返回 None

    # TODO 5: remove(self, name) -> 移除，返回 True/False（要复用 find）

    # TODO 6: total_hp(self) -> 全队总血量

    # TODO 7: avg_atk(self) -> 平均攻击（保留 1 位），空队返回 0

    # TODO 8: alive_members(self) -> 活着的成员列表

    # TODO 9: is_wiped(self) -> 全灭了吗

    # TODO 10: strongest(self) -> 攻击最高的成员，空队返回 None

    # TODO 11: heal_all(self, amount) -> 全队加血，返回总回复量

    # TODO 12: damage_all(self, amount) -> 全队受伤，返回总扣血量

    # TODO 13: report(self) -> 打印完整队伍报告


# ---------- 主流程 ----------
# TODO 14: 造一支至少 4 人的队伍，打印报告
# TODO 15: damage_all 打一次全体伤害，让至少一人倒下
# TODO 16: 打印存活人数和 is_wiped()
# TODO 17: heal_all 治一次，打印实际总回复量
# TODO 18: find 查存在的和不存在的
# TODO 19: remove 移除一个，再打印人数
# TODO 20: 打印最强成员
