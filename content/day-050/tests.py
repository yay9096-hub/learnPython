import ast
import json
import os

NEEDED = ["new_save", "save_game", "load_game",
          "add_member", "add_item", "show_save"]

SETUP = """
import os
for _n in ["存档.json", "损坏的存档.json"]:
    if os.path.exists(_n):
        os.remove(_n)
"""


def _funcs(ctx):
    return {n.name: n for n in ast.walk(ctx["tree"]) if isinstance(n, ast.FunctionDef)}


def all_defined(ctx):
    return all(f in _funcs(ctx) for f in NEEDED)


def uses_json(ctx):
    src = ctx["code"]
    return "json.dump" in src and "json.load" in src


def dump_params_ok(ctx):
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            if n.func.attr == "dump":
                names = {k.arg for k in n.keywords}
                if "ensure_ascii" in names and "indent" in names:
                    return True
    return False


def new_save_ok(ctx):
    fn = ctx["ns"].get("new_save")
    if not callable(fn):
        return False
    d = fn("测试玩家")
    if not isinstance(d, dict):
        return False
    return (d.get("player") == "测试玩家" and d.get("chapter") == 1
            and d.get("gold") == 100 and d.get("team") == []
            and d.get("items") == {})


def roundtrip_ok(ctx):
    save = ctx["ns"].get("save_game")
    load = ctx["ns"].get("load_game")
    if not callable(save) or not callable(load):
        return False
    name = "__判题往返.json"
    data = {"player": "小樱", "chapter": 3, "gold": 250,
            "team": [{"name": "星野樱", "hp": 340}],
            "items": {"药水": 5}}
    try:
        save(name, data)
        back = load(name)
    except Exception:
        return False
    finally:
        if os.path.exists(name):
            os.remove(name)
    if not isinstance(back, dict):
        return False
    return (back == data
            and isinstance(back["chapter"], int)
            and isinstance(back["team"], list)
            and isinstance(back["items"], dict))


