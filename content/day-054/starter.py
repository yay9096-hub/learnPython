# Day 54 · 带存档的文字冒险
import json

SAVE = "冒险存档.json"
START = "森林入口"

# 地图就是一个字典：场景名 -> {描述, 选项, 可捡的道具}
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


# TODO 1: new_game() -> {"scene": START, "items": [], "steps": 0, "visited": [START]}


# TODO 2: load_game(filename) -> 存档 / None（不存在和损坏各给一句提示）


# TODO 3: save_game(filename, save)


# TODO 4: show_scene(save) -> 打印当前场景的描述和可选项


# TODO 5: move(save, choice) -> 移动
#   选项不存在 -> raise ValueError
#   成功 -> steps+1、记录 visited、捡走 item


# TODO 6: is_ending(save) -> 当前场景没有选项就是结局


# TODO 7: show_status(save) -> 打印步数、背包、去过几个地方


# ---------- 主流程 ----------
# TODO 8: load_game，没有就 new_game
# TODO 9: 循环：显示场景 -> 问选择 -> move -> 存档
#         输入「退出」就存档结束
#         选项不存在要接住 ValueError 提示，且不消耗步数
# TODO 10: 走到结局要打印通关信息 + show_status
