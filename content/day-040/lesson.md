# Day 40 · 血量陷阱 🕳

> 「今天这一课有点绕，但它解释了一个你**迟早会撞上**的怪现象：
>
> 『我明明在函数里把血量减了，为什么外面打印出来还是原来的？』
>
> 搞懂它，你以后能省下无数小时的抓狂时间。」

---

## 📌 知识卡 1 · 函数里的变量，出了函数就没了

```python runnable 局部变量
def battle():
    damage = 63
    print(f"函数里：{damage}")

battle()
print(damage)
```

`NameError` —— `damage` 是在函数里造的，**函数一结束它就消失了**。

这叫**局部变量**（local）：只在这个函数内部存在。

好处是：不同函数可以用同名变量，互不干扰。

```python runnable 同名也不打架
def a():
    x = "我是 a 里的 x"
    print(x)

def b():
    x = "我是 b 里的 x"
    print(x)

a()
b()
```

---

## 📌 知识卡 2 · 函数能「看见」外面的变量

```python runnable 只读：能看见
hp = 500

def show():
    print(f"当前血量：{hp}")

show()
```

能读到外面的 `hp` —— Python 找不到局部的，就往外找。

---

## 📌 知识卡 3 · ⚠️ 但改不动它（今天的重点）

```python runnable 陷阱来了（认真看这个）
hp = 500

def take_damage():
    hp = hp - 63
    print(f"函数里：{hp}")

take_damage()
print(f"函数外：{hp}")
```

`UnboundLocalError`！为什么？

因为 Python 看到函数里有 `hp = ...` 这个**赋值**，
就认定「`hp` 是这个函数的局部变量」。
于是 `hp - 63` 里的 `hp` 指的是那个**还没赋值的局部变量** —— 所以报错。

就算不报错的版本，也改不到外面：

```python runnable 改了个寂寞
hp = 500

def take_damage(hp):
    hp = hp - 63
    print(f"函数里：{hp}")

take_damage(hp)
print(f"函数外：{hp}")
```

函数里变成 437，外面**还是 500**。

> 🧠 原因：数字传进函数时，函数拿到的是**一份复制**。
> 改复制品，原件当然不变。

---

## 📌 知识卡 4 · 正确做法：用 `return` 交回来 ⭐

```python runnable 这才是对的
hp = 500

def take_damage(hp, damage):
    """返回扣血之后的新血量。"""
    return hp - damage

hp = take_damage(hp, 63)
print(f"第一次后：{hp}")

hp = take_damage(hp, 88)
print(f"第二次后：{hp}")
```

关键是最后要**用 `hp =` 接住**。

这就是 Day 37 学的 `return`，今天你终于知道**为什么非它不可**了。

---

## 📌 知识卡 5 · 但列表和字典不一样！⚠️

```python runnable 列表居然改动了
team = ["星野樱", "月见琉璃"]

def add_member(team, name):
    team.append(name)

add_member(team, "天野灯")
print(team)
```

**外面的列表真的变了！**

为什么跟数字不一样？

| 类型 | 传进函数时 | 改了会影响外面吗 |
|---|---|---|
| 数字 / 文字 / 元组 | 传的是**值的复制** | ❌ 不会 |
| **列表 / 字典 / 集合** | 传的是**同一个东西** | ✅ **会** |

打个比方：

- 数字像**一张纸的复印件** —— 你在复印件上涂改，原件没事
- 列表像**一个房间的钥匙** —— 你拿钥匙进去搬了家具，房间真的变了

Day 31 你已经见过这个现象了（`for m in team: m["hp"] += 50` 真的生效）。
今天知道原因了。

---

## 📌 知识卡 6 · 但「整个换掉」还是不行

```python runnable 换掉 vs 改内容
team = ["星野樱"]

def replace_all(team):
    team = ["全新阵容"]        # 整个换掉：只改了局部的名字
    print(f"函数里：{team}")

replace_all(team)
print(f"函数外：{team}")
```

```python runnable 改内容才有效
team = ["星野樱"]

def modify(team):
    team.append("月见琉璃")     # 改内容：真的生效
    print(f"函数里：{team}")

modify(team)
print(f"函数外：{team}")
```

区别在于：

- `team = [...]` —— **把局部名字指向一个新列表**，原来的没动
- `team.append(...)` —— **在原列表上动手**，外面看得见

> 🧠 一句话总结今天：
> **想让函数改外面的东西，要么 `return` 交回来，要么直接改列表/字典的内容。
> 给参数重新赋值，永远只影响函数内部。**

---

## 📌 知识卡 7 · `global`：能用，但别用

```python runnable global 强行改外面
hp = 500

def take_damage():
    global hp
    hp = hp - 63

take_damage()
print(hp)
```

`global` 声明「我要改的是外面那个」。**能用，但强烈不建议。**

因为一旦用了它，你看到 `take_damage()` 这一行，
**完全猜不到它会偷偷改掉哪些东西** —— 程序一大就成了灾难。

> 💡 行业惯例：**能用 `return` 就别用 `global`**。今天知道有这么个东西就行。

---

## 🛠 今天的任务 · 血量管理实验室

用三种方式实现「扣血」，亲手对比它们的区别：

| 函数 | 做法 | 预期结果 |
|---|---|---|
| `damage_wrong(hp, dmg)` | 内部 `hp = hp - dmg`，**不 return** | 外面的血量**不会变** |
| `damage_right(hp, dmg)` | `return hp - dmg` | 接住之后外面**会变** |
| `damage_dict(role, dmg)` | 改 `role["hp"]` | 不用 return，外面**也会变** |

还要写：

| 函数 | 说明 |
|---|---|
| `heal_team(team, amount)` | 传进来一个「角色字典的列表」，给每人加血，不用 return |
| `rename_wrong(name)` | 内部 `name = "新名字"`，演示改不动 |

主流程要求：

- 三种扣血各演示一次，**每次都打印函数调用前后的血量**
- 用 `heal_team` 给一支至少 3 人的队伍加血，加血前后各打印一次
- 用 `rename_wrong` 演示字符串改不动
- 打印一句你自己的结论（含「return」两个字）

> 💡 这一天的重点不是写出多复杂的代码，而是**亲眼看见三种行为的差别**。
