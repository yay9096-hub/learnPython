## 提示 1 · 继承的写法只有两处不同

```python
class Warrior(Role):                      # ① 括号里写父类
    """战士。血厚，有护甲能减免伤害。"""

    def __init__(self, name, hp=200, atk=40, armor=10):
        super().__init__(name, hp, atk)   # ② 第一句调父类
        self.armor = armor                # ③ 再加自己的属性

    def real_damage(self, amount):
        """算上护甲之后实际受到的伤害，最低 1 点。"""
        return max(1, amount - self.armor)

    def roar(self):
        """怒吼，攻击力永久 +10。"""
        self.atk = self.atk + 10
        return f"{self.name} 发出怒吼！攻击力升到 {self.atk}"
```

⚠️ **`super().__init__(...)` 是第一句** —— 忘了它，
`name`、`hp`、`alive` 这些父类属性全都不存在，一用就 AttributeError。

⚠️ **不要在子类里再写 `take_damage` / `heal` / `status`** ——
那些已经从父类继承来了，重写一遍等于白继承。判题会检查。

## 提示 2 · 法师和盗贼

```python
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
            return 0                       # ← 提前返回，别扣蓝也别扣血
        self.mp = self.mp - cost
        damage = self.atk * 2
        target.take_damage(damage)
        return damage
```

盗贼更简单：

```python
class Rogue(Role):
    def __init__(self, name, hp=140, atk=35, crit=2.0):
        super().__init__(name, hp, atk)
        self.crit = crit

    def backstab(self, target):
        """背刺，造成暴击伤害。"""
        damage = int(self.atk * self.crit)   # ← 记得 int()，不然是小数
        target.take_damage(damage)
        return damage
```

## 提示 3 · 显示职业和统计

```python
for m in team:
    print(f"  [{type(m).__name__}] {m.status()}")
```

`type(m).__name__` 拿到类名的文字（"Warrior"、"Mage"…）。

类型判断：

```python
print(f"  战士是 Warrior 吗：{isinstance(warrior, Warrior)}")   # True
print(f"  战士也是 Role 吗：{isinstance(warrior, Role)}")       # True ← 关键
print(f"  战士是 Mage 吗：{isinstance(warrior, Mage)}")         # False
```

中间那个 True 是继承的核心含义：**战士「是一种」Role**。

按职业统计（Day 29 的 `.get(键, 默认值)`）：

```python
counts = {}
for m in all_members:
    kind = type(m).__name__
    counts[kind] = counts.get(kind, 0) + 1

for kind, n in counts.items():
    print(f"  {kind}：{n} 人")
```

⚠️ 演示施法时记得先放两次正常的，再把 `mage.mp` 手动调低，
第三次才能演示出「魔力不足」。
