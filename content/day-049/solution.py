# Day 49 · 我的错题本
NOTES = "错题本.txt"
SEP = " | "


def load_notes(filename):
    """读全部错题。文件还不存在就返回空列表。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []


def add_note(filename, question, answer):
    """追加一条错题。a 模式会自动创建文件，不用检查。"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{question}{SEP}{answer}\n")


def count_notes(filename):
    """错题本里有几条。"""
    return len(load_notes(filename))


def search_notes(filename, keyword):
    """返回题目或答案里含关键词的记录。"""
    result = []
    for line in load_notes(filename):
        if keyword in line:
            result.append(line)
    return result


def show_notes(filename):
    """带编号显示全部错题。一条都没有时给个提示。"""
    notes = load_notes(filename)
    if len(notes) == 0:
        print("  📭 错题本还是空的，加油别错题 ✨")
        return
    for i, note in enumerate(notes, start=1):
        parts = note.split("|")
        question = parts[0].strip()
        answer = parts[1].strip() if len(parts) > 1 else ""
        print(f"  {i}. ❓ {question}")
        print(f"     ✅ {answer}")


def clear_notes(filename):
    """清空错题本，但文件保留。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")


# ---------- 主流程 ----------
print("📓 === 我的错题本 === 📓")

print("\n--- 第一次打开（文件还不存在）---")
show_notes(NOTES)

add_note(NOTES, "int 和 str 能直接相加吗", "不能，要先用 str() 转换")
add_note(NOTES, "列表的编号从几开始", "从 0 开始，最大编号是长度减 1")
add_note(NOTES, "sort() 返回什么", "什么都不返回，它直接改原列表")

print("\n--- 记了三条之后 ---")
show_notes(NOTES)
print(f"\n  一共 {count_notes(NOTES)} 条")

q = input("\n你今天错了什么题？").strip()
a = input("正确答案是什么？").strip()
add_note(NOTES, q, a)
print(f"  已记下，现在有 {count_notes(NOTES)} 条")

keyword = input("\n想复习哪方面？（输个关键词）").strip()
hits = search_notes(NOTES, keyword)
if len(hits) == 0:
    print(f"  没有找到含「{keyword}」的错题")
else:
    print(f"  找到 {len(hits)} 条：")
    for line in hits:
        print(f"    · {line}")

print("\n--- 清空之后 ---")
clear_notes(NOTES)
show_notes(NOTES)
print(f"  剩 {count_notes(NOTES)} 条")
