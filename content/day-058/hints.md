## 提示 1 · Team 的骨架

```python
class Team:
    """一支队伍。成员是一堆 Role 对象。"""

    def __init__(self, name):
        self.name = name
        self.members = []          # ← 属性可以是列表

    def add(self, role):
        """加一个成员，返回现在的人数。"""
        self.members.append(role)
        return len(self.members)

    def size(self):
        return len(self.members)
```

查找和移除是老套路，注意 `remove` 要**复用** `find`：

```python
    def find(self, name):
        """按名字找成员。找不到返回 None。"""
        for m in self.members:
            if m.name == name:
                return m
        return None

    def remove(self, name):
        """按名字移除成员，返回是否成功。"""
        member = self.find(name)          # ← 复用，不重写
        if member is None:
            return False
        self.members.remove(member)
        return True
```

## 提示 2 · 今天的核心：委托

```python
    def heal_all(self, amount):
        """全队加血，返回总回复量。具体怎么加交给每个成员自己。"""
        total = 0
        for m in self.members:
            total += m.heal(amount)      # ← 调 Role 的方法，不碰 m.hp
        return total
```

⚠️ **绝对不要在 Team 里写 `m.hp = m.hp + amount`**。

为什么？因为「不超过上限」「倒下的治不了」这些规则已经写在 `Role.heal` 里了。
Team 直接改 `hp`，等于绕过了所有保护。判题专门检查这一点。

`damage_all` 同理，调 `m.take_damage(amount)`。

**把每次调用的返回值加起来**，得到的才是「实际总量」：

- 50 血的成员挨 100 点，实际只扣 50
- 满血的成员治 30 点，实际回 0

## 提示 3 · 统计方法就是把老代码搬进来

```python
    def total_hp(self):
        total = 0
        for m in self.members:
            total += m.hp
        return total

    def avg_atk(self):
        if self.size() == 0:        # ← 空队先挡住
            return 0
        total = 0
        for m in self.members:
            total += m.atk
        return round(total / self.size(), 1)

    def alive_members(self):
        result = []
        for m in self.members:
            if m.is_alive():
                result.append(m)
        return result

    def is_wiped(self):
        return len(self.alive_members()) == 0
```

`report` 把它们串起来：

```python
    def report(self):
        print(f"  【{self.name}】{self.size()} 人 · "
              f"存活 {len(self.alive_members())} 人")
        print(f"  总血量 {self.total_hp()}  平均攻击 {self.avg_atk()}")
        for m in self.members:
            print(f"    {m.status()}")
```

⚠️ 主流程里 `damage_all` 的伤害要**够大**（比如 150），
不然打不倒天野灯（120 血），演示不出「有人倒下」。
