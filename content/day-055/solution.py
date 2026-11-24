# Day 55 · 角色类


class Role:
    """一个游戏角色。除了名字，其余属性都有默认值。"""

    def __init__(self, name, hp=100, mp=50, atk=30, element="无"):
        self.name = name
        self.hp = hp
        self.max_hp = hp        # 满血值记下来，以后治疗要用
        self.mp = mp
        self.atk = atk
        self.element = element
        self.alive = True


# ---------- 主流程 ----------
print("🏗 === 角色类 === 🏗")

passerby = Role("路人甲")
sakura = Role("星野樱", 340, 180, 88, "火")
ruri = Role("月见琉璃", element="水", atk=95)
rin = Role("水城凛", 250, 90, 110, "水")

team = [passerby, sakura, ruri, rin]

print("\n--- 全员名册 ---")
for r in team:
    print(f"  {r.name}  HP {r.hp}/{r.max_hp}  ATK {r.atk}  [{r.element}]")

total = sum(r.hp for r in team)
print(f"\n队伍总血量：{total}")

strongest = max(team, key=lambda r: r.atk)
print(f"攻击力最强：{strongest.name}（{strongest.atk}）")

print("\n--- 星野樱受到 100 点伤害 ---")
sakura.hp = sakura.hp - 100

for r in team:
    print(f"  {r.name}  HP {r.hp}/{r.max_hp}")

print("\n只有星野樱掉血了 —— 每个实例的属性都是独立的 ✨")
