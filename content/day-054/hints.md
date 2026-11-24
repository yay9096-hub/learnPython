## 提示 1 · 地图是数据，不是代码

`SCENES` 已经给你了。**看懂它的结构**，今天就成功一半：

```python
"森林深处": {
    "text": "树影摇曳，远处传来水声。",
    "options": {"找水源": "小溪", "往回走": "森林入口", "爬树": "树顶"},
},
```

- `text` —— 打印给玩家看的描述
- `options` —— `{玩家输入的词: 要去的场景名}`
- `item` —— 可选，走到这里自动捡走

显示场景：

```python
def show_scene(save):
    """打印当前场景的描述和可以走的路。"""
    scene = SCENES[save["scene"]]
    print(f"\n📍 {save['scene']}")
    print(f"   {scene['text']}")
    if scene["options"]:
        print(f"   可以：{' / '.join(scene['options'].keys())}")
```

`scene["options"].keys()` 就是玩家能输入的那几个词（Day 30 学的）。

## 提示 2 · move 是今天的核心

```python
def move(save, choice):
    """按选项移动。选项不存在就抛错。"""
    scene = SCENES[save["scene"]]
    if choice not in scene["options"]:
        options = " / ".join(scene["options"].keys())
        raise ValueError(f"这里没有「{choice}」这条路，只能：{options}")

    save["scene"] = scene["options"][choice]      # 换场景
    save["steps"] = save["steps"] + 1             # 记步数

    if save["scene"] not in save["visited"]:      # 记足迹（不重复）
        save["visited"].append(save["scene"])

    item = SCENES[save["scene"]].get("item")
    if item is not None and item not in save["items"]:   # 捡道具（不重复）
        save["items"].append(item)
        print(f"   ✨ 你捡到了 {item}！")

    return save
```

三个「不重复」的判断都很重要：

- **`raise` 要写在改 steps 之前** —— 输错不该消耗步数
- `visited` 用 `not in` 判断，同一个地方去两次只记一次
- **道具也要 `not in` 判断** —— 判题专门验了「来回走不会捡两次同一件」

用 `.get("item")` 而不是 `["item"]` —— 没有道具的场景根本没这个键。

## 提示 3 · 主循环：每走一步就存

```python
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
        continue          # ← 不存档、不消耗步数，重新来一轮

    save_game(SAVE, save)  # ← 每走一步就存
```

**「每走一步就存盘」是这一天的灵魂** —— 玩家任何时候关掉浏览器都不丢进度。
这正是第五章存在的意义。
