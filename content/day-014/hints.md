## 提示 1 · 循环三件套先摆好

写 `while` 之前先问自己三个问题：

1. **条件里用到哪个变量？** → `guess`
2. **进循环前它有值吗？** → starter 里已经写了 `guess = 0`
3. **循环里有没有改它？** → 每次 `input()` 都会给它新值 ✓

三件套齐了才不会死循环。

```python
while guess != answer:
    guess = int(input("猜一个数字："))
```

念一遍：「**只要**猜的还不等于答案，**就一直**问」。

## 提示 2 · 把 if 装进 while 里

注意缩进层次 —— `while` 里缩 4 格，`if` 里再缩 4 格（一共 8 格）：

```python
while guess != answer:
    guess = int(input("猜一个数字："))
    count += 1

    if guess > answer:
        print("📉 太大了！再试试")
    elif guess < answer:
        print("📈 太小了！再试试")
```

⚠️ 不需要写 `else: print("猜对了")` —— 猜对时循环条件自动变假，直接就退出了。
恭喜的话写在循环**外面**。

## 提示 3 · 完整骨架

```python
import random

answer = random.randint(1, 100)
count = 0
guess = 0

print("🎯 我想好了一个 1~100 的数字，你猜！")

while guess != answer:
    guess = int(input("猜一个数字："))
    count += 1
    if guess > answer:
        print("📉 太大了！再试试")
    elif guess < answer:
        print("📈 太小了！再试试")

print(f"🎉 猜对啦！答案就是 {answer}，你一共用了 {count} 次")
```

最后那行**顶格写**（不缩进），因为它属于「循环结束之后」。
写在循环里面的话，每猜一次都会恭喜你一遍 😅
