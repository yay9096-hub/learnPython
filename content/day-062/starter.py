# Day 62 · 卡牌对战
import random

SEED = 2026
MAX_ROUNDS = 30


# TODO 1: class Card
#   __init__(self, name, atk, hp, cost=1) -> 还要设 max_hp
#   is_alive(self)
#   take_damage(self, amount) -> 不低于 0，返回实际扣血
#   attack(self, other) -> 返回造成的伤害
#   __str__(self) -> "名字(攻/血)"
#   __repr__(self) -> 同上


# TODO 2: class MagicCard(Card)
#   __init__(self, name, atk, hp, cost=2) -> 调 super()
#   attack(self, other) -> 重写：用 super() 拿基础伤害，再补一次同样的伤害
#   __str__(self) -> 名字前加 ✨


# TODO 3: class Deck
#   __init__(self, name) -> name 和空的 cards
#   add(self, card)
#   __len__(self) / __str__(self)
#   alive_cards(self) -> 还活着的牌
#   front(self) -> 第一张活着的牌，全死返回 None
#   is_defeated(self) -> 全灭了吗
#   shuffle(self, seed=None) -> 给了 seed 就先 random.seed(seed)
#   total_atk(self) -> 存活卡牌的攻击力总和


# ---------- 主流程 ----------
# TODO 4: 造两副牌，每副至少 5 张，其中至少 2 张魔法卡
# TODO 5: 用固定 seed 洗牌，打印两副牌
# TODO 6: 回合循环：双方 front() 互相攻击
#         打印回合数、前排、伤害；有卡倒下要打印
#         一方 is_defeated() 就结束；加回合上限防死循环
# TODO 7: 打印双方剩余卡牌和胜负
