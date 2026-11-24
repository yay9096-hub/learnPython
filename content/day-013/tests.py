def uses_and(ctx):
    import ast
    return any(isinstance(n.op, ast.And)
               for n in ast.walk(ctx["tree"]) if isinstance(n, ast.BoolOp))


def uses_in(ctx):
    import ast
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Compare):
            for op in n.ops:
                if isinstance(op, (ast.In, ast.NotIn)):
                    return True
    return False


def types_ok(ctx):
    ns = ctx["ns"]
    return isinstance(ns.get("age"), int) and isinstance(ns.get("mp"), int)


CASES = [
    {
        "stdin": ["16", "80", "火", "n"],
        "checks": [
            {
                "id": "and",
                "desc": "用 and 把条件拼起来了",
                "type": "custom", "fn": "uses_and",
                "fail": "四个条件要用 `and` 串成一句：`age >= 15 and mp >= 50 and ...`",
            },
            {
                "id": "in",
                "desc": "用 in 判断属性合法性",
                "type": "custom", "fn": "uses_in",
                "fail": "属性判断用 `element in [\"火\", \"水\", \"风\"]`，比写三个 or 清爽得多",
            },
            {
                "id": "types",
                "desc": "年龄和魔力转成了数字",
                "type": "custom", "fn": "types_ok",
                "fail": "`int(input(...))`，不转换就没法比大小",
            },
            {
                "id": "accept",
                "desc": "全达标时录取",
                "type": "stdout_contains", "value": "录取",
                "fail": "16 岁、80 魔力、火属性、无黑历史 —— 这是全达标，应该录取",
            },
        ],
    },
    {
        "stdin": ["12", "80", "火", "n"],
        "checks": [
            {
                "id": "age-no",
                "desc": "年龄不够时拒绝",
                "type": "stdout_contains", "value": ["拒绝", "年龄"],
                "fail": "12 岁不够 15，要拒绝并说明是「年龄」的问题",
            },
            {
                "id": "age-not-accept",
                "desc": "年龄不够就不该录取",
                "type": "stdout_not_contains", "value": "录取",
                "fail": "条件缺一条就不能录取 —— 检查 `and` 是不是漏了哪个条件",
            },
        ],
    },
    {
        "stdin": ["16", "80", "土", "n"],
        "checks": [
            {
                "id": "element-no",
                "desc": "属性不合法时拒绝",
                "type": "stdout_contains", "value": ["拒绝", "属性"],
                "fail": "「土」不在 火/水/风 里，要拒绝并说明是「属性」的问题",
            },
        ],
    },
    {
        "stdin": ["16", "80", "火", "y"],
        "checks": [
            {
                "id": "record-no",
                "desc": "有黑历史时拒绝",
                "type": "stdout_contains", "value": "拒绝",
                "fail": "`record` 是 `y` 表示有黑历史，要拒绝",
            },
            {
                "id": "record-not-accept",
                "desc": "有黑历史就不该录取",
                "type": "stdout_not_contains", "value": "录取",
                "fail": "别忘了把 `record != \"y\"` 也加进 `and` 里",
            },
        ],
    },
]
