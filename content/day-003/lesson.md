# Day 3 · 伤害计算器

> 「属性面板做好了，可这些数字光摆着有什么用？
> 今天让它们动起来 —— 算算你这一刀砍下去，对面掉多少血。」

---

## 📌 知识卡 1 · Python 就是个超强计算器

数字**不加引号**，直接算就行。

```python runnable 四则运算
print(7 + 3)
print(7 - 3)
print(7 * 3)
print(7 / 3)
```

注意最后一行 —— 除法的结果是 `2.3333...`。

⚠️ **`/` 的结果永远是小数**，哪怕除得尽：

```python runnable 除得尽也是小数
print(10 / 2)
```

结果是 `5.0` 而不是 `5`。后面那个 `.0` 就是在提醒你「我是小数」。

---

## 📌 知识卡 2 · 两个游戏里超常用的符号

```python runnable 整除和取余
print(17 // 5)
print(17 % 5)
```

- `//` **整除** —— 只要整数部分，小数直接砍掉（不是四舍五入！）
- `%` **取余** —— 只要余数

游戏里这两个到处都是：

```python runnable 300 点经验能升几级？
exp = 340
per_level = 100

print(f"升了 {exp // per_level} 级")
print(f"还差 {per_level - exp % per_level} 点经验到下一级")
```

---

## 📌 知识卡 3 · 变量之间可以直接算

这才是重点 —— 算式里可以放**变量**，不用写死数字。

```python runnable 伤害 = 攻击力 - 防御力
atk = 88
defense = 25
damage = atk - defense
print(f"造成了 {damage} 点伤害！")
```

看第三行：`damage = atk - defense`

Python 的执行顺序是 **先算右边，再装进左边的盒子**。

> 🧠 这就是为什么 `level = level + 1` 不是「废话」：
> 先算出 `level + 1`，再把结果重新装回 `level`。这一招以后天天用。

```python runnable 升级 +1
level = 12
level = level + 1
print(level)
```

---

## 📌 知识卡 4 · 运算顺序和括号

跟数学课上一样：**先乘除，后加减**。想改顺序就加括号。

```python runnable 括号决定一切
print(10 + 2 * 3)
print((10 + 2) * 3)
```

伤害公式里这个特别容易搞错：

```python runnable 暴击该怎么算
atk = 100
defense = 20

print(atk * 2 - defense)
print(atk * 2 - defense * 2)
print((atk - defense) * 2)
```

三种写法，三个答案。**先想清楚公式，再写代码。**

---

## 📌 知识卡 5 · 小数太长怎么办

`round()` 可以四舍五入，第二个参数是保留几位小数。

```python runnable 保留一位小数
damage = 88 * 1.35
print(damage)
print(round(damage, 1))
print(round(damage))
```

---

## 🛠 今天的任务

做一个**伤害计算器**。已经给你准备好了三个变量，你来把公式补上。

伤害公式（战斗规则）：

```
普通攻击伤害 = 攻击力 - 防御力
暴击伤害     = (攻击力 - 防御力) × 暴击倍率
```

| 要求 | 说明 |
|---|---|
| 算出普通伤害 | 存进变量 `damage` |
| 算出暴击伤害 | 存进变量 `crit_damage`，并四舍五入保留 1 位小数 |
| 用 f-string 报告战况 | 两个伤害数字都要显示出来 |
| 至少用到 `-` 和 `*` | 减法和乘法都要出现在代码里 |
