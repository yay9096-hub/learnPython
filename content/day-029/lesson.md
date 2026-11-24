# Day 29 · 角色档案 🗂

> 「列表用**数字**当编号：`team[0]`、`hps[2]`。
> 问题是 —— 你得记住『2 号位是攻击力』这种事，太反人类了。
>
> 今天学**字典**：用『名字』当编号，`role["攻击力"]`。」

---

## 📌 知识卡 1 · 列表的痛点

Day 25 你是这么存一个角色的：

```python runnable 列表版：得记住谁在几号位
role = ["星野樱", 12, 340, 88]

print(role[0])
print(role[2])
```

`role[2]` 到底是血量还是攻击力？**你得靠记。** 数据一多就乱套了。

字典版：

```python runnable 字典版：一目了然
role = {"name": "星野樱", "level": 12, "hp": 340, "atk": 88}

print(role["name"])
print(role["hp"])
```

`role["hp"]` —— 不用记，**写的就是它的意思**。

---

## 📌 知识卡 2 · 字典长什么样

**大括号 `{ }`，里面是 `键: 值`，用逗号隔开。**

```python runnable 造一个角色
role = {
    "name": "星野樱",
    "level": 12,
    "hp": 340,
    "mp": 180,
    "element": "火"
}

print(role)
```

> 💡 一行一个键值对（像上面那样竖着写）是常见风格，好读好改。
> 最后一项后面**可以留一个逗号**，加新项时更方便。

术语对照：

| 叫法 | 指的是 |
|---|---|
| **键**（key） | 冒号左边，比如 `"hp"` |
| **值**（value） | 冒号右边，比如 `340` |
| **键值对** | 一整组 |

空字典是一对空大括号：

```python runnable 空字典
role = {}
print(role)
print(len(role))
```

`len()` 数的是**有几个键值对**。

---

## 📌 知识卡 3 · 取值、改值、新增

```python runnable 三种操作
role = {"name": "星野樱", "hp": 340}

print(role["name"])          # 取

role["hp"] = 500             # 改
print(role["hp"])

role["mp"] = 180             # 新增（键不存在就是新增）
print(role)
```

⚠️ **改和新增写法一样** —— 键在就是改，键不在就是新增。
这跟列表很不同：列表 `lst[10] = x` 会报错，字典不会。

取一个**不存在**的键会报错：

```python runnable 键不存在会报错
role = {"name": "星野樱"}
print(role["hp"])
```

这个 `KeyError` 派森酱会翻译给你看 ✨

---

## 📌 知识卡 4 · `.get()` —— 安全地取 ⭐

```python runnable get 取不到也不崩
role = {"name": "星野樱", "hp": 340}

print(role.get("hp"))
print(role.get("mp"))
print(role.get("mp", 0))
```

- `role.get("mp")` → 没有就给 `None`，**不报错**
- `role.get("mp", 0)` → 没有就给你 `0`（默认值）

也可以用 `in` 先检查（跟列表一样）：

```python runnable in 查的是「键」
role = {"name": "星野樱", "hp": 340}

print("hp" in role)
print("mp" in role)
print("星野樱" in role)
```

⚠️ 注意最后一行：**`in` 查的是键，不是值！**

> 🧠 什么时候用哪个：
> **确定该有 → 用 `[]`**（没有就该报错，好早点发现 bug）
> **可能没有 → 用 `.get(键, 默认值)`**

---

## 📌 知识卡 5 · 值可以是任何东西

```python runnable 值什么都能装
role = {
    "name": "星野樱",
    "level": 12,
    "alive": True,
    "skills": ["樱花斩", "结界术"],
    "hp": 340,
}

print(role["skills"])
print(role["skills"][0])
print(len(role["skills"]))
```

`role["skills"]` 是个**列表**，所以后面还能接 `[0]`。
「字典里装列表」这种嵌套，第 31 天会专门讲。

⚠️ 但**键**有讲究：一般用字符串，而且**不能重复**：

```python runnable 键重复会被覆盖
role = {"hp": 340, "hp": 999}
print(role)
```

后面的把前面的顶掉了 —— 跟变量赋值一个道理。

---

## 📌 知识卡 6 · 删除

```python runnable 两种删法
role = {"name": "星野樱", "hp": 340, "debuff": "中毒"}

del role["debuff"]
print(role)

removed = role.pop("hp")
print(f"移除了 hp，它的值是 {removed}")
print(role)
```

`.pop()` 跟列表的一样 —— **删掉并把值交给你**。

---

## 🛠 今天的任务 · 角色档案

做一个角色档案系统：

| 要求 | 说明 |
|---|---|
| 建一个角色字典 `role` | 至少包含 `name` `level` `hp` `mp` `element` 五个键 |
| 逐行打印档案 | `姓名：星野樱` 这样 |
| 修改一个属性 | 比如让 hp 变成 500，改完再打印 |
| 新增一个属性 | 比如加上 `title`（称号），加完再打印 |
| 用 `len()` 报出有几项属性 | |
| 问玩家想查哪一项 | `input()` |
| 用 `.get()` 或 `in` 安全查询 | 查不到要提示「档案里没有这一项」 |
| 删掉一项并报出被删的值 | 用 `.pop()` |

> 💡 判题会查一个**存在**的键和一个**不存在**的键，两种都不能崩。
