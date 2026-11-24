# Day 50 · 游戏存档系统
import json

SAVE = "存档.json"
BROKEN = "损坏的存档.json"


def new_save(player):
    """造一份全新的存档。"""
    return {
        "player": player,
        "chapter": 1,
        "gold": 100,
        "team": [],
        "items": {},
    }


def save_game(filename, data):
    """把存档写进 json 文件。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_game(filename):
    """读档。文件不存在或格式损坏都返回 None。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("  （还没有存档）")
        return None
    except json.JSONDecodeError:
        print("  （存档文件损坏了）")
        return None


def add_member(data, name, hp):
    """往队伍里加一个成员。"""
    data["team"].append({"name": name, "hp": hp})
    return data


def add_item(data, item, count=1):
    """往背包里加道具。已经有的就累加数量。"""
    if item in data["items"]:
        data["items"][item] = data["items"][item] + count
    else:
        data["items"][item] = count
    return data


def show_save(data):
    """打印一份存档的全部内容。"""
    if data is None:
        print("  （没有可显示的存档）")
        return

    print(f"  玩家：{data['player']}")
    print(f"  章节：第 {data['chapter']} 章")
    print(f"  金币：{data['gold']}")

    print(f"  队伍（{len(data['team'])} 人）：")
    for m in data["team"]:
        print(f"    · {m['name']}  HP {m['hp']}")

    print(f"  道具（{len(data['items'])} 种）：")
    for name, count in data["items"].items():
        print(f"    · {name} × {count}")


# ---------- 主流程 ----------
print("💾 === 游戏存档系统 === 💾")

print("\n--- 尝试读档 ---")
data = load_game(SAVE)
if data is None:
    print("  开一份新档吧！")
    data = new_save("小樱")

add_member(data, "星野樱", 340)
add_member(data, "月见琉璃", 280)

add_item(data, "红药水", 3)
add_item(data, "钥匙")
add_item(data, "红药水", 2)
add_item(data, "宝石", 5)

data["chapter"] = data["chapter"] + 1
data["gold"] = data["gold"] + 50

save_game(SAVE, data)
print("\n  ✅ 已存盘")

print("\n--- 重新读档 ---")
loaded = load_game(SAVE)
show_save(loaded)

new_item = input("\n捡到了什么道具？").strip()
add_item(loaded, new_item)
save_game(SAVE, loaded)
print(f"  ✅ {new_item} 已收进背包并存盘")

print("\n--- 损坏存档测试 ---")
with open(BROKEN, "w", encoding="utf-8") as f:
    f.write("这不是 json{{{")
broken = load_game(BROKEN)
print(f"  读回来的是：{broken}")

print("\n✅ 全程没有崩溃")
