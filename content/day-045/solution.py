# Day 45 · 防呆登记处


def to_int(text, default=0):
    """把文字转成整数。转不了就返回 default，不崩。"""
    try:
        return int(text)
    except ValueError:
        return default


def to_float(text, default=0.0):
    """把文字转成小数。转不了就返回 default。"""
    try:
        return float(text)
    except ValueError:
        return default


def safe_divide(a, b):
    """安全除法。除数为 0 时提示并返回 0。"""
    try:
        return a / b
    except ZeroDivisionError:
        print("  ⚠️ 除数不能是 0，先当作 0 处理")
        return 0


def safe_get(data, key, default="未知"):
    """从字典取值。没有这个键就返回 default。"""
    try:
        return data[key]
    except KeyError:
        return default


def safe_index(lst, i, default=None):
    """从列表取值。编号越界就返回 default。"""
    try:
        return lst[i]
    except IndexError:
        return default


def register():
    """完成一次入学登记，返回一个信息字典。乱输也不会崩。"""
    name = input("请输入你的名字：").strip()
    age = to_int(input("请输入你的年龄："))
    height = to_float(input("请输入你的身高（米）："))

    return {
        "name": name,
        "age": age,
        "height": height,
        "birth_year": 2026 - age,
    }


# ---------- 主流程 ----------
print("🛡 === 防呆入学登记处 === 🛡")

info = register()
print("\n--- 学生证 ---")
print(f"  姓名：{info['name']}")
print(f"  年龄：{info['age']}")
print(f"  身高：{info['height']} 米")
print(f"  出生年份：{info['birth_year']}")

print("\n--- 安全除法演示 ---")
print(f"  10 / 2 = {safe_divide(10, 2)}")
print(f"  10 / 0 = {safe_divide(10, 0)}")

print("\n--- 安全取值演示 ---")
role = {"name": "星野樱", "hp": 340}
print(f"  hp = {safe_get(role, 'hp')}")
print(f"  mp = {safe_get(role, 'mp')}")

team = ["星野樱", "月见琉璃"]
print(f"  第 1 个 = {safe_index(team, 0)}")
print(f"  第 9 个 = {safe_index(team, 9)}")

print("\n✅ 全程没有崩溃")
