# Day 45 · 防呆输入 🛡

> 「你的程序到现在为止都有个共同的弱点：
> **用户一乱输，它就崩。**
>
> `int(input())` 遇到「abc」直接 ValueError 白屏退出。
> 今天学会接住这些错误，让程序稳稳地继续跑。」

---

## 📌 知识卡 1 · 先看看崩是什么样

```python runnable 这段一定会崩
age = int("abc")
print(age)
```

`ValueError` —— 派森酱会翻译给你看。

这 45 天里你已经见过好多种报错了：

| 报错 | 什么时候出现 |
|---|---|
| `ValueError` | 类型对但内容不对，比如 `int("abc")` |
| `TypeError` | 类型就不对，比如 `"字" + 1` |
| `ZeroDivisionError` | 除以 0 |
| `IndexError` | 列表编号越界 |
| `KeyError` | 字典里没这个键 |
| `NameError` | 变量没定义 |

以前你的对策是「**提前检查**」（Day 44 的 `isdigit()`）。
今天学另一种：**先干，出错了再处理**。

---

## 📌 知识卡 2 · `try` / `except` ⭐

```python runnable 接住错误
try:
    age = int("abc")
    print(f"年龄是 {age}")
except ValueError:
    print("这不是一个数字哦")

print("程序继续往下跑 ✨")
```

读法：

```
try:              ← 试着执行这一段
    可能出错的代码
except 错误类型:   ← 如果出了这种错，就跑这里
    出错时怎么办
```

**关键是最后那句 `程序继续往下跑` 真的执行了** —— 没有崩。

对比一下不用 try 的版本：

```python runnable 没有 try 就到此为止了
age = int("abc")
print("这一行永远跑不到")
```

---

## 📌 知识卡 3 · 用在 `input()` 上

```python runnable 防呆的年龄输入
text = input("你几岁了？")

try:
    age = int(text)
    print(f"明年你就 {age + 1} 岁啦")
except ValueError:
    print("要输入数字才行哦～")
```

试着输入 `abc`、`16`、什么都不输直接回车 —— 三种都不会崩。

⚠️ `try` 里面只放**可能出错的那几行**，别把整个程序都包进去：

```python runnable 包太多了（不好）
try:
    text = input("年龄：")
    age = int(text)
    print("欢迎")
    print("这些都不会出错的行也被包进来了")
except ValueError:
    print("出错了")
```

包太多有两个坏处：
出错时不知道是哪一行出的，而且可能**误接住**别的地方的 bug。

---

## 📌 知识卡 4 · 接住指定的错误类型 ⭐

```python runnable 两种错分开处理
def divide(a, b):
    """安全除法。"""
    try:
        return a / b
    except ZeroDivisionError:
        print("  除数不能是 0")
        return 0
    except TypeError:
        print("  这两个东西没法相除")
        return 0

print(divide(10, 2))
print(divide(10, 0))
print(divide(10, "abc"))
```

一个 `try` 可以跟**好几个 `except`**，各管各的错误类型。

⚠️ **别写光秃秃的 `except:`**：

```python runnable 什么都接住 = 掩盖 bug（不好）
try:
    nmae = "星野樱"      # 打错字了
    print(name)
except:
    print("出错了")
```

它把「变量名打错」这种**你应该修的 bug** 也一起吞了，
程序看起来正常，实际全是错的。

> 🧠 铁律：**只接住你预料到的那种错误。**
> 写 `except ValueError:`，不要写 `except:`。

---

## 📌 知识卡 5 · 拿到错误信息

```python runnable as e 拿到错误对象
try:
    n = int("abc")
except ValueError as e:
    print(f"出错了：{e}")
    print(f"错误类型：{type(e).__name__}")
```

`as e` 把错误对象接住，`e` 里有原始的错误信息。

调试时很有用，但**给用户看的提示要说人话** ——
`invalid literal for int()` 对她来说是天书（这正是派森酱做翻译器的原因 😉）。

---

## 📌 知识卡 6 · `else` 和 `finally`

```python runnable 四个部分的完整形态
def read_age(text):
    """把文字转成年龄，出错返回 None。"""
    try:
        age = int(text)
    except ValueError:
        print("  ✗ 不是数字")
        return None
    else:
        print("  ✓ 转换成功")
        return age
    finally:
        print("  （不管成功失败，这句都会跑）")

print(read_age("16"))
print(read_age("abc"))
```

| 部分 | 什么时候跑 |
|---|---|
| `try` | 总是先跑 |
| `except` | **只在出错时** |
| `else` | **只在没出错时** |
| `finally` | **永远都跑**（哪怕 return 了） |

`finally` 最常用来「收尾」—— 比如关文件（明天开始就用得上了）。

---

## 📌 知识卡 7 · 两种防御，各有各的场合

| 做法 | 写法 | 适合 |
|---|---|---|
| **提前检查** | `if text.isdigit():` | 条件简单、能一眼判断 |
| **try / except** | `try: int(text)` | 情况复杂、检查本身就很难写 |

比如「这个字符串能不能转成小数」——
用 `if` 判断要考虑负号、小数点、科学计数法……
而 `try: float(text)` 一行就完事了。

```python runnable float 用 try 比用 if 简单太多
def to_float(text):
    """能转就转，不能转返回 None。"""
    try:
        return float(text)
    except ValueError:
        return None

for s in ["3.14", "-2.5", "abc", "1e3", ""]:
    print(f"{s!r:>8} → {to_float(s)}")
```

---

## 🛠 今天的任务 · 防呆登记处

回收 Day 4 的入学登记处，这次**怎么乱输都不崩**：

| 函数 | 说明 |
|---|---|
| `to_int(text, default=0)` | 转整数，失败返回 default。用 try/except |
| `to_float(text, default=0.0)` | 转小数，失败返回 default |
| `safe_divide(a, b)` | 安全除法，除零返回 0 并提示 |
| `safe_get(data, key, default="未知")` | 从字典安全取值，接住 `KeyError` |
| `safe_index(lst, i, default=None)` | 从列表安全取值，接住 `IndexError` |
| `register()` | 问名字、年龄、身高，全部用安全转换，返回一个字典 |

主流程要求：

- 调用 `register()` 完成一次登记并打印结果
- 用 `safe_divide` 演示除以 0 不崩
- 用 `safe_get` 从字典取一个**不存在**的键
- 用 `safe_index` 从列表取一个**越界**的编号
- 全程一次都不能崩

> ⚠️ 每个 `except` 都要**写明错误类型**，不许写光秃秃的 `except:`。
> 判题会检查这一点。
