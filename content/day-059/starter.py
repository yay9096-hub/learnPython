# Day 59 · 三个职业


class Role:
    """所有职业的共同基础。"""

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
        """回血，返回实际回复量。"""
        if not self.alive:
            return 0
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before

    def status(self):
        state = "存活" if self.alive else "倒下"
        return f"{self.name}  HP {self.hp}/{self.max_hp}  ATK {self.atk}  [{state}]"


# TODO 1: class Warrior(Role)
#   __init__(self, name, hp=200, atk=40, armor=10)
#     第一句要 super().__init__(name, hp, atk)
#   real_damage(self, amount) -> max(1, amount - armor)
#   roar(self) -> 攻击力 +10，返回一句话


# TODO 2: class Mage(Role)
#   __init__(self, name, hp=120, atk=25, mp=100)
#     加 mp / max_mp
#   cast(self, target, cost=20) -> 魔法不够返回 0
#     够则扣 mp，对 target 造成 atk * 2 伤害，返回伤害值


# TODO 3: class Rogue(Role)
#   __init__(self, name, hp=140, atk=35, crit=2.0)
#   backstab(self, target) -> 造成 int(atk * crit) 伤害，返回伤害值


# ---------- 主流程 ----------
# TODO 4: 三个职业各造一个，装进列表
# TODO 5: 遍历打印职业名（type(m).__name__）和状态
# TODO 6: 演示 real_damage（大伤害 + 小伤害）
# TODO 7: 演示 roar 前后攻击力
# TODO 8: 演示 cast 魔法够 / 不够两种情况
# TODO 9: 演示 backstab
# TODO 10: 用 isinstance 证明战士也是 Role
# TODO 11: 统计各职业人数
