def f(a, b):
    c = a - b
    if c < 1:
        c = 1
    if c > 999:
        c = 999
    return c


def g(a, b):
    return round(f(a, b) * 1.5, 1)


def h(x):
    return x > 0


def k(x):
    if x > 400:
        return "健康"
    if x > 150:
        return "受伤"
    return "危险"


def p(n, x, y):
    print(f"  第 {n} 回合：造成 {x} 点，敌人剩 {y}")


def b(a, x, y):
    for i in range(3):
        d = f(a, y)
        x = x - d
        p(i + 1, d, x)
    return x


print("=== 战斗开始 ===")
print(f"普通伤害：{f(88, 25)}")
print(f"暴击伤害：{g(88, 25)}")
print(f"最低保底：{f(10, 99)}")

left = b(88, 500, 25)
print(f"敌人剩余：{left}")
print(f"还活着吗：{h(left)}")
print(f"状态：{k(left)}")
