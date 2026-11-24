def role_is_dict(ctx):
    return isinstance(ctx["ns"].get("role"), dict)


def has_five_keys(ctx):
    r = ctx["ns"].get("role")
    if not isinstance(r, dict):
        return False
    return all(k in r for k in ["name", "level", "element"])


def hp_changed(ctx):
    """hp 被改成 500（后面没被删）。"""
    r = ctx["ns"].get("role")
    return isinstance(r, dict) and str(r.get("hp")) == "500"


def title_added(ctx):
    r = ctx["ns"].get("role")
    return isinstance(r, dict) and "title" in r


def mp_removed(ctx):
    r = ctx["ns"].get("role")
    return isinstance(r, dict) and "mp" not in r


def uses_pop(ctx):
    import ast
    return any(isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
               and n.func.attr == "pop" for n in ast.walk(ctx["tree"]))


def safe_lookup(ctx):
    """用了 in 检查或者 .get()。"""
    import ast
    code = ctx["code"]
    if ".get(" in code.replace(" ", ""):
        return True
    for n in ast.walk(ctx["tree"]):
        if isinstance(n, ast.Compare):
            for op in n.ops:
                if isinstance(op, (ast.In, ast.NotIn)):
                    return True
    return False


CASES = [
    {
        "stdin": ["element"],
        "checks": [
            {
                "id": "dict",
                "desc": "role 是一个字典",
                "type": "custom", "fn": "role_is_dict",
                "fail": "用大括号建字典：`role = {\"name\": \"星野樱\", ...}`",
            },
            {
                "id": "keys",
                "desc": "包含 name / level / element 等键",
                "type": "custom", "fn": "has_five_keys",
                "fail": "至少要有 `name`、`level`、`hp`、`mp`、`element` 五个键（键名照抄）",
            },
            {
                "id": "printed",
                "desc": "逐行打印了档案",
                "type": "stdout_lines_min", "value": 8,
                "fail": "每一项属性单独打印一行，别整个字典 print 完事",
            },
            {
                "id": "hp",
                "desc": "把 hp 改成了 500",
                "type": "custom", "fn": "hp_changed",
                "fail": "`role[\"hp\"] = 500` —— 键已存在，赋值就是修改",
            },
            {
                "id": "title",
                "desc": "新增了 title",
                "type": "custom", "fn": "title_added",
                "fail": "`role[\"title\"] = \"樱花剑姬\"` —— 键不存在，赋值就是新增",
            },
            {
                "id": "len",
                "desc": "用 len() 报出了属性个数",
                "type": "ast_calls", "name": "len", "min": 1,
                "fail": "`len(role)` 数的是有几个键值对",
            },
            {
                "id": "safe",
                "desc": "查询用了安全写法",
                "type": "custom", "fn": "safe_lookup",
                "fail": "查询要用 `if key in role:` 或者 `role.get(key)`，"
                        "直接 `role[key]` 查不到会报 KeyError",
            },
            {
                "id": "found",
                "desc": "查到了存在的键",
                "type": "stdout_contains", "value": "火",
                "fail": "查 `element` 应该能查到「火」",
            },
            {
                "id": "pop",
                "desc": "用 pop() 删掉了 mp",
                "type": "custom", "fn": "uses_pop",
                "fail": "用 `removed = role.pop(\"mp\")` 删除，它会把值交给你",
            },
            {
                "id": "removed",
                "desc": "mp 确实被删掉了",
                "type": "custom", "fn": "mp_removed",
                "fail": "删完之后 `role` 里不该还有 `mp` 这个键",
            },
        ],
    },
    {
        "stdin": ["身高"],
        "checks": [
            {
                "id": "not-found",
                "desc": "查不存在的键不会崩",
                "type": "stdout_contains", "value": "没有",
                "fail": "查一个档案里没有的项时，要提示「档案里没有这一项」而不是报错",
            },
        ],
    },
]
