# Day 39 · 角色属性生成器
import random


def roll_stats(level):
    """按等级随机生成三围，返回 (hp, mp, atk)。"""
    hp = random.randint(50, 100) + level * 20
    mp = random.randint(20, 60) + level * 10
    atk = random.randint(10, 30) + level * 5
    return hp, mp, atk


def judge_stats(hp, mp, atk):
    """按三围总和评级，返回 (评级, 总和)。"""
    total = hp + mp + atk
    if total >= 400:
        return "优秀", total
    if total >= 300:
        return "普通", total
    return "偏弱", total


def make_role(name, level):
    """造一个完整的角色字典。"""
    hp, mp, atk = roll_stats(level)
    rank, total = judge_stats(hp, mp, atk)
    return {
        "name": name,
        "level": level,
        "hp": hp,
        "mp": mp,
        "atk": atk,
        "total": total,
        "rank": rank,
    }


def check_name(name):
    """检查名字长度，返回 (是否合法, 说明文字)。"""
    if len(name) < 2:
        return False, "名字太短了，至少 2 个字"
    if len(name) > 8:
        return False, "名字太长了，最多 8 个字"
    return True, "名字可以用"


# ---------- 主流程 ----------
print("📦 === 属性生成器 === 📦")

hp, mp, atk = roll_stats(10)
print(f"  掷出属性：HP {hp} · MP {mp} · ATK {atk}")

rank, total = judge_stats(hp, mp, atk)
print(f"  总和 {total}，评级：{rank}")

print("\n--- 批量生成角色 ---")
roles = [
    make_role("星野樱", 12),
    make_role("月见琉璃", 8),
    make_role("路人甲", 1),
]

for r in roles:
    print(f"  {r['name']} Lv.{r['level']}  HP {r['hp']} MP {r['mp']} "
          f"ATK {r['atk']}  总和 {r['total']}  [{r['rank']}]")

print("\n--- 名字校验 ---")
for n in ["樱", "超级无敌宇宙第一魔法少女", "星野樱"]:
    ok, msg = check_name(n)
    mark = "✓" if ok else "✗"
    print(f"  {mark} 「{n}」→ {msg}")
