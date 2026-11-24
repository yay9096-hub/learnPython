# Day 14 · 猜数字游戏 🎯

> 「今天这个，是每个学编程的人都会写的第一个游戏。
> 写完它，你就有一个**能给同学玩**的东西了。」

先看效果：

```
我想好了一个 1~100 的数字，你猜！
猜一个数字：50
太大了！再试试
猜一个数字：25
太小了！再试试
猜一个数字：37
🎉 猜对啦！你用了 3 次
```

关键在于：**程序会一直问下去**。这就需要循环。

---

## 📌 知识卡 1 · `while` —— 只要……就一直……

```python runnable 数到 5
count = 1

while count <= 5:
    print(f"第 {count} 次")
    count = count + 1

print("循环结束")
```

念一遍：「**只要** count 小于等于 5，**就一直**执行下面那块」。

写法跟 `if` 长得几乎一样：

```
while  条件 :
    要重复做的事
```

同样是**冒号 + 缩进**。

区别在于：

| | 做几次 |
|---|---|
| `if` | 条件成立，做**一次**，然后往下走 |
| `while` | 条件成立，做完**再回头检查**，成立就再做，直到不成立 |

---

## 📌 知识卡 2 · ⚠️ 死循环 —— 今天最容易踩的坑

把上面那段的最后一行删掉会怎样？

```
count = 1
while count <= 5:
    print(f"第 {count} 次")
    # count = count + 1   ← 删掉了
```

`count` 永远是 1，条件永远成立，程序**永远停不下来**。

> 🛡 别怕，这个网站扛得住 —— 输出超过 20 万字会自动拦下，
> 你也可以随时点红色的「■ 停止」。**放心大胆地试。**

**循环三件套，缺一不可：**

```python runnable 三件套齐全
count = 1              # ① 循环开始前，先准备好变量

while count <= 5:      # ② 条件里用到这个变量
    print(count)
    count = count + 1  # ③ 循环体里必须改变它，否则条件永远不变
```

写完 `while` 之后，**第一件事就是问自己：第 ③ 步写了吗？**

> 💡 `count = count + 1` 可以简写成 `count += 1`，意思完全一样，程序员都这么写。

```python runnable += 的简写
n = 10
n += 5
print(n)
n -= 3
print(n)
```

---

## 📌 知识卡 3 · 循环 + input：会对话的程序

把 `input()` 放进循环里，程序就会**反复问你**：

```python runnable 一直问到你说停（试试输入几次再输 stop）
answer = ""

while answer != "stop":
    answer = input("说点什么（输入 stop 结束）：")
    print(f"你说了：{answer}")

print("好的，再见！")
```

注意第一行 `answer = ""` —— 循环条件要用到 `answer`，
所以**进循环之前必须先让它存在**，否则第一次检查条件就会报 NameError。

---

## 📌 知识卡 4 · 循环里放 if：猜大猜小

现在把 `if` 装进 `while` 里，两个工具合体：

```python runnable 猜数字的核心（答案固定是 7）
answer = 7
guess = 0

while guess != answer:
    guess = int(input("猜一个 1~10 的数字："))
    if guess > answer:
        print("太大了")
    elif guess < answer:
        print("太小了")

print("🎉 猜对啦！")
```

看缩进层次：

- `while` 里的东西缩进 **4 格**
- `if` 里的东西缩进 **8 格**（4 + 4）

每嵌套一层，往右缩 4 格。这就是 Python 表达「谁归谁管」的方式。

---

## 📌 知识卡 5 · 计数器：数一数猜了几次

```python runnable 加个计数器
answer = 7
guess = 0
count = 0

while guess != answer:
    guess = int(input("猜一个 1~10 的数字："))
    count += 1
    if guess > answer:
        print("太大了")
    elif guess < answer:
        print("太小了")

print(f"🎉 猜对啦！你用了 {count} 次")
```

`count += 1` 放在循环里，转一圈加一次。这个模式叫**计数器**，以后到处都会用到。

---

## 📌 知识卡 6 · 让答案随机（回收 Day 10）

```python runnable 每次都不一样
import random

answer = random.randint(1, 100)
print(f"（偷偷告诉你答案是 {answer}，正式版要把这行删掉）")
```

---

## 🛠 今天的任务 · 猜数字游戏

| 要求 | 说明 |
|---|---|
| 用 `random.randint(1, 100)` 生成答案 | 存进 `answer` |
| 用 `while` 循环反复询问 | 猜对之前不许停 |
| 猜大了 → 提示 | 输出里有「太大」 |
| 猜小了 → 提示 | 输出里有「太小」 |
| 猜对了 → 恭喜并结束循环 | 输出里有「猜对」 |
| 统计猜了几次 | 存进 `count`，最后打印出来 |

> 💡 判题时派森酱会用**二分法**来猜（50 → 25 → 37…），
> 所以你的「太大/太小」提示必须是**对的**，否则它会猜不到 😉
>
> ⚠️ 记得 `int(input(...))` —— 拿到的是文字，不转换没法比大小。
