# Day 36 · 伤害公式函数 ⚙️

> 「昨天的函数是『死』的 —— `show_hero()` 永远打印同一个角色。
> 今天给它装上**参数**：同一个函数，喂不同的料，出不同的结果。」

---

## 📌 知识卡 1 · 参数是什么

对比一下：

```python runnable 没有参数：写死了
def greet():
    print("你好，星野樱！")

greet()
greet()
```

```python runnable 有参数：想问候谁就问候谁
def greet(name):
    print(f"你好，{name}！")

greet("星野樱")
greet("月见琉璃")
greet("天野灯")
```

括号里的 `name` 就是**参数** —— 一个**占位的名字**。

调用时括号里给的值，会被装进这个占位名，然后函数体就能用它了。

> 🧠 一句话：**参数是函数的「入口」。**

---

## 📌 知识卡 2 · 参数就是个临时变量

```python runnable 参数在函数里当变量用
def show_hp(hp):
    print(f"当前血量：{hp}")
    print("█" * (hp // 20))

show_hp(340)
show_hp(80)
```

`hp` 在函数里跟普通变量没区别 —— 能参与运算、能拿去循环。

⚠️ 但它**只在函数内部存在**：

```python runnable 参数出了函数就没了
def show_hp(hp):
    print(hp)

show_hp(340)
print(hp)
```

`NameError` —— `hp` 是函数内部的临时变量。（这叫**作用域**，第 40 天专讲。）

---

## 📌 知识卡 3 · 多个参数，按顺序对上 ⭐

```python runnable 两个参数
def attack(attacker, damage):
    print(f"{attacker} 造成了 {damage} 点伤害！")

attack("星野樱", 63)
attack("暗影魔像", 41)
```

参数之间用**逗号**隔开。调用时**按顺序**一一对应：

```
def attack(attacker, damage):
              ↓         ↓
attack(  "星野樱"  ,   63  )
```

⚠️ **顺序写反了不会报错，但结果全乱**：

```python runnable 顺序反了（不报错，但意思全变）
def attack(attacker, damage):
    print(f"{attacker} 造成了 {damage} 点伤害！")

attack(63, "星野樱")
```

Python 不知道你想干嘛，它只会照着位置塞。**这种 bug 最难找。**

---

## 📌 知识卡 4 · 个数必须对上

```python runnable 少给一个（会报错）
def attack(attacker, damage):
    print(f"{attacker} 造成 {damage} 点")

attack("星野樱")
```

报错信息会告诉你「缺了哪个参数」—— 派森酱会翻译给你看。

| 术语 | 指的是 |
|---|---|
| **形参** | 定义时括号里的名字，如 `def attack(attacker, damage)` |
| **实参** | 调用时括号里的值，如 `attack("星野樱", 63)` |

（名字知道就行，重点是**个数和顺序要对上**。）

---

## 📌 知识卡 5 · 把 Day 3 的伤害公式做成函数 ⭐

还记得 Day 3 吗？那时候你是这么写的：

```python runnable Day 3 的写法：算一次写一遍
atk = 88
defense = 25
damage = atk - defense
print(f"造成 {damage} 点伤害")

atk2 = 110
defense2 = 40
damage2 = atk2 - defense2
print(f"造成 {damage2} 点伤害")
```

变量名越编越难看。**做成函数之后**：

```python runnable 函数版：算几次都一样干净
def deal_damage(atk, defense):
    """按「攻击力 - 防御力」算伤害并播报。"""
    damage = atk - defense
    print(f"造成 {damage} 点伤害")

deal_damage(88, 25)
deal_damage(110, 40)
deal_damage(66, 80)
```

⚠️ 最后一次是负数 —— 说明公式还不够好。函数里可以加判断：

```python runnable 加个保护
def deal_damage(atk, defense):
    """伤害至少是 1，不会出现负数。"""
    damage = atk - defense
    if damage < 1:
        damage = 1
    print(f"造成 {damage} 点伤害")

deal_damage(66, 80)
```

**改一处，所有调用点全都受益** —— 这就是函数的复利。

---

## 📌 知识卡 6 · 参数可以是任何类型

列表、字典都能传：

```python runnable 传一个列表进去
def show_team(team):
    """打印整支队伍。"""
    print(f"队伍共 {len(team)} 人：")
    for name in team:
        print(f"  · {name}")

show_team(["星野樱", "月见琉璃", "天野灯"])
show_team(["水城凛"])
```

```python runnable 传一个字典进去
def show_role(role):
    """打印一个角色档案。"""
    print(f"{role['name']} · HP {role['hp']} · ATK {role['atk']}")

show_role({"name": "星野樱", "hp": 340, "atk": 88})
show_role({"name": "水城凛", "hp": 250, "atk": 110})
```

---

## 🛠 今天的任务 · 战斗系统 2.0

把 Day 35 的播报升级成**带参数**的版本：

| 函数 | 参数 | 要做的事 |
|---|---|---|
| `show_line(char, width)` | 符号、宽度 | 打印 width 个 char |
| `show_role(name, hp, atk)` | 名字、血量、攻击 | 打印一行角色信息，带血条 |
| `deal_damage(attacker, atk, defense)` | 攻击方、攻击力、防御力 | 算伤害并播报，伤害最低为 1 |
| `show_team(team)` | 一个列表 | 打印整队人 |

主流程要求：

- `show_line` 用**不同的符号和宽度**至少调用 3 次
- `show_role` 至少调用 2 次，传不同角色
- `deal_damage` 至少调用 3 次，其中**一次攻击力低于防御力**（验证保护生效）
- `show_team` 调用 1 次，传一个至少 3 人的列表

> 💡 判题会直接调用你写的函数喂不同的值，所以**参数名和顺序要照表格来**。
