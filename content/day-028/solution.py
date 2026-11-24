# Day 28 · 弹幕分析器
danmaku = "牛啊 前排 牛啊 打卡 awsl 牛啊 前排 泪目 awsl 前排 牛啊 打卡"

print("💬 === 弹幕分析器 === 💬")

words = danmaku.split()
print(f"总共接收到 {len(words)} 条弹幕")

# ---------- 去重 ----------
unique = []
for w in words:
    if w not in unique:
        unique.append(w)

print(f"不重复的弹幕有 {len(unique)} 种\n")

# ---------- 逐个统计 ----------
print("--- 词频统计 ---")
best_word = ""
best_count = 0

for w in unique:
    n = words.count(w)
    bar = "█" * n
    print(f"  {w:<6} {bar} {n} 次")

    if n > best_count:
        best_count = n
        best_word = w

print("\n" + "─" * 30)
print(f"🏆 刷得最多的是「{best_word}」，共 {best_count} 次")
print(f"出现过的词：{' / '.join(unique)}")
