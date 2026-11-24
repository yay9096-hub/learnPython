def name_trimmed(ctx):
    """测试输入的名字前后带空格，必须被 strip 掉才能存进 name。

    注意不能拿 stdout 判断 —— input() 的回显里本来就带着原始空格。
    """
    return str(ctx["ns"].get("name", "")) == "星野樱"


def stars_made(ctx):
    """找一个「同一个字符重复 3 次以上」的字符串 —— 变量叫什么无所谓。"""
    for k, v in ctx["ns"].items():
        if k.startswith("__") or not isinstance(v, str):
            continue
        s = v.strip()
        if len(s) >= 3 and len(set(s)) == 1:
            return True
    return False


CASES = [
    {
        "stdin": ["  星野樱  ", "fire"],
        "checks": [
            {
                "id": "inputs",
                "desc": "问了名字和属性两个问题",
                "type": "ast_calls", "name": "input", "min": 2,
                "fail": "要问两次：名字、属性英文",
            },
            {
                "id": "strip",
                "desc": "用 .strip() 削掉了名字两边的空格",
                "type": "custom", "fn": "name_trimmed",
                "fail": "在 `input(...)` 后面接一个 `.strip()` 把多余空格削掉，"
                        "结果存进名叫 `name` 的变量",
            },
            {
                "id": "upper",
                "desc": "属性变成了大写",
                "type": "stdout_contains", "value": "FIRE", "case_sensitive": True,
                "fail": "用 `.upper()` 把 `fire` 变成 `FIRE`",
            },
            {
                "id": "len",
                "desc": "用 len() 数出了名字的长度",
                "type": "ast_calls", "name": "len", "min": 1,
                "fail": "阶数要用 `len(name)` 数出来，不要自己数完直接写 3 😉",
            },
            {
                "id": "rank",
                "desc": "阶数算对了",
                "type": "value_present", "value": 3,
                "fail": "「星野樱」是 3 个字，所以阶数应该是 **3**。"
                        "记得先 `.strip()`，不然空格会被算进去（变量叫什么名字都行）",
            },
            {
                "id": "stars",
                "desc": "用重复生成了星星线",
                "type": "custom", "fn": "stars_made",
                "fail": "用 `\"★\" * 数字` 造一条星星线，至少 3 个（变量叫什么名字都行）",
            },
            {
                "id": "title",
                "desc": "称号里名字和阶数都出现了",
                "type": "stdout_contains", "value": ["星野樱", "3"],
                "fail": "最后的称号里要能看到名字和阶数",
            },
        ],
    }
]
