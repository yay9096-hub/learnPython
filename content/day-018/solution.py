# Day 18 · 图案生成器四连

# ---------- ① 8×8 棋盘 ----------
print("=== 棋盘 ===")
for row in range(8):
    for col in range(8):
        if (row + col) % 2 == 0:
            print("⬛", end="")
        else:
            print("⬜", end="")
    print()

# ---------- ② 九九乘法表 ----------
print("=== 九九乘法表 ===")
for i in range(1, 10):
    for j in range(1, i + 1):
        print(f"{j}×{i}={i * j}", end="\t")
    print()

# ---------- ③ 菱形 ----------
print("=== 菱形 ===")
n = 5
for i in range(1, n + 1):
    print(" " * (n - i) + "★" * (2 * i - 1))
for i in range(n - 1, 0, -1):
    print(" " * (n - i) + "★" * (2 * i - 1))

# ---------- ④ 空心方框 ----------
print("=== 空心方框 ===")
size = 5
for row in range(size):
    for col in range(size):
        if row == 0 or row == size - 1 or col == 0 or col == size - 1:
            print("★", end="")
        else:
            print(" ", end="")
    print()
