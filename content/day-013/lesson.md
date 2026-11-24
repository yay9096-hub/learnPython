# Day 13 · 入学资格审查 📋

> 「昨天判断一次只能问一个问题。
> 但真实的规则往往是：**年龄够 而且 魔力够 而且 没被通缉**。
> 今天学会把条件拼起来。」

---

## 📌 知识卡 1 · `and` —— 两个都要成立

```python runnable 两个条件都要满足
age = 16
mp = 80

if age >= 15 and mp >= 50:
    print("✅ 通过审查")
else:
    print("❌ 不符合条件")
```

把 `mp` 改成 `30` 再跑 —— 就不通过了，因为 `and` 要求**两边都成立**。

```python runnable and 的真值表
print(True and True)
print(True and False)
print(False and True)
print(False and False)
```

**只有两个都是 True，结果才是 True。** 一个不达标就整体不通过。

`and` 可以串很多个：

```python runnable 三个条件
age = 16
mp = 80
banned = False

if age >= 15 and mp >= 50 and banned == False:
    print("✅ 全部条件达标")
```

---

## 📌 知识卡 2 · `or` —— 任意一个成立就行

```python runnable 有一条路走通就行
is_vip = False
score = 95

if is_vip or score >= 90:
    print("🎫 可以进入 VIP 区")
else:
    print("普通入口那边请")
```

```python runnable or 的真值表
print(True or False)
print(False or False)
```

**只要有一个是 True，结果就是 True。** 全是 False 才不通过。

> 🧠 一句话记住：
> **`and` 是「严格」，条件越多越难通过。**
> **`or` 是「宽容」，条件越多越容易通过。**

---

## 📌 知识卡 3 · `not` —— 反过来

```python runnable not 把结果翻个面
banned = False

if not banned:
    print("没被封禁，可以进")
```

`not banned` 读作「**没有**被封禁」。当 `banned` 是 `False` 时，`not banned` 就是 `True`。

```python runnable not 的效果
print(not True)
print(not False)
print(not (10 > 3))
```

> 💡 `if not banned:` 比 `if banned == False:` 更短也更好读，是 Python 的习惯写法。

---

## 📌 知识卡 4 · `in` —— 在不在这一串里面

这个特别实用。想问「属性是不是火水风之一」，不用写三个 `or`：

```python runnable in 一句顶三句
element = "水"

if element in ["火", "水", "风"]:
    print("✅ 合法属性")
else:
    print("❓ 不认识这个属性")
```

方括号 `[ ]` 里用逗号隔开的一串东西叫**列表**（第三章会细讲）。
今天你只要知道：**`in` 是问「在不在里面」**。

对比一下有多省事：

```python runnable 三个 or vs 一个 in
element = "水"

print(element == "火" or element == "水" or element == "风")
print(element in ["火", "水", "风"])
```

`in` 也能查文字里有没有某几个字：

```python runnable 文字里找字
name = "星野樱"

if "樱" in name:
    print("名字里有樱！")
```

配合 `not` 就是「不在里面」：

```python runnable not in
element = "土"

if element not in ["火", "水", "风"]:
    print("❓ 这个属性不在名单里")
```

---

## 📌 知识卡 5 · ⚠️ 一个常见的写错

想表达「等级是 1 或者 2」，很多人会这样写：

```python runnable 这样写是错的（跑跑看）
level = 5

if level == 1 or 2:
    print("新手")
```

等级明明是 5，却打印了「新手」！

因为 Python 把它读成了 `(level == 1) or (2)`，
而 `2` 这个非零数字本身就算 `True`，所以整体永远成立。

**正确写法：每一边都要写完整的比较。**

```python runnable 正确写法
level = 5

if level == 1 or level == 2:
    print("新手")
else:
    print("不是新手")

# 或者更简洁：
if level in [1, 2]:
    print("新手")
```

---

## 📌 知识卡 6 · 括号让意思更清楚

`and` 比 `or` 优先级高（就像乘法比加法优先）。混用时**加括号**，别让人猜：

```python runnable 括号改变了含义
age = 10
is_vip = True
mp = 100

print(age >= 15 and mp >= 50 or is_vip)
print(age >= 15 and (mp >= 50 or is_vip))
```

两行结果不一样。**混用 `and` 和 `or` 时，永远加括号。**

---

## 🛠 今天的任务 · 入学资格审查

派森学院的录取规则：

```
必须同时满足：
  ① 年龄 >= 15
  ② 魔力 >= 50
  ③ 属性是 火 / 水 / 风 之一
  ④ 没有黑历史

以上全部满足 -> 录取
只要缺一条   -> 拒绝，并说明缺哪一条
```

| 要求 | 说明 |
|---|---|
| 问年龄 | `int()`，存进 `age` |
| 问魔力 | `int()`，存进 `mp` |
| 问属性 | 存进 `element` |
| 问有没有黑历史（y/n） | 存进 `record`，输入 `y` 表示**有**黑历史 |
| 用 `and` 把四个条件拼起来 | 全过 → 输出里有「录取」 |
| 用 `in` 判断属性合法性 | 不合法要能识别出来 |
| 没过时要说明原因 | 输出里有「拒绝」，并指出缺了哪一条 |

> 💡 判题会跑四遍：全达标、年龄不够、属性不对、有黑历史。
