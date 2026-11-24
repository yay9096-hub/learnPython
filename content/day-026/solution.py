# Day 26 · 抽卡记录分析
records = ["R", "SR", "R", "SSR", "R", "R", "SR", "SSR", "R", "SR", "SSR", "R"]

print("🔪 === 抽卡记录分析 === 🔪")
print(f"全部记录（{len(records)} 次）：{records}")
print("─" * 40)

recent = records[-5:]
earliest = records[:3]
reversed_records = records[::-1]
every_other = records[::2]
middle = records[4:8]
ssr_recent = recent.count("SSR")

print(f"最近 5 次：{recent}")
print(f"最早 3 次：{earliest}")
print(f"倒序全部：{reversed_records}")
print(f"每隔一个：{every_other}")
print(f"中间 4 次：{middle}")
print("─" * 40)
print(f"最近 5 次里出了 {ssr_recent} 个 SSR")
