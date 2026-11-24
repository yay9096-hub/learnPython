# Day 56 · 会战斗的角色


class Role:
    """一个会战斗的角色。数据和本事都装在这里。"""

    def __init__(self, name, hp=100, mp=50, atk=30):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.mp = mp
        self.atk = atk
        self.level = 1
        self.alive = True

    def is_alive(self):
        """还活着吗。"""
        return self.hp > 0

    def take_damage(self, amount):
        """受到伤害，返回实际扣掉的血量。"""
        self.hp = self.hp - amount
        if not self.is_alive():
            self.alive = False
            print(f"     💀 {self.name} 倒下了")
        return amount

    def attack(self, target):
        """攻击另一个角色，返回造成的伤害。"""
        damage = self.atk
        print(f"     ⚔️ {self.name} 攻击 {target.name}，造成 {damage} 点")
        target.take_damage(damage)
        return damage

    def heal(self, amount):
        """回血，返回实际回复量。"""
        self.hp = self.hp + amount
        print(f"     💚 {self.name} 恢复了 {amount} 点血")
        return amount

    def level_up(self):
        """升级：等级+1，上限+20，攻击+5，并且回满血。"""
        self.level = self.level + 1
        self.max_hp = self.max_hp + 20
        self.atk = self.atk + 5
        self.hp = self.max_hp
        print(f"     ⬆️ {self.name} 升到了 {self.level} 级！")
        return self.level

    def status(self):
        """返回一行状态文字。"""
        state = "存活" if self.is_alive() else "倒下"
        return f"{self.name} Lv.{self.level}  HP {self.hp}/{self.max_hp}  ATK {self.atk}  [{state}]"


# ---------- 主流程 ----------
print("⚔️ === 战斗开始 === ⚔️")

hero = Role("星野樱", 200, 180, 55)
enemy = Role("暗影魔像", 180, 60, 40)

print("\n--- 初始状态 ---")
print("  " + hero.status())
print("  " + enemy.status())

round_no = 0
while hero.is_alive() and enemy.is_alive() and round_no < 6:
    round_no = round_no + 1
    print(f"\n--- 第 {round_no} 回合 ---")

    hero.attack(enemy)
    if not enemy.is_alive():
        break

    enemy.attack(hero)

    if round_no == 2:
        hero.heal(40)
    if round_no == 3:
        hero.level_up()

    print("  " + hero.status())
    print("  " + enemy.status())

print("\n=== 战斗结束 ===")
print("  " + hero.status())
print("  " + enemy.status())

if hero.is_alive() and not enemy.is_alive():
    print(f"\n🎉 {hero.name} 获胜！")
elif enemy.is_alive() and not hero.is_alive():
    print(f"\n💀 {enemy.name} 获胜……")
else:
    print("\n🤝 打成平手")
