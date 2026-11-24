# Day 29 · 角色档案
print("🗂 === 角色档案系统 === 🗂")

role = {
    "name": "星野樱",
    "level": 12,
    "hp": 340,
    "mp": 180,
    "element": "火",
}

print("--- 初始档案 ---")
print(f"姓名：{role['name']}")
print(f"等级：{role['level']}")
print(f"生命：{role['hp']}")
print(f"魔力：{role['mp']}")
print(f"属性：{role['element']}")

# ---------- 修改 ----------
role["hp"] = 500
print(f"\n⬆ 生命值提升到 {role['hp']}")

# ---------- 新增 ----------
role["title"] = "樱花剑姬"
print(f"✨ 获得称号：{role['title']}")

print(f"\n档案现在有 {len(role)} 项属性")

# ---------- 查询 ----------
key = input("\n想查哪一项？（name/level/hp/mp/element/title）").strip()

if key in role:
    print(f"🔎 {key} = {role[key]}")
else:
    print(f"🔎 档案里没有这一项：「{key}」")

# ---------- 删除 ----------
removed = role.pop("mp")
print(f"\n🗑 移除了 mp，它原来的值是 {removed}")
print(f"档案剩下 {len(role)} 项：{role}")
