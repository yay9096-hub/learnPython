# Day 50 · 游戏存档系统
import json

SAVE = "存档.json"
BROKEN = "损坏的存档.json"


# TODO 1: new_save(player) -> 新存档字典
#   {"player": ..., "chapter": 1, "gold": 100, "team": [], "items": {}}


# TODO 2: save_game(filename, data)
#   json.dump(data, f, ensure_ascii=False, indent=2)


# TODO 3: load_game(filename) -> 存档字典 / None
#   FileNotFoundError -> 提示「还没有存档」，返回 None
#   json.JSONDecodeError -> 提示「存档损坏」，返回 None


# TODO 4: add_member(data, name, hp) -> 往 team 里加一个字典，返回 data


# TODO 5: add_item(data, item, count=1) -> 往 items 里加道具
#   已经有的要累加数量


# TODO 6: show_save(data) -> 打印玩家、章节、金币、队伍、道具


# ---------- 主流程 ----------
# TODO 7: 先 load_game（文件不存在），提示后用 new_save 造新档
# TODO 8: 加 2 个队员、3 种道具（其中一种加两次）
# TODO 9: 章节 +1、金币 +50
# TODO 10: save_game 存盘
# TODO 11: 再 load_game 读回来，show_save 打印
# TODO 12: 问玩家一个道具名，加进去再存一次
# TODO 13: 写一个损坏的 json 文件，load_game 读它，验证不崩
