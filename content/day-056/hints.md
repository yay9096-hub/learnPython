## 提示 1 · 方法就是缩进在类里的函数

```python
class Role:
    def __init__(self, name, hp=100, mp=50, atk=30):
        ...

    def is_alive(self):
        """还活着吗。"""
        return self.hp > 0

    def take_damage(self, amount):
        """受到伤害，返回实际扣掉的血量。"""
        self.hp = self.hp - amount
        if not self.is_alive():          # ← 调自己的方法也要写 self.
            self.alive = False
            print(f"     💀 {self.name} 倒下了")
        return amount
```

三个要点：

- 方法**缩进在 class 里面**，跟 `__init__` 同一层
- **第一个参数永远是 `self`**
- **调用自己的别的方法要写 `self.`** —— 光写 `is_alive()` 会报 NameError

## 提示 2 · attack 里有两个角色

```python
    def attack(self, target):
        """攻击另一个角色，返回造成的伤害。"""
        damage = self.atk
        print(f"     ⚔️ {self.name} 攻击 {target.name}，造成 {damage} 点")
        target.take_damage(damage)       # ← 让对方自己处理扣血
        return damage
```

分清楚：

- **`self`** = 攻击者（`sakura.attack(enemy)` 里的 sakura）
- **`target`** = 挨打的（括号里的 enemy）

⚠️ 别在 attack 里直接写 `target.hp -= damage` ——
调 `target.take_damage(...)` 才会触发倒下判断。判题会检查这一点。

升级要改四样：

```python
    def level_up(self):
        """升级：等级+1，上限+20，攻击+5，并且回满血。"""
        self.level = self.level + 1
        self.max_hp = self.max_hp + 20
        self.atk = self.atk + 5
        self.hp = self.max_hp            # ← 回满血，别忘了
        print(f"     ⬆️ {self.name} 升到了 {self.level} 级！")
        return self.level
```

## 提示 3 · status 只 return，主流程负责打印

```python
    def status(self):
        """返回一行状态文字。"""
        state = "存活" if self.is_alive() else "倒下"
        return f"{self.name} Lv.{self.level}  HP {self.hp}/{self.max_hp}  ATK {self.atk}  [{state}]"
```

主流程里用 `print("  " + hero.status())`。

战斗循环靠 `is_alive()` 控制：

```python
round_no = 0
while hero.is_alive() and enemy.is_alive() and round_no < 6:
    round_no = round_no + 1
    print(f"\n--- 第 {round_no} 回合 ---")

    hero.attack(enemy)
    if not enemy.is_alive():
        break                    # 打死了就别再挨打了

    enemy.attack(hero)

    if round_no == 2:
        hero.heal(40)
    if round_no == 3:
        hero.level_up()

    print("  " + hero.status())
    print("  " + enemy.status())
```

⚠️ 那个 `round_no < 6` 是**保险丝** —— 万一双方伤害太低打不死，
循环也不会变成死循环。
