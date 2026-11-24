# Day 44 · 猜数字（函数版）
import random

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


def is_valid(text, high):
    """校验输入，返回 (是否合法, 说明文字)。"""
    if not text.isdigit():
        return False, "这不是一个数字哦"
    number = int(text)
    if number < 1 or number > high:
        return False, f"要在 1 到 {high} 之间"
    return True, "可以"


def make_hint(answer):
    """给一句关于答案的提示。"""
    if answer % 2 == 0:
        return "悄悄告诉你：它是偶数"
    return "悄悄告诉你：它是奇数"


def show_result(won, answer, used):
    """打印这一局的结局。"""
    if won:
        print(f"🎉 猜对了！答案就是 {answer}，你用了 {used} 次")
    else:
        print(f"💀 次数用完了。答案是 {answer}")


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
            continue

        used = used + 1
        result = check_guess(int(text), answer)
        print(f"  → {result}")

        if result == "猜对了":
            won = True
            break

        if used == chances - 2:
            print(f"  💡 {make_hint(answer)}")

    show_result(won, answer, used)
    return won


# ---------- 主流程 ----------
print("🔢 === 猜数字 · 函数版 === 🔢")

level = input("选择难度（简单/普通/困难）：").strip()
high, chances = get_difficulty(level)

won = play(high, chances)

if won:
    print("下次试试更难的？")
else:
    print("再来一局吧，你一定行的 (๑•̀ㅂ•́)و")
