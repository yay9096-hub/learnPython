# Day 5 · 中二称号生成器

> 「每个魔法少女都需要一个羞耻度爆表的称号。
> 今天做一台机器 —— 输入名字和属性，自动帮你生成。」

目标长这样：

```
✧･ﾟ:*  ★★★  *:･ﾟ✧
【FIRE 之子】星野樱 · 三阶魔导士
✧･ﾟ:*  ★★★  *:･ﾟ✧
```

---

## 📌 知识卡 1 · `len()` —— 数一数有几个字

```python runnable 数字数
print(len("星野樱"))
print(len("Sakura"))
print(len(""))
```

中文一个字算 1，英文一个字母也算 1。空字符串是 0。

有了它就能玩点花样 —— 比如**名字越长，称号等级越高**：

```python runnable 名字长度决定阶数
name = "星野樱"
print(f"{name} 是 {len(name)} 阶魔导士")
```

---

## 📌 知识卡 2 · 字符串 × 数字 = 重复

这是 Python 一个特别可爱的设定：

```python runnable 重复的魔法
print("★" * 5)
print("=" * 20)
print("哈" * 3)
```

做分隔线再也不用一个个敲了：

```python runnable 用变量控制长度
n = 3
print("★" * n)
```

> ⚠️ 只能 **文字 × 数字**。`"★" * "3"` 会报错，因为两边都是文字。

---

## 📌 知识卡 3 · 字符串的「方法」

有些操作是**挂在字符串身上**的，写法是 `字符串.方法名()`，注意那个点。

```python runnable 大小写变换
word = "fire"
print(word.upper())
print("MAGIC".lower())
```

- `.upper()` 全变大写
- `.lower()` 全变小写

⚠️ 这些方法**不会改变原来的变量**，而是**返回一个新的**：

```python runnable 原来的没变哦
word = "fire"
word.upper()
print(word)

word = word.upper()
print(word)
```

第一次 print 还是小写 —— 因为你没把结果装回去。**必须用 `=` 接住**。

---

## 📌 知识卡 4 · 两个特别实用的方法

```python runnable strip 和 replace
messy = "   星野樱   "
print(f"[{messy}]")
print(f"[{messy.strip()}]")

s = "我是水属性"
print(s.replace("水", "火"))
```

- `.strip()` 把首尾的空格削掉 —— 处理 `input()` 拿回来的东西时特别有用，
  因为人打字很容易多按一个空格
- `.replace(旧的, 新的)` 替换

---

## 📌 知识卡 5 · 方法可以串起来用

```python runnable 一条龙处理
raw = "  fire  "
print(raw.strip().upper())
```

从左往右读：先 `.strip()` 削空格，再把结果 `.upper()` 变大写。

---

## 🛠 今天的任务

做一台**中二称号生成器**：

问两个问题 →

| 顺序 | 问什么 | 变量 |
|---|---|---|
| 1 | 名字 | `name` |
| 2 | 属性英文（如 fire / water / wind） | `element` |

然后输出称号，必须包含：

| 要求 | 说明 |
|---|---|
| 属性**大写** | 用 `.upper()`，`fire` → `FIRE` |
| 名字去掉多余空格 | 用 `.strip()` |
| 阶数 = 名字的长度 | 用 `len(name)` |
| 一条星星线 | 用 `"★" * 数字` 生成，至少 3 颗星 |
| 用 f-string 拼出来 | 老朋友了 |

> 阶数和星星线存进哪个变量都行，派森酱只看**算得对不对**。
> （名字要存进 `name`，因为要检查你有没有 `.strip()` 干净。）

> 💡 测试时派森酱会输入 `  星野樱  `（前后带空格）和 `fire`，
> 所以 `.strip()` 一定要写上，不然名字会歪掉～
