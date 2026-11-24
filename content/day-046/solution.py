# Day 46 · 严格的登记处
ELEMENTS = ["火", "水", "风", "雷"]
MIN_NAME = 2
MAX_NAME = 8
MAX_AGE = 120


def validate_name(name):
    """检查名字。不合法就抛错，合法返回清理后的名字。"""
    if not isinstance(name, str):
        raise TypeError(f"名字得是文字，你给的是 {type(name).__name__}")

    name = name.strip()
    if len(name) < MIN_NAME:
        raise ValueError(f"名字太短了，至少 {MIN_NAME} 个字（你给的是「{name}」）")
    if len(name) > MAX_NAME:
        raise ValueError(f"名字太长了，最多 {MAX_NAME} 个字（你给了 {len(name)} 个）")
    return name


def validate_age(age):
    """检查年龄。必须是 0~120 的整数。"""
    if not isinstance(age, int):
        raise TypeError(f"年龄得是整数，你给的是 {type(age).__name__}")
    if age < 0:
        raise ValueError(f"年龄不能是负数（收到的是 {age}）")
    if age > MAX_AGE:
        raise ValueError(f"年龄不能超过 {MAX_AGE}（收到的是 {age}）")
    return age


def validate_element(el):
    """检查属性。必须是预设的几种之一。"""
    if el not in ELEMENTS:
        options = " / ".join(ELEMENTS)
        raise ValueError(f"不认识的属性「{el}」，只能是：{options}")
    return el


def create_role(name, age, element):
    """造一个角色。任何一项不合法都会抛错。"""
    return {
        "name": validate_name(name),
        "age": validate_age(age),
        "element": validate_element(element),
    }


def try_register(name, age, element):
    """安全地登记。成功返回 (True, 角色)，失败返回 (False, 错误说明)。"""
    try:
        role = create_role(name, age, element)
    except (ValueError, TypeError) as e:
        return False, str(e)
    return True, role


# ---------- 主流程 ----------
print("🚨 === 严格登记处 === 🚨")

print("\n--- 合法数据 ---")
ok, result = try_register("  星野樱  ", 16, "火")
if ok:
    print(f"  ✓ 登记成功：{result}")

print("\n--- 非法数据测试 ---")
bad_cases = [
    ("樱", 16, "火"),
    ("星野樱", -5, "火"),
    ("星野樱", 16, "土"),
]
for name, age, el in bad_cases:
    ok, result = try_register(name, age, el)
    if not ok:
        print(f"  ✗ {result}")

print("\n--- 轮到你了 ---")
in_name = input("名字：")
in_age_text = input("年龄：")
in_el = input("属性（火/水/风/雷）：").strip()

try:
    in_age = int(in_age_text)
except ValueError:
    in_age = in_age_text

ok, result = try_register(in_name, in_age, in_el)
if ok:
    print(f"  ✓ 欢迎入学，{result['name']}！")
else:
    print(f"  ✗ 登记失败：{result}")

print("\n✅ 全程没有崩溃")
