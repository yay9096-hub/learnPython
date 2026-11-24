# Day 64 · 队伍数据可视化
import matplotlib.pyplot as plt

names = ["星野樱", "月见琉璃", "天野灯", "水城凛", "风见幽香"]
hp    = [340, 280, 310, 250, 360]
atk   = [88, 95, 72, 110, 90]

print("📊 === 队伍数据 === 📊")

# ---------- 文字版摘要 ----------
total_hp = sum(hp)
avg_atk = round(sum(atk) / len(atk), 1)
best_index = atk.index(max(atk))

print(f"  总血量：{total_hp}")
print(f"  平均攻击：{avg_atk}")
print(f"  最强：{names[best_index]}（{max(atk)}）")

# ---------- 画图 ----------
plt.figure(figsize=(9, 4))

# 左边：血量（名字长，横着画）
plt.subplot(1, 2, 1)
plt.barh(names, hp, color="#EC6FA9")
plt.title("队伍血量")
plt.xlabel("血量")

# 右边：攻击力（竖着画 + 标数值）
plt.subplot(1, 2, 2)
plt.bar(names, atk, color="#8B5CF6")
plt.title("队伍攻击力")
plt.ylabel("攻击力")
plt.ylim(0, 130)

for i in range(len(names)):
    plt.text(i, atk[i] + 3, str(atk[i]), ha="center")

plt.xticks(rotation=30, ha="right")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

print("\n✅ 图画好了，切到右边「📊 图表」看看")
