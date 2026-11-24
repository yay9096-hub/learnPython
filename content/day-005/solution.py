# Day 5 · 中二称号生成器

print("✦ 称号生成器 · 启动 ✦")

name = input("请输入你的名字：").strip()
element = input("请输入属性英文（fire / water / wind）：").strip()

rank = len(name)
stars = "★" * rank

print(f"✧･ﾟ:*  {stars}  *:･ﾟ✧")
print(f"【{element.upper()} 之子】{name} · {rank} 阶魔导士")
print(f"✧･ﾟ:*  {stars}  *:･ﾟ✧")
