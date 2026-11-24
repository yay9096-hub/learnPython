# Day 54 · 带存档的文字冒险
import json

SAVE = "冒险存档.json"
START = "森林入口"

SCENES = {
    "森林入口": {
        "text": "你站在一片幽暗的森林前，风里有樱花的味道。",
        "options": {"进去": "森林深处", "回头": "村庄"},
    },
    "森林深处": {
        "text": "树影摇曳，远处传来水声。",
        "options": {"找水源": "小溪", "往回走": "森林入口", "爬树": "树顶"},
    },
    "小溪": {
        "text": "一条清澈的小溪，水底闪着微光。",
        "options": {"回去": "森林深处"},
        "item": "月光石",
    },
    "树顶": {
        "text": "从树顶能看到整片森林，鸟巢里有个亮晶晶的东西。",
        "options": {"下树": "森林深处"},
        "item": "羽毛徽章",
    },
    "村庄": {
        "text": "温暖的灯火，冒险结束了。欢迎回家 ✨",
        "options": {},
    },
}


def new_game():
    """开一局全新的冒险。"""
    return {"scene": START, "items": [], "steps": 0, "visited": [START]}


def load_game(filename):
    """读档。不存在或损坏都返回 None。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("  （还没有存档，开始新的冒险）")
        return None
    except json.JSONDecodeError:
        print("  （存档损坏了，只好重新开始）")
        return None


def save_game(filename, save):
    """把进度存进 json。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(save, f, ensure_ascii=False, indent=2)


def show_scene(save):
    """打印当前场景的描述和可以走的路。"""
    scene = SCENES[save["scene"]]
    print(f"\n📍 {save['scene']}")
    print(f"   {scene['text']}")
    if scene["options"]:
        print(f"   可以：{' / '.join(scene['options'].keys())}")


def move(save, choice):
    """按选项移动。选项不存在就抛错。"""
    scene = SCENES[save["scene"]]
    if choice not in scene["options"]:
        options = " / ".join(scene["options"].keys())
        raise ValueError(f"这里没有「{choice}」这条路，只能：{options}")

    save["scene"] = scene["options"][choice]
    save["steps"] = save["steps"] + 1

    if save["scene"] not in save["visited"]:
        save["visited"].append(save["scene"])

    item = SCENES[save["scene"]].get("item")
    if item is not None and item not in save["items"]:
        save["items"].append(item)
        print(f"   ✨ 你捡到了 {item}！")

    return save


def is_ending(save):
    """当前场景没有任何选项 = 结局。"""
    return len(SCENES[save["scene"]]["options"]) == 0


def show_status(save):
    """打印当前状态。"""
    print(f"   步数：{save['steps']}")
    print(f"   背包：{'、'.join(save['items']) if save['items'] else '（空）'}")
    print(f"   去过 {len(save['visited'])} 个地方")


# ---------- 主流程 ----------
print("🗺 === 樱之森的冒险 === 🗺")

save = load_game(SAVE)
if save is None:
    save = new_game()
else:
    print(f"  ✓ 读档成功，你在「{save['scene']}」，已走 {save['steps']} 步")

while True:
    show_scene(save)

    if is_ending(save):
        print("\n🎉 === 冒险完成 === 🎉")
        show_status(save)
        save_game(SAVE, save)
        break

    choice = input("   你选择：").strip()

    if choice == "退出":
        save_game(SAVE, save)
        print("   💾 已存档，下次接着玩 ✨")
        break

    try:
        move(save, choice)
    except ValueError as e:
        print(f"   ⚠️ {e}")
        continue

    save_game(SAVE, save)
