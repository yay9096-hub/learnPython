# 答案被固定成 42，好让判题能按剧本喂猜测。
# judge.py 判完会自动把 random 还原，不影响她自己点「运行」时的随机性。
FIX42 = "import random\nrandom.randint = lambda a, b: 42\nrandom.randrange = lambda *a: 42\n"


def uses_while(ctx):
    import ast
    return any(isinstance(n, ast.While) for n in ast.walk(ctx["tree"]))


def counted(ctx):
    """猜了 7 次，就该有个变量记着 7。变量叫什么名字不重要。"""
    for k, v in ctx["ns"].items():
        if k.startswith("__") or isinstance(v, bool):
            continue
        if isinstance(v, int) and v == 7:
            return True
    return False


CASES = [
    {
        "setup": FIX42,
        "stdin": ["50", "42"],
        "checks": [
            {
                "id": "while",
                "desc": "用了 while 循环",
                "type": "custom", "fn": "uses_while",
                "fail": "要用 `while guess != answer:` 才能反复问下去",
            },
            {
                "id": "random",
                "desc": "用 random 生成了答案",
                "type": "ast_imports", "name": "random",
                "fail": "答案要用 `random.randint(1, 100)` 随机生成",
            },
            {
                "id": "input-in-loop",
                "desc": "循环里会重复提问",
                "type": "ast_calls", "name": "input", "min": 1,
                "fail": "`input()` 要写在 `while` 里面（缩进 4 格），写在外面就只会问一次",
            },
            {
                "id": "too-big",
                "desc": "猜大了会提示「太大」",
                "type": "stdout_contains", "value": "太大",
                "fail": "答案是 42，猜 50 应该提示「太大」",
            },
            {
                "id": "not-too-small",
                "desc": "猜大了不该说「太小」",
                "type": "stdout_not_contains", "value": "太小",
                "fail": "提示反了 —— `guess > answer` 时该说「太大」",
            },
            {
                "id": "win",
                "desc": "猜对了会恭喜",
                "type": "stdout_contains", "value": "猜对",
                "fail": "循环结束后要打印一句带「猜对」的话",
            },
        ],
    },
    {
        "setup": FIX42,
        "stdin": ["10", "42"],
        "checks": [
            {
                "id": "too-small",
                "desc": "猜小了会提示「太小」",
                "type": "stdout_contains", "value": "太小",
                "fail": "答案是 42，猜 10 应该提示「太小」",
            },
            {
                "id": "not-too-big",
                "desc": "猜小了不该说「太大」",
                "type": "stdout_not_contains", "value": "太大",
                "fail": "提示反了 —— `guess < answer` 时该说「太小」",
            },
        ],
    },
    {
        "setup": FIX42,
        "stdin": ["50", "25", "37", "43", "40", "41", "42"],
        "checks": [
            {
                "id": "count",
                "desc": "数对了猜的次数",
                "type": "custom", "fn": "counted",
                "fail": "这一局猜了 7 次。`count += 1` 要放在循环**里面**，"
                        "每问一次加一次（变量叫什么名字都行）",
            },
            {
                "id": "count-shown",
                "desc": "最后报出了次数",
                "type": "stdout_contains", "value": "7",
                "fail": "结束时用 f-string 把次数打印出来，比如 `你一共用了 {count} 次`",
            },
        ],
    },
]
