def has_comment(ctx):
    """注释不会出现在语法树里，只能直接翻源码。"""
    for line in ctx["code"].splitlines():
        stripped = line.strip()
        if stripped.startswith("#") and len(stripped) > 2:
            return True
        if "#" in line and not line.strip().startswith("#"):
            after = line.split("#", 1)[1].strip()
            if after:
                return True
    return False


CHECKS = [
    {
        "id": "prints",
        "desc": "至少写了 5 个 print",
        "type": "ast_calls", "name": "print", "min": 5,
        "fail": "数一数你写了几个 print？出场卡至少要 5 行哦",
    },
    {
        "id": "border",
        "desc": "卡片有分隔线",
        "type": "stdout_regex", "pattern": "[=\-─★☆*~+#]{6,}",
        "fail": "分隔线要至少 6 个连着的符号，比如 `==============`",
    },
    {
        "id": "name",
        "desc": "写了「姓名：」",
        "type": "stdout_regex", "pattern": "姓名\s*[:：]\s*\S",
        "fail": "要有一行长这样：`姓名：你编的名字`（冒号后面别空着）",
    },
    {
        "id": "title",
        "desc": "写了「称号：」",
        "type": "stdout_regex", "pattern": "称号\s*[:：]\s*\S",
        "fail": "还差「称号：」那一行 —— 越中二越好 ✨",
    },
    {
        "id": "quote",
        "desc": "写了「台词：」",
        "type": "stdout_regex", "pattern": "台词\s*[:：]\s*\S",
        "fail": "还差「台词：」那一行，给你的角色一句出场白！",
    },
    {
        "id": "comment",
        "desc": "至少写了一句注释",
        "type": "custom", "fn": "has_comment",
        "fail": "用 `#` 写一句说明吧，比如 `# 这是我的角色卡`",
    },
]
