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


class Warrior(Role):
    """战士。血厚，有护甲能减免伤害。"""

    def __init__(self, name, hp=200, atk=40, armor=10):
        super().__init__(name, hp, atk)
        self.armor = armor

    def real_damage(self, amount):
        """算上护甲之后实际受到的伤害，最低 1 点。"""
        return max(1, amount - self.armor)

    def roar(self):
        """怒吼，攻击力永久 +10。"""
        self.atk = self.atk + 10
        return f"{self.name} 发出怒吼！攻击力升到 {self.atk}"


class Mage(Role):
    """法师。血薄，但能放高伤害的魔法。"""

    def __init__(self, name, hp=120, atk=25, mp=100):
        super().__init__(name, hp, atk)
        self.mp = mp
        self.max_mp = mp

    def cast(self, target, cost=20):
        """施法。魔法不够就放不出来，返回造成的伤害。"""
        if self.mp < cost:
            print(f"     ⚠️ {self.name} 魔力不足（{self.mp}/{cost}）")
            return 0
        self.mp = self.mp - cost
        damage = self.atk * 2
        target.take_damage(damage)
        print(f"     ✨ {self.name} 施法，对 {target.name} 造成 {damage} 点（剩余 MP {self.mp}）")
        return damage


class Rogue(Role):
    """盗贼。攻击不高，但背刺伤害翻倍。"""

    def __init__(self, name, hp=140, atk=35, crit=2.0):
        super().__init__(name, hp, atk)
        self.crit = crit

    def backstab(self, target):
        """背刺，造成暴击伤害。"""
        damage = int(self.atk * self.crit)
        target.take_damage(damage)
        print(f"     🗡 {self.name} 背刺 {target.name}，造成 {damage} 点")
        return damage


# ---------- 主流程 ----------
print("🧙 === 三个职业 === 🧙")

warrior = Warrior("铁壁")
mage = Mage("月见琉璃")
rogue = Rogue("影")
dummy = Role("训练木桩", 999)

team = [warrior, mage, rogue]

print("\n--- 队伍名册 ---")
for m in team:
    print(f"  [{type(m).__name__}] {m.status()}")

print("\n--- 战士的护甲 ---")
print(f"  挨 50 点，实际受到 {warrior.real_damage(50)} 点")
print(f"  挨 5 点，实际受到 {warrior.real_damage(5)} 点（护甲减免不会变负）")

print("\n--- 战士怒吼 ---")
print(f"  怒吼前攻击力 {warrior.atk}")
print(f"  {warrior.roar()}")

print("\n--- 法师施法 ---")
mage.cast(dummy)
mage.cast(dummy)
mage.mp = 5
mage.cast(dummy)

print("\n--- 盗贼背刺 ---")
rogue.backstab(dummy)
print(f"  木桩剩余 {dummy.hp}")

print("\n--- 类型判断 ---")
print(f"  战士是 Warrior 吗：{isinstance(warrior, Warrior)}")
print(f"  战士也是 Role 吗：{isinstance(warrior, Role)}")
print(f"  战士是 Mage 吗：{isinstance(warrior, Mage)}")

print("\n--- 职业统计 ---")
all_members = [warrior, mage, rogue, Warrior("盾姬"), Mage("星见")]
counts = {}
for m in all_members:
    kind = type(m).__name__
    counts[kind] = counts.get(kind, 0) + 1

for kind, n in counts.items():
    print(f"  {kind}：{n} 人")
