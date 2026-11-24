# Day 58 · 队伍管理


class Role:
    """一个角色。血量永远夹在 0 和 max_hp 之间。"""

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
        """回血，返回实际回复量。倒下的治不了。"""
        if not self.alive:
            return 0
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before

    def status(self):
        state = "存活" if self.alive else "倒下"
        return f"{self.name}  HP {self.hp}/{self.max_hp}  ATK {self.atk}  [{state}]"


class Team:
    """一支队伍。成员是一堆 Role 对象。"""

    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, role):
        """加一个成员，返回现在的人数。"""
        self.members.append(role)
        return len(self.members)

    def size(self):
        """队伍人数。"""
        return len(self.members)

    def find(self, name):
        """按名字找成员。找不到返回 None。"""
        for m in self.members:
            if m.name == name:
                return m
        return None

    def remove(self, name):
        """按名字移除成员，返回是否成功。"""
        member = self.find(name)
        if member is None:
            return False
        self.members.remove(member)
        return True

    def total_hp(self):
        """全队总血量。"""
        total = 0
        for m in self.members:
            total += m.hp
        return total

    def avg_atk(self):
        """平均攻击力。空队返回 0。"""
        if self.size() == 0:
            return 0
        total = 0
        for m in self.members:
            total += m.atk
        return round(total / self.size(), 1)

    def alive_members(self):
        """还活着的成员。"""
        result = []
        for m in self.members:
            if m.is_alive():
                result.append(m)
        return result

    def is_wiped(self):
        """全灭了吗。"""
        return len(self.alive_members()) == 0

    def strongest(self):
        """攻击力最高的成员。空队返回 None。"""
        if self.size() == 0:
            return None
        best = self.members[0]
        for m in self.members:
            if m.atk > best.atk:
                best = m
        return best

    def heal_all(self, amount):
        """全队加血，返回总回复量。具体怎么加交给每个成员自己。"""
        total = 0
        for m in self.members:
            total += m.heal(amount)
        return total

    def damage_all(self, amount):
        """全队受伤，返回总扣血量。"""
        total = 0
        for m in self.members:
            total += m.take_damage(amount)
        return total

    def report(self):
        """打印完整的队伍报告。"""
        print(f"  【{self.name}】{self.size()} 人 · "
              f"存活 {len(self.alive_members())} 人")
        print(f"  总血量 {self.total_hp()}  平均攻击 {self.avg_atk()}")
        for m in self.members:
            print(f"    {m.status()}")


# ---------- 主流程 ----------
print("👥 === 队伍管理 === 👥")

team = Team("樱之队")
team.add(Role("星野樱", 340, 88))
team.add(Role("月见琉璃", 280, 95))
team.add(Role("天野灯", 120, 72))
team.add(Role("水城凛", 250, 110))

print("\n--- 初始状态 ---")
team.report()

print("\n--- 敌人释放全体魔法（150 点）---")
dealt = team.damage_all(150)
print(f"  全队共承受 {dealt} 点伤害")
team.report()

print(f"\n  存活 {len(team.alive_members())} 人，全灭了吗：{team.is_wiped()}")

print("\n--- 全体治疗 100 点 ---")
healed = team.heal_all(100)
print(f"  全队共回复 {healed} 点")
team.report()

print("\n--- 查找成员 ---")
found = team.find("水城凛")
print(f"  找水城凛：{found.status() if found else '没找到'}")
print(f"  找路人甲：{team.find('路人甲')}")

print("\n--- 移除成员 ---")
print(f"  移除天野灯：{team.remove('天野灯')}")
print(f"  移除路人甲：{team.remove('路人甲')}")
print(f"  现在剩 {team.size()} 人")

best = team.strongest()
print(f"\n最强成员：{best.name}（ATK {best.atk}）")
