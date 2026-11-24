# Day 47 · 我的日记本

DIARY = "日记.txt"
TODO = "待办.txt"
CARD = "角色卡.txt"


def write_diary(filename, date, content):
    """用 w 模式写一篇日记。会清空文件原有内容。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"【{date}】\n")
        f.write(content + "\n\n")


def append_diary(filename, date, content):
    """用 a 模式追加一篇日记，保留之前写的。"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"【{date}】\n")
        f.write(content + "\n\n")


def write_lines(filename, lines):
    """把一个列表写成多行文本，每行末尾都有换行。"""
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


def save_role(filename, role):
    """把一个角色字典写成好看的多行文本。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== 角色卡 ===\n")
        for key, value in role.items():
            f.write(f"{key}: {value}\n")
        f.write("==============\n")


def show_file(filename):
    """把文件内容读回来打印，证明真的写进去了。"""
    with open(filename, encoding="utf-8") as f:
        print(f.read())


# ---------- 主流程 ----------
print("📝 === 我的日记本 === 📝")

write_diary(DIARY, "2026-09-02", "今天我的程序学会记住东西了！")
append_diary(DIARY, "2026-09-03", "写文件比我想的简单，就是别忘了 encoding。")
append_diary(DIARY, "2026-09-04", "刷新页面文件还在，有点感动。")

todo = ["复习 with open", "搞懂 w 和 a 的区别", "写完三篇日记", "明天学读文件"]
write_lines(TODO, todo)

role = {"姓名": "星野樱", "等级": 12, "血量": 340, "属性": "火"}
save_role(CARD, role)

extra = input("\n再写一句今天的心情：").strip()
append_diary(DIARY, "2026-09-04 补记", extra)

print("\n--- 日记.txt ---")
show_file(DIARY)

print("--- 待办.txt ---")
show_file(TODO)

print("--- 角色卡.txt ---")
show_file(CARD)

print("✅ 三个文件都写好了，刷新页面它们还在")
