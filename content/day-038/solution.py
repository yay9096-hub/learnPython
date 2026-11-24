# Day 38 · 角色生成器


def create_role(name, hp=100, mp=50, atk=30, element="无", level=1):
    """造一个角色字典。除了名字，其余都有默认值。"""
    return {
        "name": name,
        "hp": hp,
        "mp": mp,
        "atk": atk,
        "element": element,
        "level": level,
        "skills": [],
    }


def show_role(role, width=20, char="█"):
    """打印角色卡，血条宽度和符号都可以换。"""
    filled = int(role["hp"] / 400 * width)
    if filled > width:
        filled = width
    bar = char * filled + "░" * (width - filled)
    name = role["name"]
    lv = role["level"]
    el = role["element"]
    print(f"  {name} Lv.{lv} [{el}]")
    print(f"    HP {bar} {role['hp']}")
    print(f"    MP {role['mp']}   ATK {role['atk']}")
    if role["skills"]:
        joined = "、".join(role["skills"])
        print(f"    技能：{joined}")


def add_skill(role, skill, skills=None):
    """给角色加一个技能。默认值用 None，避免可变默认值的坑。"""
    if skills is None:
        skills = role["skills"]
    skills.append(skill)
    role["skills"] = skills
    return role


# ---------- 主流程 ----------
print("🎛 === 角色生成器 === 🎛")

passerby = create_role("路人甲")
hero = create_role("星野樱", 340, 180, 88, "火", 12)
mage = create_role("月见琉璃", element="水", level=8)

add_skill(hero, "樱花斩")
add_skill(hero, "结界术")

show_role(passerby)
show_role(hero)
show_role(mage, width=30, char="=")
