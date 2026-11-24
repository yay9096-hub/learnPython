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
        """受伤，返回实际扣掉的血。"""
        before = self.hp
        self.hp = max(0, self.hp - amount)
        self.alive = self.hp > 0
        return before - self.hp

    def status(self):
        """状态文字。"""
        state = "存活" if self.alive else "倒下"
        return f"{self.name}  HP {self.hp}/{self.max_hp}  MP {self.mp}  [{state}]"

    def attack(self, target):
        """普通攻击，造成 atk 点伤害。"""
        damage = self.atk
        target.take_damage(damage)
        return damage

    def skill_name(self):
        """技能名字。"""
        return "普通攻击"


class Warrior(Role):
    """战士。在普通攻击基础上追加一次重击。"""

    def attack(self, target):
        """先照常打一下，再追加 atk // 2 点。"""
        base = super().attack(target)
        bonus = self.atk // 2
        target.take_damage(bonus)
        return base + bonus

    def skill_name(self):
        return "狂暴重击"


class Mage(Role):
    """法师。魔法伤害三倍，但要花蓝；没蓝就退回普通攻击。"""

    COST = 20

    def attack(self, target):
        """够蓝就放魔法，不够就用法杖敲。"""
        if self.mp < self.COST:
            return super().attack(target)
        self.mp = self.mp - self.COST
        damage = self.atk * 3
        target.take_damage(damage)
        return damage

    def skill_name(self):
        if self.mp < self.COST:
            return "法杖敲击"
        return "奥术飞弹"


class Rogue(Role):
    """盗贼。背刺，伤害 2.5 倍。"""

    def attack(self, target):
        damage = int(self.atk * 2.5)
        target.take_damage(damage)
        return damage

    def skill_name(self):
        return "背刺"


# ---------- 主流程 ----------
print("✨ === 技能系统 === ✨")

boss = Role("暗影魔王", 2000, 50)

team = [
    Role("路人甲", 100, 30),
    Warrior("铁壁", 200, 40),
    Mage("月见琉璃", 120, 25),
    Rogue("影", 140, 35),
]

print("\n--- 全员出击 ---")
for m in team:
    damage = m.attack(boss)
    print(f"  {m.name} 使用「{m.skill_name()}」，造成 {damage} 点")

print(f"\n  {boss.name} 剩余 {boss.hp}/{boss.max_hp}")

print("\n--- 法师蓝不够了 ---")
mage = team[2]
mage.mp = 5
print(f"  当前 MP {mage.mp}，技能变成「{mage.skill_name()}」")
damage = mage.attack(boss)
print(f"  造成 {damage} 点（退回了普通攻击）")

print("\n--- 职业技能对照表 ---")
for m in team:
    print(f"  {type(m).__name__:<8} {m.name:<10} → {m.skill_name()}")

print(f"\n最终 {boss.name} 剩余 {boss.hp}/{boss.max_hp}")
