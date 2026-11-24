def uses_if(ctx):
    """至少两个 if —— 口令一个、魔力一个。"""
    import ast
    return sum(1 for n in ast.walk(ctx["tree"]) if isinstance(n, ast.If)) >= 2


def uses_else(ctx):
    import ast
    return any(isinstance(n, ast.If) and n.orelse for n in ast.walk(ctx["tree"]))


def mp_is_int(ctx):
    return isinstance(ctx["ns"].get("mp"), int)


CASES = [
    {
        "stdin": ["sakura", "80"],
        "checks": [
            {
                "id": "if",
                "desc": "用了 if 做判断（至少两处）",
                "type": "custom", "fn": "uses_if",
                "fail": "口令一个 `if`、魔力一个 `if`，一共要两处判断",
            },
            {
                "id": "else",
                "desc": "用了 else 处理另一种情况",
                "type": "custom", "fn": "uses_else",
                "fail": "`else:` 要和 `if` 顶格对齐，后面同样有冒号",
            },
            {
                "id": "mp-int",
                "desc": "魔力值转成了数字",
                "type": "custom", "fn": "mp_is_int",
                "fail": "`mp = int(input(...))`，不转换就没法跟 50 比大小",
            },
            {
                "id": "pass-ok",
                "desc": "口令正确时放行",
                "type": "stdout_contains", "value": "欢迎",
                "fail": "口令是 `sakura` 时，输出里要有「欢迎」两个字",
            },
            {
                "id": "cast-ok",
                "desc": "魔力足够时能施法",
                "type": "stdout_contains", "value": "施法",
                "fail": "`mp >= 50` 时，输出里要有「施法」两个字",
            },
        ],
    },
    {
        "stdin": ["banana", "20"],
        "checks": [
            {
                "id": "pass-no",
                "desc": "口令错误时拦下",
                "type": "stdout_contains", "value": "拒绝",
                "fail": "口令不是 `sakura` 时，输出里要有「拒绝」两个字",
            },
            {
                "id": "cast-no",
                "desc": "魔力不足时提示",
                "type": "stdout_contains", "value": "不足",
                "fail": "`mp < 50` 时，输出里要有「不足」两个字",
            },
            {
                "id": "no-welcome",
                "desc": "口令错了就不该说欢迎",
                "type": "stdout_not_contains", "value": "欢迎",
                "fail": "口令错的时候还是放行了 —— 检查一下是不是把 `else` 那块写在 `if` 外面了",
            },
        ],
    },
]
