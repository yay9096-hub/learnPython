# Day 63 · 电子宠物
import json

SAVE = "宠物存档.json"


def clamp(value, low=0, high=100):
    """把值夹在 low..high 之间。"""
    return max(low, min(value, high))


class Pet:
    """一只电子宠物。"""

    def __init__(self, name, species="史莱姆"):
        self.name = name
        self.species = species
        self.hunger = 50
        self.energy = 50
        self.mood = 50
        self.age = 0
        self.alive = True

    # TODO 1: feed(self, amount=20) -> 饥饿 -amount、心情 +5，都夹取
    #   返回实际减少的饥饿值

    # TODO 2: sleep(self, hours=1) -> 精力 +hours*20、饥饿 +hours*10、年龄 +hours

    # TODO 3: play(self, cost=15) -> 精力 < 20 返回 False 并提示
    #   否则精力 -cost、心情 +15、饥饿 +10，返回 True

    # TODO 4: tick(self) -> 饥饿 +8、精力 -5、年龄 +1
    #   饥饿满 100 时心情 -20
    #   心情和精力都为 0 时 alive = False

    # TODO 5: is_hungry(self) -> 饥饿 > 70

    # TODO 6: stage(self) -> age<10 幼年 / <30 少年 / 否则成年

    # TODO 7: to_dict(self) -> 转成字典

    # TODO 8: from_dict(cls, data) -> 类方法，从字典造回来
    #   记得写 @classmethod

    # TODO 9: __str__(self) -> 一行状态，含名字、阶段、三条状态条


# TODO 10: save_pet(filename, pet)
# TODO 11: load_pet(filename) -> Pet 对象 / None


# ---------- 主流程 ----------
# TODO 12: load_pet，没有就新建
# TODO 13: 演示 feed / sleep / play，每次打印状态
# TODO 14: 演示精力不足时 play 失败
# TODO 15: 循环 tick 至少 5 小时，每小时打印
# TODO 16: 打印成长阶段
# TODO 17: 问玩家做什么并执行
# TODO 18: 存档，再读回来验证
