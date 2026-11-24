## 提示 1 · 先打包，再排序

**这是今天的核心。** 名字和战力分开排会对不上号，所以要打包成一对：

```python
pairs = []
for i in range(len(names)):
    pairs.append([powers[i], names[i]])
```

⚠️ **战力放前面**！因为排序默认按每项的**第一个元素**比大小。

打包完 `print(pairs)` 看一眼，长这样：

```
[[820, '星野樱'], [995, '月见琉璃'], [640, '天野灯'], ...]
```

然后一句话排好：

```python
pairs.sort(reverse=True)
```

整对一起移动，名字自然跟着战力走。

## 提示 2 · 打印榜单

```python
for i, pair in enumerate(pairs):
    print(f"第 {i + 1} 名 · {pair[1]} · 战力 {pair[0]}")
```

`pair[0]` 是战力，`pair[1]` 是名字（因为打包时战力放在前面）。

也可以用解包写得更好看：

```python
for i, (power, name) in enumerate(pairs):
    print(f"第 {i + 1} 名 · {name} · 战力 {power}")
```

前三名用切片：

```python
for power, name in pairs[:3]:
    print(f"   {name}（{power}）")
```

## 提示 3 · 查名次

`.index()` 要在**名字列表**上用，但排序后的名字在 `pairs` 里，
所以先把排好序的名字单独抽出来：

```python
ranked_names = []
for power, name in pairs:
    ranked_names.append(name)

who = input("想查谁的名次？").strip()

if who in ranked_names:
    place = ranked_names.index(who) + 1
    print(f"🔎 {who} 排第 {place} 名")
else:
    print(f"🔎 榜上无名：查无此人「{who}」")
```

两个要点：

- `.index()` 给的是编号，报名次要 **+1**
- 查之前先 `in` 检查，否则查不到会报 ValueError
