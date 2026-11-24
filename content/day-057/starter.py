# Day 57 · 守规矩的角色类
# 不变量：任何时候都必须满足 0 <= hp <= max_hp


class Role:
    """一个会自己守规矩的角色。"""

    def __init__(self, name, hp=100, atk=30):
        # TODO 1: hp <= 0 要 raise ValueError
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.level = 1
        self.alive = True

    # TODO 2: take_damage(self, amount)
    #   负数 -> raise ValueError
    #   血量不低于 0（用 max(0, ...)）
    #   同步 alive
    #   返回实际扣掉的血

    # TODO 3: heal(self, amount)
    #   负数 -> raise ValueError
    #   不超过 max_hp（用 min(...)）
    #   倒下的不能治，返回 0
    #   返回实际回复量（先记 before，改完算差值）

    # TODO 4: attack(self, target)
    #   自己倒下了不能攻击，返回 0
    #   返回造成的伤害

    # TODO 5: revive(self, ratio=0.5)
    #   只对倒下的有效
    #   复活后至少 1 血（用 max(1, ...)）
    #   返回 True / False

    # TODO 6: level_up(self) -> 等级+1、max_hp+20、atk+5、回满血，返回新等级

    # TODO 7: hp_percent(self) -> 0~100 的整数

    # TODO 8: status(self) -> 返回一行状态，含血条


# ---------- 主流程 ----------
# TODO 9: 造角色，打印初始状态
# TODO 10: 演示过量伤害（停在 0）
# TODO 11: 演示复活
# TODO 12: 演示过量治疗（停在满血，打印实际回了多少）
# TODO 13: 演示倒下后治疗无效、倒下后攻击无效
# TODO 14: 演示负数参数被 raise 挡住（try 接住）
# TODO 15: level_up 升一级
