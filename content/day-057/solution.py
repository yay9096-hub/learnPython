# Day 57 · 守规矩的角色类


class Role:
    """一个会自己守规矩的角色。

    不变量：任何时候都满足 0 <= hp <= max_hp，
    而且 alive 永远和 hp 保持一致。
    """

    def __init__(self, name, hp=100, atk=30):
        if hp <= 0:
            raise ValueError(f"初始血量必须大于 0（收到 {hp}）")
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk
        self.level = 1
        self.alive = True

    def take_damage(self, amount):
        """受伤。血量最低到 0，返回实际扣掉的血。"""
        if amount < 0:
            raise ValueError(f"伤害不能是负数（收到 {amount}）")
        before = self.hp
        self.hp = max(0, self.hp - amount)
        self.alive = self.hp > 0
        actual = before - self.hp
        if not self.alive:
            print(f"     💀 {self.name} 倒下了")
        return actual

    def heal(self, amount):
        """回血。最多回到满血，返回实际回复量。倒下的治不了。"""
        if amount < 0:
            raise ValueError(f"治疗量不能是负数（收到 {amount}）")
        if not self.alive:
            print(f"     ⚠️ {self.name} 已经倒下了，治不了")
            return 0
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before

    def attack(self, target):
        """攻击别人。自己倒下了就打不动，返回造成的伤害。"""
        if not self.alive:
            print(f"     ⚠️ {self.name} 已经倒下了，攻击不了")
            return 0
        print(f"     ⚔️ {self.name} 攻击 {target.name}，造成 {self.atk} 点")
        target.take_damage(self.atk)
        return self.atk

    def revive(self, ratio=0.5):
        """复活。只对倒下的角色有效，复活后至少 1 血。"""
        if self.alive:
            print(f"     ⚠️ {self.name} 还活着，不用复活")
            return False
        self.hp = max(1, int(self.max_hp * ratio))
        self.alive = True
        print(f"     ✨ {self.name} 复活了！HP {self.hp}/{self.max_hp}")
        return True

    def level_up(self):
        """升级：等级+1、上限+20、攻击+5，并且回满血。"""
        self.level = self.level + 1
        self.max_hp = self.max_hp + 20
        self.atk = self.atk + 5
        self.hp = self.max_hp
        self.alive = True
        print(f"     ⬆️ {self.name} 升到了 {self.level} 级！")
        return self.level

    def hp_percent(self):
        """血量百分比，0~100 的整数。"""
        return int(self.hp / self.max_hp * 100)

    def status(self):
        """返回一行状态文字，带血条。"""
        percent = self.hp_percent()
        filled = percent // 10
        bar = "█" * filled + "░" * (10 - filled)
        state = "存活" if self.alive else "倒下"
        return (f"{self.name} Lv.{self.level}  {bar} "
                f"{self.hp}/{self.max_hp}（{percent}%）  [{state}]")


# ---------- 主流程 ----------
print("🛡 === 守规矩的角色 === 🛡")

hero = Role("星野樱", 200, 55)
dummy = Role("木桩", 100, 10)

print("\n--- 初始状态 ---")
print("  " + hero.status())

print("\n--- 过量伤害（血量该停在 0）---")
actual = hero.take_damage(999)
print(f"  想打 999，实际扣了 {actual} 点")
print("  " + hero.status())

print("\n--- 倒下之后 ---")
print(f"  治疗回复了 {hero.heal(50)} 点")
print(f"  攻击造成了 {hero.attack(dummy)} 点")

print("\n--- 复活 ---")
hero.revive()
print("  " + hero.status())

print("\n--- 过量治疗（该停在满血）---")
healed = hero.heal(9999)
print(f"  想治 9999，实际只回了 {healed} 点")
print("  " + hero.status())

print("\n--- 负数参数会被挡住 ---")
try:
    hero.take_damage(-100)
except ValueError as e:
    print(f"  ✓ 被拦下了：{e}")

try:
    hero.heal(-50)
except ValueError as e:
    print(f"  ✓ 被拦下了：{e}")

try:
    Role("非法角色", 0)
except ValueError as e:
    print(f"  ✓ 被拦下了：{e}")

print("\n--- 升级 ---")
hero.level_up()
print("  " + hero.status())

print("\n✅ 不变量全程守住：血量永远在 0 和 max_hp 之间")
