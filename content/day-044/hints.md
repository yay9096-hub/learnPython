## 提示 1 · 先把五个「只算不打印」的写出来

这五个最简单，各自只有几行：

```python
DIFFICULTIES = {
    "简单": (50, 8),
    "普通": (100, 7),
    "困难": (200, 6),
}


def pick_number(low, high):
    """随机出一个 low..high 之间的整数。"""
    return random.randint(low, high)


def get_difficulty(name):
    """按难度名返回 (上限, 次数)。不认识的名字按普通算。"""
    if name in DIFFICULTIES:
        return DIFFICULTIES[name]
    return DIFFICULTIES["普通"]


def check_guess(guess, answer):
    """比较猜测和答案，返回 太大 / 太小 / 猜对了。"""
    if guess > answer:
        return "太大"
    if guess < answer:
        return "太小"
    return "猜对了"
```

用字典存难度表，比写一串 `if` 清爽（Day 30 学的）。

校验函数返回两个值：

```python
def is_valid(text, high):
    """校验输入，返回 (是否合法, 说明文字)。"""
    if not text.isdigit():
        return False, "这不是一个数字哦"
    number = int(text)
    if number < 1 or number > high:
        return False, f"要在 1 到 {high} 之间"
    return True, "可以"
```

> 💡 `"123".isdigit()` 返回 True，`"abc".isdigit()` 返回 False ——
> 比用 `try/except` 简单（异常要到第五章才学）。

## 提示 2 · play 是调度中心

```python
def play(high, chances):
    """跑完一整局，返回是否猜中。"""
    answer = pick_number(1, high)
    used = 0
    won = False

    print(f"我想好了一个 1 到 {high} 之间的数，你有 {chances} 次机会")

    while used < chances:
        text = input(f"第 {used + 1} 次，你猜：").strip()

        ok, why = is_valid(text, high)
        if not ok:
            print(f"  ⚠️ {why}（这次不算）")
            continue                    # ← 关键：跳过，不扣次数

        used = used + 1
        result = check_guess(int(text), answer)
        print(f"  → {result}")

        if result == "猜对了":
            won = True
            break

    show_result(won, answer, used)
    return won
```

三个关键点：

- **`continue` 在扣次数之前** —— 非法输入才不会浪费机会
- **`used = used + 1` 放在校验通过之后**
- **最后 `return won`**，主流程才知道结果

## 提示 3 · 提示和结局

快用完次数时给一句提示：

```python
        if used == chances - 2:
            print(f"  💡 {make_hint(answer)}")
```

（放在 `if result == "猜对了": break` 后面）

结局函数只管打印：

```python
def show_result(won, answer, used):
    """打印这一局的结局。"""
    if won:
        print(f"🎉 猜对了！答案就是 {answer}，你用了 {used} 次")
    else:
        print(f"💀 次数用完了。答案是 {answer}")
```

主流程串起来：

```python
level = input("选择难度（简单/普通/困难）：").strip()
high, chances = get_difficulty(level)      # 解包接住两个值

won = play(high, chances)

if won:
    print("下次试试更难的？")
else:
    print("再来一局吧，你一定行的 (๑•̀ㅂ•́)و")
```
