# Day 60 · 技能系统


class Role:
    """所有职业的基础。普通攻击。"""

    def __init__(self, name, hp=100, atk=30, mp=100):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.mp = mp
        self.alive = True

    def take_damage(self, amount):
        """受伤，返回实际扣掉的血。子类不要重写这个。"""
        before = self.hp
        self.hp = max(0, self.hp - amount)
        self.alive = self.hp > 0
        return before - self.hp

    def status(self):
        """状态文字。子类不要重写这个。"""
        state = "存活" if self.alive else "倒下"
        return f"{self.name}  HP {self.hp}/{self.max_hp}  MP {self.mp}  [{state}]"

    # TODO 1: attack(self, target) -> 造成 atk 点伤害，返回伤害值

    # TODO 2: skill_name(self) -> 返回 "普通攻击"


# TODO 3: class Warrior(Role)
#   attack: 用 super().attack(target) 拿到基础伤害，
#           再额外打出 atk // 2 点（记得也要 target.take_damage）
#           返回总伤害
#   skill_name: "狂暴重击"


# TODO 4: class Mage(Role)
#   attack: mp >= 20 时扣 20 蓝，伤害 = atk * 3
#           mp 不够时 return super().attack(target)
#   skill_name: 蓝够返回 "奥术飞弹"，不够返回 "法杖敲击"


# TODO 5: class Rogue(Role)
#   attack: 伤害 = int(atk * 2.5)
#   skill_name: "背刺"


# ---------- 主流程 ----------
# TODO 6: 造一个血厚的敌人和四个角色（含一个纯 Role）
# TODO 7: 用一个 for 循环让全员攻击，打印技能名和伤害
#         ⚠️ 主流程里不许出现 isinstance
# TODO 8: 把法师的 mp 调低，再打一次，验证退回普通攻击
# TODO 9: 打印类名和技能名的对照表
# TODO 10: 打印敌人剩余血量
