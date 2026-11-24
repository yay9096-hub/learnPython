## 提示 1 · 参数写在括号里

```python
def show_line(char, width):
    """打印 width 个 char 组成的分隔线。"""
    print(char * width)
```

括号里的 `char` 和 `width` 是**占位名**，调用时给什么就是什么：

```python
show_line("=", 32)
show_line("─", 32)
show_line("★", 20)
```

⚠️ 参数**顺序**要跟定义一致。`show_line(32, "=")` 不报错，但会算 `32 * "="`，
结果完全不是你想要的。

## 提示 2 · 伤害函数要有保护

```python
def deal_damage(attacker, atk, defense):
    """按「攻击力 - 防御力」算伤害，最低保底 1 点。"""
    damage = atk - defense
    if damage < 1:
        damage = 1
    print(f"  {attacker} 造成了 {damage} 点伤害！")
```

那三行 `if` 是关键 —— 没有它，`deal_damage("史莱姆", 10, 99)` 会播报「造成 -89 点伤害」。

**改一处，所有调用点全都受益**，这就是函数的价值。

## 提示 3 · 参数也可以是列表

```python
def show_team(team):
    """打印整支队伍。"""
    print(f"  队伍共 {len(team)} 人：")
    for name in team:
        print(f"    · {name}")

show_team(["星野樱", "月见琉璃", "天野灯", "水城凛"])
```

⚠️ 人数一定要用 `len(team)` 算，别写死成 4 ——
判题会传一个 2 人的列表进去验证。

角色信息带血条：

```python
def show_role(name, hp, atk):
    """打印一行角色信息，附带血条。"""
    bar = "█" * (hp // 20)
    print(f"  {name}  HP {hp} {bar}  ATK {atk}")
```

`hp // 20` 是整除（Day 3 学的）—— 340 血画 17 格，长度正好。
