# Day 56 · 会战斗的角色


class Role:
    """一个会战斗的角色。"""

    def __init__(self, name, hp=100, mp=50, atk=30):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.atk = atk
        self.level = 1
        self.alive = True

    # TODO 1: is_alive(self) -> True / False

    # TODO 2: take_damage(self, amount) -> 扣血，返回实际扣的血
    #   血量 <= 0 时把 alive 设为 False 并打印倒下

    # TODO 3: attack(self, target) -> 攻击别人，返回造成的伤害
    #   要调用 target.take_damage(...)

    # TODO 4: heal(self, amount) -> 回血，返回实际回了多少

    # TODO 5: level_up(self) -> 等级+1、max_hp+20、atk+5、回满血

    # TODO 6: status(self) -> 返回一行状态文字（不是 print）


# ---------- 主流程 ----------
# TODO 7: 造我方和敌方两个角色，打印初始状态
# TODO 8: 循环至少 3 回合互相攻击，每回合打印状态
# TODO 9: 中途用一次 heal、一次 level_up
# TODO 10: 用 is_alive 判断战斗是否继续
# TODO 11: 宣布谁赢了
