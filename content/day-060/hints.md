## 提示 1 · 重写就是「写一个同名方法」

父类先给一个基础实现：

```python
    def attack(self, target):
        """普通攻击，造成 atk 点伤害。"""
        damage = self.atk
        target.take_damage(damage)
        return damage

    def skill_name(self):
        return "普通攻击"
```

子类写同名的就覆盖了：

```python
class Rogue(Role):
    """盗贼。背刺，伤害 2.5 倍。"""

    def attack(self, target):
        damage = int(self.atk * 2.5)
        target.take_damage(damage)
        return damage

    def skill_name(self):
        return "背刺"
```

⚠️ `int(...)` 别忘了 —— 35 × 2.5 = 87.5，判题要的是 **87**。

## 提示 2 · 战士用 super() 扩展

```python
class Warrior(Role):
    def attack(self, target):
        """先照常打一下，再追加 atk // 2 点。"""
        base = super().attack(target)      # ← 父类已经打过一次了
        bonus = self.atk // 2
        target.take_damage(bonus)          # ← 追加那部分也要真的打出去
        return base + bonus
```

两个容易漏的点：

- **必须用 `super().attack(target)`**，不许把父类那三行抄一遍（判题会查）
- `super()` 只打了 `base`，**追加的 `bonus` 要自己再 `take_damage` 一次**

⚠️ 千万别写 `self.attack(target)` —— 那是调自己，会无限递归。

## 提示 3 · 法师的两种状态

```python
class Mage(Role):
    COST = 20

    def attack(self, target):
        """够蓝就放魔法，不够就用法杖敲。"""
        if self.mp < self.COST:
            return super().attack(target)      # ← 退回父类的普通攻击
        self.mp = self.mp - self.COST
        damage = self.atk * 3
        target.take_damage(damage)
        return damage

    def skill_name(self):
        if self.mp < self.COST:
            return "法杖敲击"
        return "奥术飞弹"
```

蓝不够时：**不扣蓝、伤害等于 atk、走 `super()`** —— 三个条件判题都会验。

`COST = 20` 写在类里面、方法外面，叫**类属性** ——
所有法师共用这个值，改一处全改。

## 提示 4 · 主流程一个循环搞定

```python
boss = Role("暗影魔王", 2000, 50)

team = [
    Role("路人甲", 100, 30),
    Warrior("铁壁", 200, 40),
    Mage("月见琉璃", 120, 25),
    Rogue("影", 140, 35),
]

for m in team:
    damage = m.attack(boss)
    print(f"  {m.name} 使用「{m.skill_name()}」，造成 {damage} 点")
```

**一个 `isinstance` 都不要写** —— 这正是今天的重点。
每个对象自己知道该怎么打，主流程只管喊「攻击」。

对照表用 `type(m).__name__`（Day 59 学的）：

```python
for m in team:
    print(f"  {type(m).__name__:<8} {m.name:<10} → {m.skill_name()}")
```
