# Day 44 · 猜数字（函数版）
import random

# ⚠️ 下面五个函数里一个 print 都不要写

# TODO 1: pick_number(low, high) -> 随机整数


# TODO 2: get_difficulty(name) -> 返回两个值 (上限, 次数)
#   简单 -> (50, 8)   普通 -> (100, 7)   困难 -> (200, 6)
#   其它 -> 默认返回普通


# TODO 3: check_guess(guess, answer) -> "太大" / "太小" / "猜对了"


# TODO 4: is_valid(text, high) -> 返回两个值 (是否合法, 说明)
#   不是数字、超范围都算不合法


# TODO 5: make_hint(answer) -> 返回一句提示字符串（比如「是偶数」）


# ---------- 下面两个负责打印 ----------

# TODO 6: show_result(won, answer, used) -> 打印结局


# TODO 7: play(high, chances) -> 跑完一整局，返回 True/False
#   循环里：问输入 -> is_valid 校验（不合法不扣次数）
#          -> check_guess 判断 -> 猜对就 break


# ---------- 主流程 ----------
# TODO 8: 问难度 -> get_difficulty -> play -> 根据返回值打印总结
