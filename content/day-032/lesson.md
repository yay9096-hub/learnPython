# Day 32 · 共同好友 🔗

> 「Day 28 你写了 5 行代码去重：
> 建空列表、遍历、`not in`、append……
>
> 今天告诉你，那件事其实**一行就够了**。」

---

## 📌 知识卡 1 · `set()` —— 一行去重 ⭐

```python runnable Day 28 的 5 行 vs 今天的 1 行
words = ["牛啊", "前排", "牛啊", "打卡", "牛啊"]

# Day 28 的写法
unique = []
for w in words:
    if w not in unique:
        unique.append(w)
print(unique)

# 今天的写法
print(set(words))
```

`set()` 就是**集合** —— 一群**不重复**的东西。

写法上，集合用大括号 `{ }`（跟字典一样，但**没有冒号**）：

```python runnable 直接写一个集合
friends = {"星野樱", "月见琉璃", "天野灯"}
print(friends)
print(len(friends))
print(type(friends))
```

⚠️ 空集合要写 `set()`，**不能写 `{}`** —— 那是空字典：

```python runnable 空的到底是谁
print(type({}))
print(type(set()))
```

---

## 📌 知识卡 2 · 集合的两个特点

**① 自动去重**

```python runnable 重复的会被吃掉
s = {"樱", "琉璃", "樱", "樱"}
print(s)
print(len(s))
```

**② 没有顺序，不能用编号取**

```python runnable 集合不能编号（会报错）
s = {"樱", "琉璃", "灯"}
print(s[0])
```

想要回顺序，转成列表再排：

```python runnable 转回列表
words = ["牛啊", "前排", "牛啊", "打卡"]

unique = list(set(words))
unique.sort()
print(unique)
```

| | 列表 `[]` | 集合 `{}` |
|---|---|---|
| 能重复吗 | ✅ 能 | ❌ 自动去重 |
| 有顺序吗 | ✅ 有 | ❌ 没有 |
| 能 `[0]` 取吗 | ✅ 能 | ❌ 不能 |
| 查「在不在」 | 慢 | **快** |

---

## 📌 知识卡 3 · 交集 `&` —— 共同好友 ⭐

这是集合最爽的地方：

```python runnable 一行算出共同好友
my_friends = {"星野樱", "月见琉璃", "天野灯", "水城凛"}
her_friends = {"月见琉璃", "水城凛", "夜刀神澪"}

print(my_friends & her_friends)
```

`&` 读作「**两边都有的**」。

想想不用集合要怎么写：

```python runnable 不用集合的写法（累）
mine = ["樱", "琉璃", "灯"]
hers = ["琉璃", "澪"]

common = []
for f in mine:
    if f in hers:
        common.append(f)
print(common)
```

**5 行 → 1 行。**

---

## 📌 知识卡 4 · 并集 `|` 和差集 `-`

```python runnable 三个运算
a = {"樱", "琉璃", "灯"}
b = {"琉璃", "澪"}

print(a & b)
print(a | b)
print(a - b)
print(b - a)
```

| 符号 | 名字 | 意思 | 好友场景 |
|---|---|---|---|
| `&` | 交集 | 两边都有 | **共同好友** |
| `\|` | 并集 | 合起来去重 | 所有认识的人 |
| `-` | 差集 | 我有你没有 | **只有我认识的** |

⚠️ `a - b` 和 `b - a` **结果不一样** —— 差集有方向。

---

## 📌 知识卡 5 · 增删和检查

```python runnable 集合的日常操作
friends = {"樱", "琉璃"}

friends.add("灯")               # 加一个（不是 append！）
print(friends)

friends.add("灯")               # 重复添加没有效果
print(len(friends))

friends.discard("琉璃")         # 删（不存在也不报错）
print(friends)

print("樱" in friends)          # 查
```

⚠️ 集合用 `.add()` 不是 `.append()`。

⚠️ `.remove()` 删不存在的会报错，`.discard()` 不会 —— **建议用 `.discard()`**。

---

## 📌 知识卡 6 · 什么时候用集合

| 需求 | 用什么 |
|---|---|
| 要保持顺序 | 列表 |
| 要允许重复 | 列表 |
| 要**去重** | **集合** |
| 要算**共同 / 差异** | **集合** |
| 要「名字 → 数据」的对应 | 字典 |

> 🧠 一句话：**列表管顺序，字典管对应，集合管「有没有」。**

---

## 🛠 今天的任务 · 好友分析

给你三个人的好友列表（**注意里面有重复**）：

```python
mine  = ["星野樱", "月见琉璃", "天野灯", "水城凛", "月见琉璃", "星野樱"]
hers  = ["月见琉璃", "水城凛", "夜刀神澪", "风见幽香"]
his   = ["天野灯", "水城凛", "雾岛遥"]
```

| 要求 | 说明 |
|---|---|
| 把三个列表都转成集合 | `my_set` / `her_set` / `his_set` |
| 报出我去重后有几个好友 | 原来 6 条，去重后几个？ |
| 我和她的共同好友 | 用 `&` |
| 我和她所有认识的人 | 用 `\|` |
| 只有我认识的 | 用 `-` |
| 只有她认识的 | 反过来减 |
| 三个人的共同好友 | `&` 可以连着用 |
| 结果都排序后再显示 | 集合没顺序，要 `sorted()` 一下才好看 |

> 💡 自己先算：我去重后 4 个、我和她的共同好友 2 个、三人共同好友 1 个（水城凛）。
