## 提示 1 · 先做难度选择

跟 Day 21 的输入校验一模一样：

```python
level = ""
while level not in ["1", "2", "3"]:
    print("  1) 简单   2) 普通   3) 困难")
    level = input("你的选择（1/2/3）：").strip()
    if level not in ["1", "2", "3"]:
        print("❓ 请输入 1、2 或 3\n")

if level == "1":
    top, chances = 50, 10
elif level == "2":
    top, chances = 100, 7
else:
    top, chances = 500, 12
```

先写到这里，跑一次，`print(top, chances)` 确认对了再往下。

## 提示 2 · 一局的完整流程

关键是循环条件里的两个条件（Day 13 的 `and`）：

```python
answer = random.randint(1, top)
guess = -1              # 一个肯定不等于答案的值
tries = 0

while guess != answer and tries < chances:
    tries += 1
    guess = int(input(f"第 {tries}/{chances} 次，猜："))
    if guess > answer:
        print("  📉 太大了")
    elif guess < answer:
        print("  📈 太小了")
```

循环结束后，**必须判断是怎么结束的**：

```python
if guess == answer:
    wins += 1
    print(f"🎉 猜对啦！这局用了 {tries} 次")
    if tries < best:
        best = tries
else:
    print(f"💀 次数用完了，答案是 {answer}")
```

## 提示 3 · 套上外层循环和战报

把上面整段**往右缩 4 格**，塞进外层循环：

```python
while True:
    games += 1
    answer = random.randint(1, top)
    guess = -1
    tries = 0

    while guess != answer and tries < chances:
        ...                       # 这里缩进 8 格

    if guess == answer:
        ...

    again = input("再来一局吗？(y/n)：").strip().lower()
    if again != "y":
        break
```

⚠️ 注意哪些东西该在**外层循环外面**：
`games`、`wins`、`best` 三个统计变量，还有难度选择 ——
它们只该做一次，放进循环里就每局都重置了（Day 17 的「归零在外」）。

战报写在所有循环外面（顶格）：

```python
print("📊 战报")
print(f"  总局数：{games}")
print(f"  胜利：{wins}    失败：{games - wins}")
if wins > 0:
    print(f"  最佳成绩：{best} 次猜中")
```
