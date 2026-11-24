NEEDED = ["name", "level", "hp", "mp"]


def has_all_vars(ctx):
    return all(v in ctx["ns"] for v in NEEDED)


def _shows(ctx, var):
    if var not in ctx["ns"]:
        return False
    return str(ctx["ns"][var]) in ctx["stdout"]


def shows_name(ctx):
    return _shows(ctx, "name")


def shows_level(ctx):
    return _shows(ctx, "level")


def shows_hp_mp(ctx):
    return _shows(ctx, "hp") and _shows(ctx, "mp")


CHECKS = [
    {
        "id": "vars",
        "desc": "造了 name / level / hp / mp 四个变量",
        "type": "custom", "fn": "has_all_vars",
        "fail": "四个变量名要和要求的一模一样（全小写）：`name`、`level`、`hp`、`mp`",
    },
    {
        "id": "fstring",
        "desc": "用上了 f-string",
        "type": "ast_has", "node": "fstring", "min": 1,
        "fail": "引号前面加个 `f`，然后用 `{}` 把变量括起来，像这样：`print(f\"姓名：{name}\")`",
    },
    {
        "id": "show-name",
        "desc": "面板上显示了名字",
        "type": "custom", "fn": "shows_name",
        "fail": "输出里没看到 `name` 盒子里的内容。是不是漏写了 `{name}`？",
    },
    {
        "id": "show-level",
        "desc": "面板上显示了等级",
        "type": "custom", "fn": "shows_level",
        "fail": "等级那一行还没写，试试 `print(f\"等级：Lv.{level}\")`",
    },
    {
        "id": "show-hp-mp",
        "desc": "面板上显示了 HP 和 MP",
        "type": "custom", "fn": "shows_hp_mp",
        "fail": "生命和魔力两个数字都要出现在面板上哦",
    },
    {
        "id": "prints",
        "desc": "至少写了 5 个 print",
        "type": "ast_calls", "name": "print", "min": 5,
        "fail": "面板至少要 5 行：上边框、姓名、等级、HP、MP、下边框",
    },
]
