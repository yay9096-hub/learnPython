import ast
import json
import os

NEEDED = ["new_game", "load_game", "save_game", "show_scene",
          "move", "is_ending", "show_status"]

SETUP = """
import os
if os.path.exists("冒险存档.json"):
    os.remove("冒险存档.json")
"""


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def scenes_rich_enough(ctx):
    """地图至少 5 个场景，至少 2 个带道具，至少 1 个结局。"""
    scenes = ctx["ns"].get("SCENES")
    if not isinstance(scenes, dict) or len(scenes) < 5:
        return False
    with_item = sum(1 for s in scenes.values() if s.get("item"))
    endings = sum(1 for s in scenes.values() if not s.get("options"))
    return with_item >= 2 and endings >= 1


def scenes_link_back(ctx):
    """场景之间能来回走：至少有一对互通的场景。"""
    scenes = ctx["ns"].get("SCENES")
    if not isinstance(scenes, dict):
        return False
    for name, s in scenes.items():
        for target in (s.get("options") or {}).values():
            back = scenes.get(target, {}).get("options") or {}
            if name in back.values():
                return True
    return False


def new_game_shape(ctx):
    fn = ctx["ns"].get("new_game")
    if not callable(fn):
        return False
    s = fn()
    if not isinstance(s, dict):
        return False
    return (s.get("steps") == 0 and s.get("items") == []
            and isinstance(s.get("scene"), str)
            and s.get("visited") == [s["scene"]])


def load_missing_none(ctx):
    fn = ctx["ns"].get("load_game")
    if not callable(fn):
        return False
    try:
        return fn("肯定不存在_xyz.json") is None
    except Exception:
        return False


def load_broken_none(ctx):
    fn = ctx["ns"].get("load_game")
    if not callable(fn):
        return False
    name = "__判题坏档.json"
    try:
        with open(name, "w", encoding="utf-8") as f:
            f.write("{{{坏的")
        return fn(name) is None
    except Exception:
        return False
    finally:
        if os.path.exists(name):
            os.remove(name)


def handles_both_errors(ctx):
    src = ctx["code"]
    return "FileNotFoundError" in src and "JSONDecodeError" in src


def move_raises(ctx):
    """走一条不存在的路要抛 ValueError。"""
    mk = ctx["ns"].get("new_game")
    fn = ctx["ns"].get("move")
    if not callable(mk) or not callable(fn):
        return False
    s = mk()
    try:
        fn(s, "根本没有这条路")
        return False
    except ValueError:
        return True
    except Exception:
        return False


def move_counts_and_visits(ctx):
    """成功移动要 steps+1 并记录 visited。"""
    mk = ctx["ns"].get("new_game")
    fn = ctx["ns"].get("move")
    scenes = ctx["ns"].get("SCENES")
    if not callable(mk) or not callable(fn) or not isinstance(scenes, dict):
        return False
    s = mk()
    first = list(scenes[s["scene"]]["options"].keys())[0]
    target = scenes[s["scene"]]["options"][first]
    try:
        fn(s, first)
    except Exception:
        return False
    return (s["steps"] == 1 and s["scene"] == target
            and target in s["visited"])


def move_no_step_on_error(ctx):
    """走错路不该消耗步数。"""
    mk = ctx["ns"].get("new_game")
    fn = ctx["ns"].get("move")
    if not callable(mk) or not callable(fn):
        return False
    s = mk()
    try:
        fn(s, "不存在的路")
    except ValueError:
        pass
    except Exception:
        return False
    return s["steps"] == 0


def picks_up_items(ctx):
    """走到带道具的场景要自动捡起来，而且不会重复捡。"""
    mk = ctx["ns"].get("new_game")
    fn = ctx["ns"].get("move")
    scenes = ctx["ns"].get("SCENES")
    if not callable(mk) or not callable(fn) or not isinstance(scenes, dict):
        return False

    # 找一条能走到带道具场景的两步路径
    start = mk()["scene"]
    for c1, mid in (scenes[start].get("options") or {}).items():
        for c2, dest in (scenes.get(mid, {}).get("options") or {}).items():
            item = scenes.get(dest, {}).get("item")
            if not item:
                continue
            s = mk()
            try:
                fn(s, c1)
                fn(s, c2)
            except Exception:
                return False
            if s["items"].count(item) != 1:
                return False
            # 来回走一趟，验证不会重复捡
            back = None
            for k, v in (scenes[dest].get("options") or {}).items():
                if v == mid:
                    back = k
            if back is None:
                return True
            try:
                fn(s, back)
                fn(s, c2)
            except Exception:
                return False
            return s["items"].count(item) == 1
    return False


def is_ending_ok(ctx):
    fn = ctx["ns"].get("is_ending")
    scenes = ctx["ns"].get("SCENES")
    mk = ctx["ns"].get("new_game")
    if not callable(fn) or not isinstance(scenes, dict) or not callable(mk):
        return False
    ending = None
    for name, s in scenes.items():
        if not s.get("options"):
            ending = name
    if ending is None:
        return False
    s = mk()
    if fn(s):
        return False
    s["scene"] = ending
    return fn(s) is True


