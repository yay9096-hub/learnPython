## 提示 1 · 三个扣血函数的区别就在这几行

```python
def damage_wrong(hp, dmg):
    """错误示范：只改了局部变量，外面感觉不到。"""
    hp = hp - dmg
    print(f"    （函数内部看到的血量：{hp}）")


def damage_right(hp, dmg):
    """正确做法：把新血量交回去。"""
    return hp - dmg


def damage_dict(role, dmg):
    """字典是可变对象，改内容外面真的会变，不用 return。"""
    role["hp"] = role["hp"] - dmg
```

看清楚：

- 第一个**故意不写 return** —— 判题会检查它确实没有
- 第二个只有一行 `return`
- 第三个改的是**字典里的值**，所以不用 return

## 提示 2 · 主流程要打印「前后对比」

这一天的重点是**亲眼看见差别**，所以每次都要前后各打印一次：

```python
print("\n① 不 return —— 改不动")
hp = 500
print(f"  调用前：{hp}")
damage_wrong(hp, 63)
print(f"  调用后：{hp}   ← 一点没变")

print("\n② 用 return 接住 —— 改得动")
hp = 500
print(f"  调用前：{hp}")
hp = damage_right(hp, 63)      # ← 关键在这个 hp =
print(f"  调用后：{hp}   ← 变了！")
```

⚠️ 第二种**必须用 `hp =` 接住**，光调用不接等于白干。

第三种传字典：

```python
role = {"name": "星野樱", "hp": 500}
print(f"  调用前：{role['hp']}")
damage_dict(role, 63)
print(f"  调用后：{role['hp']}   ← 也变了！")
```

## 提示 3 · 整队加血

```python
def heal_team(team, amount):
    """给整队人加血。列表和字典都是可变的，直接改就行。"""
    for member in team:
        member["hp"] = member["hp"] + amount
```

主流程里加血前后各遍历打印一次：

```python
team = [
    {"name": "星野樱", "hp": 340},
    {"name": "月见琉璃", "hp": 280},
    {"name": "天野灯", "hp": 310},
]

print("  加血前：")
for m in team:
    print(f"    {m['name']} {m['hp']}")

heal_team(team, 50)

print("  加血后：")
for m in team:
    print(f"    {m['name']} {m['hp']}")
```

最后别忘了写一句结论，里面要出现 `return` 这个词：

```python
print("💡 我的结论：数字和文字要用 return 把结果交回来才算数，")
print("   列表和字典改内容就能直接生效。")
```
