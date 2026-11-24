"""战斗伤害计算模块 —— Day 42 重构练习。

原始版本能跑，但函数名和变量名都是单字母，数字全是硬编码。
这一版逻辑完全没改，只是整理成了看得懂的样子。
"""

MIN_DAMAGE = 1
MAX_DAMAGE = 999
CRIT_RATE = 1.5
HEALTHY_HP = 400
WOUNDED_HP = 150
TOTAL_ROUNDS = 3


def deal_damage(atk, defense):
    """按「攻击力 - 防御力」算伤害，并夹在合法范围内。"""
    damage = atk - defense
    if damage < MIN_DAMAGE:
        damage = MIN_DAMAGE
    if damage > MAX_DAMAGE:
        damage = MAX_DAMAGE
    return damage


def deal_crit_damage(atk, defense):
    """暴击伤害 = 普通伤害 × 暴击倍率，保留一位小数。"""
    return round(deal_damage(atk, defense) * CRIT_RATE, 1)


def is_alive(hp):
    """血量大于 0 就还活着。"""
    return hp > 0


def describe_status(hp):
    """按血量返回状态描述：健康 / 受伤 / 危险。"""
    if hp > HEALTHY_HP:
        return "健康"
    if hp > WOUNDED_HP:
        return "受伤"
    return "危险"


def show_round(round_no, damage, enemy_hp):
    """播报一个回合的战况。"""
    print(f"  第 {round_no} 回合：造成 {damage} 点，敌人剩 {enemy_hp}")


def run_battle(atk, enemy_hp, enemy_defense):
    """打完固定回合数，返回敌人剩余血量。"""
    for round_index in range(TOTAL_ROUNDS):
        damage = deal_damage(atk, enemy_defense)
        enemy_hp = enemy_hp - damage
        show_round(round_index + 1, damage, enemy_hp)
    return enemy_hp


# ---------- 主流程 ----------
print("=== 战斗开始 ===")
print(f"普通伤害：{deal_damage(88, 25)}")
print(f"暴击伤害：{deal_crit_damage(88, 25)}")
print(f"最低保底：{deal_damage(10, 99)}")

remaining_hp = run_battle(88, 500, 25)
print(f"敌人剩余：{remaining_hp}")
print(f"还活着吗：{is_alive(remaining_hp)}")
print(f"状态：{describe_status(remaining_hp)}")
