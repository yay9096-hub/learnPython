## 提示 1 · 从上往下，一步步来

**第一步：文件说明 + 常量**

```python
"""战斗伤害计算模块 —— Day 42 重构练习。"""

MIN_DAMAGE = 1
MAX_DAMAGE = 999
CRIT_RATE = 1.5
HEALTHY_HP = 400
WOUNDED_HP = 150
TOTAL_ROUNDS = 3
```

对照原代码找魔法数字：`999`（伤害上限）、`1.5`（暴击倍率）、
`400` 和 `150`（血量分档）、`3`（回合数）。

**第二步：给函数改名**

| 原名 | 它其实在干嘛 | 建议新名 |
|---|---|---|
| `f(a, b)` | 算伤害 | `deal_damage(atk, defense)` |
| `g(a, b)` | 算暴击 | `deal_crit_damage(atk, defense)` |
| `h(x)` | 判断活着没 | `is_alive(hp)` |
| `k(x)` | 返回状态文字 | `describe_status(hp)` |
| `p(n, x, y)` | 播报回合 | `show_round(round_no, damage, enemy_hp)` |
| `b(a, x, y)` | 跑完整场战斗 | `run_battle(atk, enemy_hp, enemy_defense)` |

## 提示 2 · 改名要连着改调用点

改了函数名，**所有调用的地方都要跟着改**，否则会 NameError。

顺序建议：改一个函数 → 立刻运行一次 → 没问题再改下一个。
**一次只改一处**，出错了马上知道是哪里。

```python
def deal_damage(atk, defense):
    """按「攻击力 - 防御力」算伤害，并夹在合法范围内。"""
    damage = atk - defense
    if damage < MIN_DAMAGE:
        damage = MIN_DAMAGE
    if damage > MAX_DAMAGE:
        damage = MAX_DAMAGE
    return damage
```

注意函数体里的 `c` 也改成了 `damage`，两个魔法数字换成了常量名。

## 提示 3 · docstring 写「为什么」不写「怎么做」

❌ 不好：`"""这个函数用 atk 减 defense 然后判断。"""`
（代码本身就看得出来，等于没说）

✅ 好：`"""按「攻击力 - 防御力」算伤害，最低保底 1 点。"""`
（说清了**规则**）

几个参考：

```python
def is_alive(hp):
    """血量大于 0 就还活着。"""
    return hp > 0


def describe_status(hp):
    """按血量返回状态描述：健康 / 受伤 / 危险。"""
    ...


def run_battle(atk, enemy_hp, enemy_defense):
    """打完固定回合数，返回敌人剩余血量。"""
    ...
```

⚠️ 最后一定要**运行一次对比输出** —— 三个回合敌人应该是
500 → 437 → 374 → 311，状态「受伤」。
数字对不上就说明改坏了。
