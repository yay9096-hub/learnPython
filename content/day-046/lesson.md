# Day 46 · 主动报错 🚨

> 「昨天学会了**接住**错误。今天学**主动扔出**错误。
>
> 听起来很奇怪 —— 好好的干嘛要报错？
> 因为有些时候，**报错比继续跑下去安全得多。**」

---

## 📌 知识卡 1 · 静悄悄的错误最可怕

看这个函数：

```python runnable 它「能跑」，但结果是错的
def create_role(name, hp):
    """造一个角色。"""
    return {"name": name, "hp": hp}

r = create_role("星野樱", -100)
print(r)
print(f"血量 {r['hp']} 的角色诞生了……？")
```

血量 **-100** 的角色被造出来了，程序**一点错都没报**。

然后这个坏数据会流到全世界：存进队伍、参与战斗、写进存档……
等你发现不对劲时，早就不知道是哪一步搞出来的了。

> 🧠 编程里有一条重要原则：
> **错误要在离出错点最近的地方被发现。**
> 拖得越久，找起来越难。

---

## 📌 知识卡 2 · `raise` —— 主动喊停

```python runnable 数据不合法就当场喊停
def create_role(name, hp):
    """造一个角色。血量必须是正数。"""
    if hp <= 0:
        raise ValueError(f"血量必须大于 0，你给的是 {hp}")
    return {"name": name, "hp": hp}

print(create_role("星野樱", 340))
print(create_role("坏数据", -100))
```

第二次调用直接抛错 —— **坏数据一步都没走出去**。

写法：

```
raise 错误类型("给人看的说明")
```

`raise` 跟 `return` 一样会**立刻结束函数**，后面的代码不执行。

---

## 📌 知识卡 3 · 挑一个合适的错误类型

用 Python 自带的就够了，选最贴切的那个：

| 类型 | 什么时候用 |
|---|---|
| `ValueError` | 类型对，但**值**不合法（负血量、空名字） |
| `TypeError` | **类型**就不对（该给数字却给了文字） |
| `KeyError` | 字典里找不到 |
| `IndexError` | 编号越界 |
| `RuntimeError` | 别的说不清的运行时问题 |

```python runnable 两种错分得清清楚楚
def set_hp(hp):
    """设置血量。"""
    if not isinstance(hp, int):
        raise TypeError(f"血量得是整数，你给的是 {type(hp).__name__}")
    if hp <= 0:
        raise ValueError(f"血量必须大于 0，你给的是 {hp}")
    return hp

print(set_hp(340))

try:
    set_hp("很多")
except TypeError as e:
    print(f"TypeError: {e}")

try:
    set_hp(-5)
except ValueError as e:
    print(f"ValueError: {e}")
```

> 💡 `isinstance(x, int)` 判断 x 是不是整数，比 `type(x) == int` 更常用。

---

## 📌 知识卡 4 · 错误信息要说人话 ⭐

```python runnable 三种质量的错误信息
def check_age(age):
    if age < 0:
        raise ValueError("错误")

def check_age2(age):
    if age < 0:
        raise ValueError("age < 0")

def check_age3(age):
    if age < 0:
        raise ValueError(f"年龄不能是负数（收到的是 {age}）")

for fn in [check_age, check_age2, check_age3]:
    try:
        fn(-5)
    except ValueError as e:
        print(f"  → {e}")
```

好的错误信息包含三样：**哪里错了、期望什么、实际收到了什么**。

第三个最好 —— 一看就知道毛病在哪，不用去翻源码。

---

## 📌 知识卡 5 · 异常会一层层往外传 ⭐

```python runnable 谁不接，谁就往上扔
def level3(x):
    """最里层：发现问题就抛。"""
    if x < 0:
        raise ValueError(f"不能是负数：{x}")
    return x * 2

def level2(x):
    """中间层：不管异常，让它穿过去。"""
    return level3(x) + 1

def level1(x):
    """外层：还是不管。"""
    return level2(x) * 10

print(level1(5))

try:
    level1(-3)
except ValueError as e:
    print(f"最外面接住了：{e}")
```

`level3` 抛的错，穿过 `level2`、`level1`，**一直传到最外面才被接住**。

这是个很有用的性质：

- **里层负责发现问题**（`raise`）
- **外层负责决定怎么办**（`try/except`）

中间那些层什么都不用写。

> 🧠 常见分工：
> **函数库里 `raise`，主流程里 `try`。**
> 因为「该怎么办」只有调用它的人知道 —— 是重试、用默认值、还是提示用户。

---

## 📌 知识卡 6 · 校验函数的标准写法

```python runnable 一次检查一个问题
MIN_NAME = 2
MAX_NAME = 8


def validate_name(name):
    """检查名字。有问题就抛 ValueError，没问题返回清理后的名字。"""
    if not isinstance(name, str):
        raise TypeError("名字得是文字")

    name = name.strip()
    if len(name) < MIN_NAME:
        raise ValueError(f"名字太短了，至少 {MIN_NAME} 个字（你给的是「{name}」）")
    if len(name) > MAX_NAME:
        raise ValueError(f"名字太长了，最多 {MAX_NAME} 个字（你给了 {len(name)} 个）")
    return name


print(validate_name("  星野樱  "))

for bad in ["樱", "超级无敌宇宙第一魔法少女"]:
    try:
        validate_name(bad)
    except ValueError as e:
        print(f"  ✗ {e}")
```

注意它**既校验又清理**：通过时返回 `.strip()` 之后的干净名字。

---

## 🛠 今天的任务 · 严格的登记处

回收 Day 45 的登记处，这次改成「**里层 raise，外层 try**」的专业写法：

| 函数 | 说明 |
|---|---|
| `validate_name(name)` | 长度 2~8。不合法抛 `ValueError`，合法返回 strip 后的名字 |
| `validate_age(age)` | 必须是 int 且 0~120。类型不对抛 `TypeError`，范围不对抛 `ValueError` |
| `validate_element(el)` | 必须在 火/水/风/雷 里。不合法抛 `ValueError`，信息里要列出可选值 |
| `create_role(name, age, element)` | 调用上面三个校验，全过才返回字典 |
| `try_register(name, age, element)` | **包一层 try**，成功返回 `(True, 角色字典)`，失败返回 `(False, 错误信息)` |

主流程要求：

- 用**合法数据**调 `try_register` 一次，打印成功的角色
- 用**三种不同的非法数据**各调一次，把错误信息打印出来
- 问玩家输入一次，用 `try_register` 处理，成功失败都要有反馈
- 全程不能崩

> ⚠️ 五个校验/创建函数里**不许写 try** —— 它们只管 `raise`。
> `try` 只出现在 `try_register` 和主流程里。这就是「里层报错、外层处理」的分工。
