def enough_branches(ctx):
    """至少两个 elif —— 光靠 if/else 是做不出多分支的。"""
    import ast
    n = 0
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.If):
            # elif 在语法树里就是 orelse 里再套一个 If
            if len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
                n += 1
    return n >= 2


def has_else(ctx):
    import ast
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.If) and node.orelse:
            if not (len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If)):
                return True
    return False


CASES = [
    {
        "stdin": ["火", "风"],
        "checks": [
            {
                "id": "elif",
                "desc": "用了 elif 做多分支（至少两个）",
                "type": "custom", "fn": "enough_branches",
                "fail": "情况有四种以上，要用 `elif` 串起来，不能只写 if 和 else",
            },
            {
                "id": "else",
                "desc": "有 else 兜底",
                "type": "custom", "fn": "has_else",
                "fail": "最后要有一个 `else:`，兜住所有想不到的情况",
            },
            {
                "id": "win",
                "desc": "火 vs 风 判成优势",
                "type": "stdout_contains", "value": "优势",
                "fail": "火克风，这局你赢 —— 输出里要有「优势」两个字",
            },
        ],
    },
    {
        "stdin": ["水", "风"],
        "checks": [
            {
                "id": "lose",
                "desc": "水 vs 风 判成劣势",
                "type": "stdout_contains", "value": "劣势",
                "fail": "风克水，这局你被克 —— 输出里要有「劣势」两个字",
            },
            {
                "id": "lose-not-win",
                "desc": "被克的时候不该说优势",
                "type": "stdout_not_contains", "value": "优势",
                "fail": "同时出现了「优势」和「劣势」—— 检查一下是不是写成了好几个独立的 if",
            },
        ],
    },
    {
        "stdin": ["火", "火"],
        "checks": [
            {
                "id": "draw",
                "desc": "同属性判成平局",
                "type": "stdout_contains", "value": "平局",
                "fail": "两边属性一样时输出「平局」。这一条要放在克制判断**前面**",
            },
        ],
    },
    {
        "stdin": ["土", "火"],
        "checks": [
            {
                "id": "unknown",
                "desc": "不认识的属性有兜底",
                "type": "stdout_contains", "value": "不认识",
                "fail": "输入了「土」这种没定义的属性时，`else` 要说一句「不认识」",
            },
        ],
    },
]
