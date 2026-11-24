# Day 13 · 入学资格审查
print("📋 === 派森学院 · 入学资格审查 === 📋")

age = int(input("年龄："))
mp = int(input("魔力值："))
element = input("属性（火/水/风）：")
record = input("有黑历史吗（y/n）：")

if age >= 15 and mp >= 50 and element in ["火", "水", "风"] and record != "y":
    print("🎓 恭喜！你被录取了")
    print(f"   {element}属性 · {age} 岁 · 魔力 {mp}")
elif age < 15:
    print(f"❌ 拒绝：年龄不够，要满 15 岁（你 {age} 岁）")
elif mp < 50:
    print(f"❌ 拒绝：魔力不足，要 50 点以上（你只有 {mp}）")
elif element not in ["火", "水", "风"]:
    print(f"❌ 拒绝：属性必须是 火/水/风 之一（你填了「{element}」）")
else:
    print("❌ 拒绝：有黑历史，本院概不收录")
