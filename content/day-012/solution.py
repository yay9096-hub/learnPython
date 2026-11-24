# Day 12 · 属性克制判定
# 克制关系：火克风、风克水、水克火

print("⚔️ === 属性克制判定器 === ⚔️")

mine = input("你的属性（火/水/风）：")
enemy = input("对手属性（火/水/风）：")

# 先把不认识的属性挡在外面，后面的判断就干净了
if mine not in ["火", "水", "风"] or enemy not in ["火", "水", "风"]:
    print("❓ 我不认识这个属性，只能是 火 / 水 / 风")
elif mine == enemy:
    print(f"🤝 都是{mine}属性，平局！")
elif mine == "火" and enemy == "风":
    print("🔥 火克风 —— 你占优势！")
elif mine == "风" and enemy == "水":
    print("🌪 风克水 —— 你占优势！")
elif mine == "水" and enemy == "火":
    print("💧 水克火 —— 你占优势！")
else:
    print("💀 属性被克，你处于劣势……")