def chinese_readable(ctx):
    save = ctx["ns"].get("save_game")
    if not callable(save):
        return False
    name = "__判题中文.json"
    try:
        save(name, {"name": "星野樱"})
        with open(name, encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return False
    finally:
        if os.path.exists(name):
            os.remove(name)
    return "星野樱" in text and (chr(92) + "u") not in text


def missing_returns_none(ctx):
    fn = ctx["ns"].get("load_game")
    if not callable(fn):
        return False
    try:
        return fn("肯定不存在的存档_xyz.json") is None
    except Exception:
        return False


def broken_returns_none(ctx):
    fn = ctx["ns"].get("load_game")
    if not callable(fn):
        return False
    name = "__判题损坏.json"
    try:
        with open(name, "w", encoding="utf-8") as f:
            f.write("{{{这不是 json")
        return fn(name) is None
    except Exception:
        return False
    finally:
        if os.path.exists(name):
            os.remove(name)


def handles_both_errors(ctx):
    src = ctx["code"]
    return "FileNotFoundError" in src and "JSONDecodeError" in src


def add_member_ok(ctx):
    mk = ctx["ns"].get("new_save")
    fn = ctx["ns"].get("add_member")
    if not callable(mk) or not callable(fn):
        return False
    d = mk("测试")
    fn(d, "甲", 100)
    fn(d, "乙", 200)
    return (len(d["team"]) == 2 and d["team"][0]["name"] == "甲"
            and d["team"][1]["hp"] == 200)


def add_item_accumulates(ctx):
    mk = ctx["ns"].get("new_save")
    fn = ctx["ns"].get("add_item")
    if not callable(mk) or not callable(fn):
        return False
    d = mk("测试")
    fn(d, "药水", 3)
    fn(d, "药水", 2)
    fn(d, "钥匙")
    return d["items"].get("药水") == 5 and d["items"].get("钥匙") == 1


def save_file_valid_json(ctx):
    if not os.path.exists("存档.json"):
        return False
    try:
        with open("存档.json", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return False
    return isinstance(d, dict) and "宝箱钥匙" in d.get("items", {})


def progressed(ctx):
    try:
        with open("存档.json", encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return False
    return d.get("chapter") == 2 and d.get("gold") == 150


def shown(ctx):
    out = ctx["stdout"]
    return "星野樱" in out and "月见琉璃" in out and "红药水" in out


def survived(ctx):
    return ctx["error"] is None and "全程没有崩溃" in ctx["stdout"]


CASES = [
    {
        "setup": SETUP,
        "stdin": ["宝箱钥匙"],
        "checks": [
            {"id": "defined", "desc": "六个函数都定义了",
             "type": "custom", "fn": "all_defined",
             "fail": "new_save / save_game / load_game / add_member / add_item / show_save"},
            {"id": "json", "desc": "用了 json.dump 和 json.load",
             "type": "custom", "fn": "uses_json",
             "fail": "别再自己拼字符串了 —— 用 `json.dump` 存、`json.load` 读"},
            {"id": "params", "desc": "json.dump 带了两个必要参数",
             "type": "custom", "fn": "dump_params_ok",
             "fail": "固定咒语：`json.dump(data, f, ensure_ascii=False, indent=2)`"},
            {"id": "chinese", "desc": "存出来的中文是中文",
             "type": "custom", "fn": "chinese_readable",
             "fail": "不写 `ensure_ascii=False`，中文会变成一串看不懂的转义码"},
            {"id": "new-save", "desc": "new_save 结构正确",
             "type": "custom", "fn": "new_save_ok",
             "fail": "chapter=1、gold=100、team=[]、items={}，键名照抄"},
            {"id": "roundtrip", "desc": "存了再读，数据和类型都没变",
             "type": "custom", "fn": "roundtrip_ok",
             "fail": "json 的价值就在这里 —— 数字读回来还是数字，列表还是列表"},
            {"id": "both-errors", "desc": "两种读档错误都处理了",
             "type": "custom", "fn": "handles_both_errors",
             "fail": "要分别接住 `FileNotFoundError` 和 `json.JSONDecodeError`"},
            {"id": "missing", "desc": "读不存在的存档返回 None",
             "type": "custom", "fn": "missing_returns_none",
             "fail": "文件不存在时返回 `None` 并提示一句"},
            {"id": "broken", "desc": "读损坏的存档也返回 None",
             "type": "custom", "fn": "broken_returns_none",
             "fail": "内容不是合法 json 时会抛 `json.JSONDecodeError`，要接住它"},
            {"id": "member", "desc": "add_member 正确加入队伍",
             "type": "custom", "fn": "add_member_ok",
             "fail": "往 `data[\"team\"]` 里 append 一个 name/hp 字典"},
            {"id": "item-acc", "desc": "同一道具加两次会累加",
             "type": "custom", "fn": "add_item_accumulates",
             "fail": "药水加 3 再加 2 应该是 **5**，不是 2。先用 `in` 判断有没有"},
            {"id": "progress", "desc": "章节 +1、金币 +50 都存进去了",
             "type": "custom", "fn": "progressed",
             "fail": "chapter 应该变成 2，gold 应该变成 150"},
            {"id": "file-ok", "desc": "最终存档是合法 json 且含玩家道具",
             "type": "custom", "fn": "save_file_valid_json",
             "fail": "玩家输入的道具要加进去并**再存一次盘**"},
            {"id": "shown", "desc": "读回来的存档打印完整",
             "type": "custom", "fn": "shown",
             "fail": "`show_save` 要把队伍成员和道具都列出来"},
            {"id": "survive", "desc": "全程没有崩溃",
             "type": "custom", "fn": "survived",
             "fail": "最后打印一句「全程没有崩溃」—— 包括读损坏存档那一步"},
        ],
    }
]