def saved_each_step(ctx):
    """跑完之后存档文件存在，而且记录的是玩家走到的位置。"""
    if not os.path.exists("冒险存档.json"):
        return False
    try:
        with open("冒险存档.json", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return False
    return isinstance(d, dict) and d.get("steps", 0) >= 3


def collected_items(ctx):
    """走的路线会经过两个道具场景。"""
    try:
        with open("冒险存档.json", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return False
    return len(d.get("items", [])) >= 2


def bad_choice_handled(ctx):
    return "没有" in ctx["stdout"] or "⚠" in ctx["stdout"]


def survived(ctx):
    return ctx["error"] is None


CASES = [
    {
        "setup": SETUP,
        # 进去 -> 爬树(捡羽毛徽章) -> 下树 -> 乱输 -> 找水源(捡月光石) -> 退出
        "stdin": ["进去", "爬树", "下树", "飞过去", "找水源", "退出"],
        "checks": [
            {"id": "defined", "desc": "七个函数都定义了",
             "type": "custom", "fn": "all_defined",
             "fail": "new_game / load_game / save_game / show_scene / "
                     "move / is_ending / show_status"},
            {"id": "map", "desc": "地图够丰富（5 场景 / 2 道具 / 1 结局）",
             "type": "custom", "fn": "scenes_rich_enough",
             "fail": "至少 5 个场景，其中至少 2 个带 `item`，至少 1 个 `options` 为空的结局"},
            {"id": "two-way", "desc": "场景之间能来回走",
             "type": "custom", "fn": "scenes_link_back",
             "fail": "至少要有一对场景互相连通，不能全是单向死路"},
            {"id": "new", "desc": "new_game 结构正确",
             "type": "custom", "fn": "new_game_shape",
             "fail": "`{\"scene\": 起点, \"items\": [], \"steps\": 0, \"visited\": [起点]}`"},
            {"id": "both-errors", "desc": "读档两种错都处理了",
             "type": "custom", "fn": "handles_both_errors",
             "fail": "要分别接住 `FileNotFoundError` 和 `json.JSONDecodeError`"},
            {"id": "missing", "desc": "没有存档时返回 None",
             "type": "custom", "fn": "load_missing_none",
             "fail": "文件不存在要返回 None 并提示一句"},
            {"id": "broken", "desc": "存档损坏时也返回 None",
             "type": "custom", "fn": "load_broken_none",
             "fail": "内容不是合法 json 时同样要兜住"},
            {"id": "move-raise", "desc": "走不存在的路会抛错",
             "type": "custom", "fn": "move_raises",
             "fail": "`move` 里 `if choice not in scene[\"options\"]: raise ValueError(...)`"},
            {"id": "move-count", "desc": "成功移动会记步数和足迹",
             "type": "custom", "fn": "move_counts_and_visits",
             "fail": "移动成功要 `steps + 1`，新地方要加进 `visited`"},
            {"id": "no-step", "desc": "走错路不消耗步数",
             "type": "custom", "fn": "move_no_step_on_error",
             "fail": "抛错要在改 steps **之前** —— 输错选项不该惩罚玩家"},
            {"id": "items", "desc": "自动捡道具且不重复捡",
             "type": "custom", "fn": "picks_up_items",
             "fail": "到了带 `item` 的场景要自动捡起来。"
                     "但**同一个道具来回走不能捡两次** —— 加之前先用 `in` 判断"},
            {"id": "ending", "desc": "is_ending 判断正确",
             "type": "custom", "fn": "is_ending_ok",
             "fail": "当前场景的 `options` 为空就是结局"},
            {"id": "bad-choice", "desc": "输错选项有提示",
             "type": "custom", "fn": "bad_choice_handled",
             "fail": "主循环里用 `try` 接住 `ValueError`，提示之后 `continue`"},
            {"id": "saved", "desc": "每一步都存了盘",
             "type": "custom", "fn": "saved_each_step",
             "fail": "每次 `move` 成功之后立刻 `save_game` —— "
                     "这样任何时候关掉都不丢进度",
             },
            {"id": "collected", "desc": "存档里记下了捡到的道具",
             "type": "custom", "fn": "collected_items",
             "fail": "这条路线会经过两个带道具的场景，存档的 `items` 里应该有两件"},
            {"id": "survive", "desc": "全程没有崩溃",
             "type": "custom", "fn": "survived",
             "fail": "输错选项、没有存档，两种情况都要撑住"},
        ],
    },
    {
        "setup": SETUP,
        "stdin": ["回头"],
        "checks": [
            {"id": "ending-flow", "desc": "走到结局会通关",
             "type": "stdout_contains", "value": "冒险完成",
             "fail": "走到 `options` 为空的场景时，打印通关信息并 `show_status`"},
        ],
    },
]
