# Day 61 · 好用的类


class Role:
    """一个角色。装上特殊方法之后用起来像内置类型。"""

    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.atk = atk

    def __str__(self):
        """print(角色) 时显示的样子。"""
        return f"【{self.name}】HP {self.hp}/{self.max_hp}  ATK {self.atk}"

    def __repr__(self):
        """调试时显示的样子，看着像能重新造出这个对象。"""
        return f"Role({self.name!r}, {self.hp}, {self.atk})"

    def __eq__(self, other):
        """名字一样就算同一个角色。"""
        if not isinstance(other, Role):
            return False
        return self.name == other.name

    def __lt__(self, other):
        """比大小的规则：按攻击力。"""
        return self.atk < other.atk


class Team:
    """一支队伍。支持 len() 和 in。"""

    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, role):
        """加一个成员。"""
        self.members.append(role)
        return len(self.members)

    def __str__(self):
        return f"《{self.name}》共 {len(self.members)} 人"

    def __len__(self):
        return len(self.members)

    def __contains__(self, name):
        """支持「名字 in 队伍」。"""
        for m in self.members:
            if m.name == name:
                return True
        return False


# ---------- 主流程 ----------
print("🎴 === 好用的类 === 🎴")

sakura = Role("星野樱", 340, 88)
ruri = Role("月见琉璃", 280, 95)
rin = Role("水城凛", 250, 110)
akari = Role("天野灯", 310, 72)

print("\n--- print(对象) ---")
print(sakura)
print(f"用 f-string 也一样：{ruri}")

roles = [sakura, ruri, rin]
print("\n--- 打印列表用的是 __repr__ ---")
print(roles)

print("\n--- 相等判断 ---")
same_name = Role("星野樱", 100, 20)
print(f"  同名不同血：{sakura == same_name}")
print(f"  不同名：{sakura == ruri}")
print(f"  跟字符串比：{sakura == '星野樱'}")

print("\n--- in 也变聪明了 ---")
print(f"  星野樱在列表里吗：{Role('星野樱') in roles}")
print(f"  路人甲在列表里吗：{Role('路人甲') in roles}")

print("\n--- 不写 key= 也能排序 ---")
ordered = sorted(roles)
for r in ordered:
    print(f"  {r}")
print(f"  最强：{max(roles).name}")
print(f"  最弱：{min(roles).name}")

print("\n--- 队伍的 len 和 in ---")
team = Team("樱之队")
team.add(sakura)
team.add(ruri)
team.add(akari)

print(f"  {team}")
print(f"  len(team) = {len(team)}")
print(f"  星野樱在队里吗：{'星野樱' in team}")
print(f"  水城凛在队里吗：{'水城凛' in team}")

print("\n--- 空队伍的真假判断 ---")
empty = Team("空队")
if team:
    print(f"  {team.name} 有人")
if not empty:
    print(f"  {empty.name} 是空的（len 为 0 就算 False）")
