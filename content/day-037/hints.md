## 提示 1 · return 和 print 的区别

```python
def deal_damage(atk, defense):
    """按「攻击 - 防御」算伤害，最低保底 1 点。"""
    return max(atk - defense, 1)
```

注意最后一行是 `return`，**不是 `print`**。

区别在于：

```python
dmg = deal_damage(88, 25)     # dmg 现在是 63，能拿去用
enemy_hp = enemy_hp - dmg     # ← 这一步昨天的版本做不到
```

`max(a, b)` 返回较大的那个，用它一行就完成保底，比写 `if` 短。

## 提示 2 · 提前返回，省掉 else

```python
def grade(score):
    """把分数转成等第。"""
    if score >= 90:
        return "优秀"
    if score >= 60:
        return "及格"
    return "再努力一下"
```

三个 `if`、零个 `else` —— 因为 `return` 一执行函数就结束了，
后面的判断根本没机会跑。这种写法比嵌套 else 好读。

⚠️ 边界要用 `>=`：90 分算优秀、60 分算及格。判题会拿边界值试。

布尔值直接返回比较结果就行：

```python
def is_alive(hp):
    """血量大于 0 就还活着。"""
    return hp > 0
```

不用写 `if hp > 0: return True else: return False` —— 那是重复劳动。

## 提示 3 · 主流程负责打印

函数只算不打印，所以主流程要接住返回值再 print：

```python
enemy_hp = 500
for atk in [88, 110, 95]:
    dmg = deal_damage(atk, 25)
    enemy_hp = enemy_hp - dmg
    print(f"  造成 {dmg} 点伤害，敌人剩余 {enemy_hp} 血")
```

掷骰子要把三次**加起来**：

```python
a = roll(6)
b = roll(6)
c = roll(20)
print(f"  三次点数：{a} + {b} + {c} = {a + b + c}")
```

战报函数返回字符串，主流程打印它：

```python
def battle_report(name, hp):
    """生成一句战报文字。"""
    status = "存活" if is_alive(hp) else "倒下"
    return f"【战报】{name} 当前 HP {hp}，状态：{status}"

print(battle_report("星野樱", 340))
```

> 💡 `"存活" if 条件 else "倒下"` 是三元表达式，一行写完 if-else。
> 不用也行，写成普通 if 一样过。
