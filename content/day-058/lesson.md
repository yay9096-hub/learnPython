# Day 58 · 一整支队伍 👥

> 「昨天的 `Role` 已经很结实了。
> 但『队伍』这件事还散着 —— 一个列表 + 一堆外部函数。
>
> 今天再造一个 `Team` 类。你会看到一件很自然的事：
> **一个类的属性，可以是一堆别的类的对象。**」

---

## 📌 知识卡 1 · 类的属性可以是列表

```python runnable Team 里装着 Role
class Role:
    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.alive = True


class Team:
    """一支队伍。"""

    def __init__(self, name):
        self.name = name
        self.members = []          # ← 一个装 Role 对象的列表


team = Team("樱之队")
print(team.name)
print(team.members)
print(len(team.members))
```

`self.members = []` —— **属性可以是任何东西**，包括一个列表。

---

## 📌 知识卡 2 · 加成员的方法

```python runnable add 方法
class Role:
    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.hp = hp
        self.atk = atk


class Team:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, role):
        """加一个成员。返回队伍现在有几人。"""
        self.members.append(role)
        return len(self.members)

    def size(self):
        """队伍人数。"""
        return len(self.members)


team = Team("樱之队")
team.add(Role("星野樱", 340, 88))
team.add(Role("月见琉璃", 280, 95))

print(f"{team.name} 共 {team.size()} 人")
for m in team.members:
    print(f"  {m.name}  HP {m.hp}")
```

看 `team.add(Role("星野樱", 340, 88))` ——
**造一个 Role，直接塞进 Team**。这叫**组合**（composition）。

> 🧠 现实里也是这个结构：
> 一支球队「有」一堆球员，一辆车「有」四个轮子。
> **「A 有一堆 B」→ A 的属性里放 B 的列表。**

---

## 📌 知识卡 3 · 委托：Team 的方法调成员的方法 ⭐

```python runnable 全队加血
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.max_hp = hp
        self.hp = hp

    def heal(self, amount):
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before


class Team:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, role):
        self.members.append(role)

    def heal_all(self, amount):
        """给全队加血，返回总共回了多少。"""
        total = 0
        for m in self.members:
            total += m.heal(amount)      # ← 调用成员自己的方法
        return total


team = Team("樱之队")
team.add(Role("星野樱", 340))
team.add(Role("月见琉璃", 280))

team.members[0].hp = 200
team.members[1].hp = 280

healed = team.heal_all(100)
print(f"全队共回复 {healed} 点")
for m in team.members:
    print(f"  {m.name}  HP {m.hp}/{m.max_hp}")
```

`Team.heal_all` 自己**不知道怎么加血** —— 它把这件事**交给每个 Role 自己做**。

这叫**委托**（delegation）。好处是：治疗的规则（不超上限、倒下不能治）
只写在 `Role` 里一处，`Team` 完全不用操心。

---

## 📌 知识卡 4 · 统计和筛选，还是老套路

```python runnable Team 的统计方法
class Role:
    def __init__(self, name, hp=100, atk=30):
        self.name = name
        self.hp = hp
        self.atk = atk

    def is_alive(self):
        return self.hp > 0


class Team:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, role):
        self.members.append(role)

    def total_hp(self):
        """全队总血量。"""
        return sum(m.hp for m in self.members)

    def alive_members(self):
        """还活着的成员，返回一个新列表。"""
        return [m for m in self.members if m.is_alive()]

    def is_wiped(self):
        """全灭了吗。"""
        return len(self.alive_members()) == 0

    def strongest(self):
        """攻击力最高的成员。空队返回 None。"""
        if not self.members:
            return None
        return max(self.members, key=lambda m: m.atk)


team = Team("樱之队")
team.add(Role("星野樱", 340, 88))
team.add(Role("月见琉璃", 0, 95))
team.add(Role("天野灯", 310, 72))

print(f"总血量：{team.total_hp()}")
print(f"存活：{len(team.alive_members())} 人")
print(f"全灭了吗：{team.is_wiped()}")
print(f"最强：{team.strongest().name}")
```

**第三章、第四章学的全部统计本事，原样搬进方法里就行。**

注意 `team.strongest().name` —— 方法返回一个对象，可以**接着点**。

---

## 📌 知识卡 5 · 按名字找成员

```python runnable find 方法
class Role:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp


class Team:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, role):
        self.members.append(role)

    def find(self, name):
        """按名字找成员。找不到返回 None。"""
        for m in self.members:
            if m.name == name:
                return m
        return None

    def remove(self, name):
        """按名字移除成员。返回是否成功。"""
        member = self.find(name)
        if member is None:
            return False
        self.members.remove(member)
        return True


team = Team("樱之队")
team.add(Role("星野樱", 340))
team.add(Role("月见琉璃", 280))

found = team.find("星野樱")
print(found.name if found else "没找到")
print(team.find("路人甲"))

print(f"移除月见琉璃：{team.remove('月见琉璃')}")
print(f"移除路人甲：{team.remove('路人甲')}")
print(f"剩 {len(team.members)} 人")
```

`remove` 里调用了 `self.find(...)` —— **方法复用方法**，不用把查找逻辑写两遍。

---

## 📌 知识卡 6 · 谁该负责什么

| 职责 | 归谁 |
|---|---|
| 单个角色怎么扣血、怎么治疗 | **Role** |
| 一个角色活着没 | **Role** |
| 队伍有几个人、谁最强 | **Team** |
| 全队加血 | **Team**（但具体加血交给 Role） |
| 打印报告 | 主流程或 Team 的 `report()` |

> 🧠 一条实用原则：
> **只跟一个角色有关的事，写在 Role 里；
> 需要「看到全队」才能做的事，写在 Team 里。**

---

## 🛠 今天的任务 · 队伍管理

`Role` 类沿用 Day 57 的（starter 里给了简化版）。今天写 `Team`：

| 方法 | 说明 |
|---|---|
| `__init__(self, name)` | 属性 `name` 和空的 `members` |
| `add(self, role)` | 加成员，返回现在的人数 |
| `size(self)` | 人数 |
| `find(self, name)` | 按名字找，找不到返回 `None` |
| `remove(self, name)` | 按名字移除，返回 `True` / `False`。**要复用 `find`** |
| `total_hp(self)` | 全队总血量 |
| `avg_atk(self)` | 平均攻击力（保留 1 位）。**空队返回 0** |
| `alive_members(self)` | 活着的成员列表 |
| `is_wiped(self)` | 全灭了吗 |
| `strongest(self)` | 攻击最高的成员，空队返回 `None` |
| `heal_all(self, amount)` | 全队加血，**返回总回复量** |
| `damage_all(self, amount)` | 全队受伤，**返回总扣血量** |
| `report(self)` | 打印完整队伍报告 |

主流程要求：

- 造一支至少 4 人的队伍
- 打印报告
- 用 `damage_all` 打一次全体伤害，让**至少一人倒下**
- 打印存活人数和 `is_wiped()`
- 用 `heal_all` 治一次，打印实际总回复量
- 用 `find` 查一个存在的和一个不存在的
- 用 `remove` 移除一个成员，再打印人数
- 打印最强成员

> ⚠️ `Team` 的方法里**不许直接改 `m.hp`** —— 一律调 `Role` 的方法。
> 这就是「委托」：规则只写在一处。
