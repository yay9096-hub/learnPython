## 提示 1 · 返回多个就是加逗号

```python
def roll_stats(level):
    """按等级随机生成三围，返回 (hp, mp, atk)。"""
    hp = random.randint(50, 100) + level * 20
    mp = random.randint(20, 60) + level * 10
    atk = random.randint(10, 30) + level * 5
    return hp, mp, atk
```

接住时左边写**同样多**的变量：

```python
hp, mp, atk = roll_stats(10)
```

这就是 Day 33 的解包 —— 右边其实是个元组 `(hp, mp, atk)`。

评级函数返回两个：

```python
def judge_stats(hp, mp, atk):
    """按三围总和评级，返回 (评级, 总和)。"""
    total = hp + mp + atk
    if total >= 400:
        return "优秀", total
    if total >= 300:
        return "普通", total
    return "偏弱", total
```

⚠️ 边界用 `>=`：总和正好 400 算优秀、正好 300 算普通。判题会拿这两个数试。

## 提示 2 · make_role 要「拼零件」，不要重写

```python
def make_role(name, level):
    """造一个完整的角色字典。"""
    hp, mp, atk = roll_stats(level)
    rank, total = judge_stats(hp, mp, atk)
    return {
        "name": name,
        "level": level,
        "hp": hp,
        "mp": mp,
        "atk": atk,
        "total": total,
        "rank": rank,
    }
```

⚠️ 判题会检查 `make_role` **内部真的调用了**另外两个函数。
把 `random.randint` 和评级逻辑再抄一遍是不行的 —— 那样改公式要改两处。

## 提示 3 · 结果 + 说明

```python
def check_name(name):
    """检查名字长度，返回 (是否合法, 说明文字)。"""
    if len(name) < 2:
        return False, "名字太短了，至少 2 个字"
    if len(name) > 8:
        return False, "名字太长了，最多 8 个字"
    return True, "名字可以用"
```

主流程用循环验三个名字：

```python
for n in ["樱", "超级无敌宇宙第一魔法少女", "星野樱"]:
    ok, msg = check_name(n)
    mark = "✓" if ok else "✗"
    print(f"  {mark} 「{n}」→ {msg}")
```

批量造角色也用列表装起来再遍历：

```python
roles = [
    make_role("星野樱", 12),
    make_role("月见琉璃", 8),
    make_role("路人甲", 1),
]

for r in roles:
    print(f"  {r['name']} Lv.{r['level']}  HP {r['hp']}  [{r['rank']}]")
```
