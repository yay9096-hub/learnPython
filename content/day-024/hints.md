## 提示 1 · 批量捡：循环 + append

```python
bag = []
loot = ["铁剑", "护符", "红药水", "面包"]

for item in loot:
    bag.append(item)
    print(f"✅ 捡到了 {item}！背包现在有 {len(bag)} 件")
```

⚠️ 千万别写成 `bag = bag.append(item)` ——
`.append()` 不返回东西，那样写背包会变成 `None`。

**列表方法直接改原列表，不用接住。**

## 提示 2 · 扔东西要先检查

```python
drop = input("想扔掉什么？").strip()

if drop in bag:
    bag.remove(drop)
    print(f"🗑 扔掉了 {drop}")
else:
    print(f"❓ 背包里没有 {drop}，扔不了")
```

没有这个 `if`，玩家输入一个背包里没有的东西，`remove()` 会直接报 ValueError。

「**先检查，再操作**」—— 这个习惯以后处理任何用户输入都用得上。

## 提示 3 · pop 会把东西交给你

```python
last = bag.pop()
print(f"✋ 掏出了 {last}")
```

注意 `.pop()` 和 `.remove()` 的区别：

- `.remove("面包")` —— 按**内容**删，删完就没了
- `.pop()` —— 按**位置**删（默认最后一个），而且**把它返回给你**，所以要用 `=` 接住

最后别忘了报一下战果：

```python
print(f"最终背包：{bag}")
print(f"一共 {len(bag)} 件")
```

数一数应该剩几件：捡 4 + 玩家捡 1 = 5，扔掉 1 剩 4，再掏走 1 —— **剩 3 件**。
