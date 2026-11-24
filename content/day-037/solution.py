# Day 37 · 骰子判定系统
import random


def roll(sides):
    """掷一个 sides 面的骰子，返回点数。"""
    return random.randint(1, sides)


def deal_damage(atk, defense):
    """按「攻击 - 防御」算伤害，最低保底 1 点。"""
    return max(atk - defense, 1)


def is_alive(hp):
    """血量大于 0 就还活着。"""
    return hp > 0


def grade(score):
    """把分数转成等第。"""
    if score >= 90:
        return "优秀"
    if score >= 60:
        return "及格"
    return "再努力一下"


def battle_report(name, hp):
    """生成一句战报文字。"""
    status = "存活" if is_alive(hp) else "倒下"
    return f"【战报】{name} 当前 HP {hp}，状态：{status}"


# ---------- 主流程 ----------
print("🎲 === 掷骰阶段 === 🎲")
a = roll(6)
b = roll(6)
c = roll(20)
print(f"  三次点数：{a} + {b} + {c} = {a + b + c}")

print("\n⚔️ === 战斗阶段 === ⚔️")
enemy_hp = 500
for atk in [88, 110, 95]:
    dmg = deal_damage(atk, 25)
    enemy_hp = enemy_hp - dmg
    print(f"  造成 {dmg} 点伤害，敌人剩余 {enemy_hp} 血")

print(f"  敌人还活着吗？{is_alive(enemy_hp)}")

print("\n📊 === 评级阶段 === 📊")
for score in [95, 72, 30]:
    print(f"  {score} 分 → {grade(score)}")

print()
print(battle_report("星野樱", 340))
print(battle_report("暗影魔像", enemy_hp))
