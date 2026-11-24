def types_ok(ctx):
    ns = ctx["ns"]
    return isinstance(ns.get("age"), int) and isinstance(ns.get("lucky"), int)


# 出生年份和学号用 value_present：只看算得对不对，不管她把结果存进哪个变量。
# 讲解里没规定这两个变量叫什么，为名字判她错说不过去。
# name / age / lucky 是讲解表格里点名要的，才用变量名去卡。

CASES = [
    {
        "stdin": ["星野樱", "16", "7"],
        "checks": [
            {
                "id": "inputs",
                "desc": "问了 3 个问题",
                "type": "ast_calls", "name": "input", "min": 3,
                "fail": "名字、年龄、幸运数字，一共要问三次哦",
            },
            {
                "id": "convert",
                "desc": "年龄和幸运数字转成了数字",
                "type": "custom", "fn": "types_ok",
                "fail": "`input()` 拿到的是文字，要用 `int()` 包一层才能拿来算数。"
                        "而且这两个要分别存进名叫 `age` 和 `lucky` 的变量",
            },
            {
                "id": "name",
                "desc": "学生证上有名字",
                "type": "stdout_contains", "value": "星野樱",
                "fail": "把 `{name}` 打印到学生证上",
            },
            {
                "id": "birth",
                "desc": "算对了出生年份",
                "type": "value_present", "value": 2010,
                "fail": "出生年份 = `2026 - age`。测试输入 16 岁，所以应该算出 **2010**。"
                        "（变量叫什么名字都行）",
            },
            {
                "id": "sid",
                "desc": "算对了学号",
                "type": "value_present", "value": 1607,
                "fail": "学号 = `age * 100 + lucky`。16 和 7 应该算出 **1607**。"
                        "（变量叫什么名字都行）",
            },
            {
                "id": "show-all",
                "desc": "学生证上四项信息齐全",
                "type": "stdout_contains", "value": ["星野樱", "16", "2010", "1607"],
                "fail": "名字、年龄、出生年份、学号，四样都要打印出来",
            },
        ],
    }
]
