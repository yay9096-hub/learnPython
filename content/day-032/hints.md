## 提示 1 · 先全部转成集合

```python
my_set = set(mine)
her_set = set(hers)
his_set = set(his)

print(f"我的好友列表原有 {len(mine)} 条，去重后 {len(my_set)} 人")
```

一行 `set(...)` 就完成了 Day 28 写 5 行才做完的去重。

## 提示 2 · 三个运算符

```python
common = my_set & her_set          # 交集：两边都有
everyone = my_set | her_set        # 并集：合起来去重
only_mine = my_set - her_set       # 差集：我有你没有
only_hers = her_set - my_set       # 注意方向反过来了！
```

⚠️ **差集有方向**：`a - b` 和 `b - a` 结果完全不同。
「只有我认识的」= `我 - 她`；「只有她认识的」= `她 - 我`。

三个人的共同好友，`&` 可以连着写：

```python
all_common = my_set & her_set & his_set
```

## 提示 3 · 显示前排个序

集合**没有顺序**，直接打印每次结果排列可能不一样，也不能 `[0]` 取。
打印前用 `sorted()` 转成排好的列表：

```python
print(f"共同好友（{len(common)} 人）：{sorted(common)}")
```

完整的一段长这样：

```python
common = my_set & her_set
print(f"我和她的共同好友（{len(common)} 人）：{sorted(common)}")

everyone = my_set | her_set
print(f"我俩认识的所有人（{len(everyone)} 人）：{sorted(everyone)}")
```

剩下几项照着这个格式写就行 ✨
