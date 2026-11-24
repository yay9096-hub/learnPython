# Day 27 · 战力排行榜 🏆

> 「Day 25 你能算出「最强的是谁」，但那只有一个人。
> 排行榜要**所有人按顺序排好**。今天学排序。」

---

## 📌 知识卡 1 · `.sort()` —— 原地排序

```python runnable 从小到大
scores = [88, 95, 72, 110, 66]

scores.sort()
print(scores)
```

原列表**直接变了**。跟 Day 24 的 `.append()` 一样，是列表方法 —— **不用接住**。

```python runnable 接了又变 None（跑一下）
scores = [88, 95, 72]
scores = scores.sort()
print(scores)
```

又是那个坑 😅 **列表方法改原来的，别用 `=` 接。**

文字也能排（按拼音/编码顺序）：

```python runnable 文字排序
names = ["banana", "apple", "cherry"]
names.sort()
print(names)
```

---

## 📌 知识卡 2 · `reverse=True` —— 从大到小 ⭐

排行榜要的是**从高到低**：

```python runnable 从大到小
scores = [88, 95, 72, 110, 66]

scores.sort(reverse=True)
print(scores)
```

`reverse=True` 是 Day 6 学过的**关键字参数**（跟 `sep=` `end=` 一个写法）。

---

## 📌 知识卡 3 · `sorted()` —— 不动原来的

有时候你**不想弄乱**原列表，那就用 `sorted()`：

```python runnable 对比一下
scores = [88, 95, 72]

ranked = sorted(scores, reverse=True)

print(f"排好的：{ranked}")
print(f"原来的：{scores}")
```

| | 改原列表？ | 返回新的？ | 怎么用 |
|---|---|---|---|
| `lst.sort()` | ✅ 改 | ❌ 不返回 | `lst.sort()` |
| `sorted(lst)` | ❌ 不改 | ✅ 返回 | `new = sorted(lst)` |

> 🧠 一句话：**`.sort()` 是动手术，`sorted()` 是照相。**

---

## 📌 知识卡 4 · ⚠️ 排序会拆散平行列表

这是今天最大的坑。Day 25 学的「名字和血量分开存」，一排序就完蛋：

```python runnable 排序之后对不上号了
names = ["星野樱", "月见琉璃", "天野灯"]
atks = [88, 95, 72]

atks.sort(reverse=True)

for i in range(len(names)):
    print(f"{names[i]} 的攻击力是 {atks[i]}")
```

**攻击力排好了，但名字没跟着动** —— 月见琉璃的 95 跑到星野樱头上了。

### 解决办法：把一对一起搬

把「名字 + 数值」打包成一个小列表，再排：

```python runnable 打包之后再排 ⭐
names = ["星野樱", "月见琉璃", "天野灯"]
atks = [88, 95, 72]

pairs = []
for i in range(len(names)):
    pairs.append([atks[i], names[i]])

print(f"打包后：{pairs}")

pairs.sort(reverse=True)
print(f"排序后：{pairs}")

for atk, name in pairs:
    print(f"{name} —— {atk}")
```

看懂三件事：

1. `[atks[i], names[i]]` —— **数值放前面**，因为排序默认按第一项比
2. `pairs.sort(reverse=True)` —— 整对一起移动，名字跟着数值走
3. `for atk, name in pairs:` —— 一次拿出两个（这叫**解包**，第 33 天细讲）

---

## 📌 知识卡 5 · `.index()` —— 查排名

```python runnable 查我排第几
ranked = ["夜刀神澪", "月见琉璃", "星野樱"]

who = "月见琉璃"
place = ranked.index(who)
print(f"{who} 排第 {place + 1} 名")
```

⚠️ `.index()` 给的是**编号**（从 0 开始），报名次要 `+1`。

⚠️ 查一个**不存在**的会报错，先用 `in` 检查（Day 24 的老规矩）：

```python runnable 安全地查名次
ranked = ["夜刀神澪", "月见琉璃"]
who = "路人甲"

if who in ranked:
    print(f"排第 {ranked.index(who) + 1} 名")
else:
    print(f"榜上没有 {who}")
```

---

## 📌 知识卡 6 · 几个顺手的

```python runnable 其它常用操作
nums = [3, 1, 4, 1, 5]

nums.reverse()           # 直接倒过来（不是排序！）
print(nums)

print(nums.count(1))     # 数有几个 1
```

⚠️ `.reverse()` 和 `.sort(reverse=True)` 不一样：

- `.reverse()` —— 把现在的顺序**颠倒**过来
- `.sort(reverse=True)` —— 真正**排序**成从大到小

---

## 🛠 今天的任务 · 战力排行榜

| 要求 | 说明 |
|---|---|
| 把名字和战力打包成 `pairs` | 每项是 `[战力, 名字]` |
| 按战力**从高到低**排序 | 用 `.sort(reverse=True)` |
| 打印排行榜 | `第 1 名 · 夜刀神澪 · 战力 998` |
| 前三名单独表扬 | 用切片 `[:3]`（Day 26 学的） |
| 问玩家查谁的名次 | `input()` |
| 先用 `in` 检查再报名次 | 查不到要提示「榜上无名」 |
| 报出榜首和榜尾 | 用 `[0]` 和 `[-1]` |

数据（starter 里给好了）：

```python
names  = ["星野樱", "月见琉璃", "天野灯", "水城凛", "夜刀神澪", "风见幽香"]
powers = [820, 995, 640, 998, 770, 905]
```

> 💡 判题会查「月见琉璃」（第 2 名）和一个不存在的人，两种都要处理好。
