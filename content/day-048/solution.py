# Day 48 · 日记阅读器
DIARY = "我的日记.txt"

ENTRIES = [
    "2026-09-02 今天学会了写文件，程序终于能记住东西了",
    "2026-09-03 写文件比想象中简单，就是别忘了 encoding",
    "2026-09-04 刷新页面文件还在，有点感动",
    "2026-09-05 读文件也学会了，w 和 a 别搞混",
    "2026-09-06 明天要做错题本，感觉能派上大用场",
]


def build_diary(filename, entries):
    """把若干篇日记写进文件，每篇一行。"""
    with open(filename, "w", encoding="utf-8") as f:
        for line in entries:
            f.write(line + "\n")


def read_all(filename):
    """整个文件读成一个字符串。"""
    with open(filename, encoding="utf-8") as f:
        return f.read()


def read_lines(filename):
    """读成列表，每项已经 strip 过，空行不要。"""
    result = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                result.append(line)
    return result


def count_lines(filename):
    """有多少篇日记（非空行）。"""
    return len(read_lines(filename))


def count_chars(filename):
    """一共写了多少字（不算换行符）。"""
    total = 0
    for line in read_lines(filename):
        total += len(line)
    return total


def find_by_date(filename, date):
    """找出某一天的日记。找不到返回 None。"""
    for line in read_lines(filename):
        if line.startswith(date):
            return line
    return None


def search(filename, keyword):
    """返回所有含关键词的行。"""
    result = []
    for line in read_lines(filename):
        if keyword in line:
            result.append(line)
    return result


def show_numbered(filename):
    """带行号打印全部日记。"""
    for i, line in enumerate(read_lines(filename), start=1):
        print(f"  {i}. {line}")


# ---------- 主流程 ----------
print("📖 === 日记阅读器 === 📖")

build_diary(DIARY, ENTRIES)

print(f"\n共 {count_lines(DIARY)} 篇，一共写了 {count_chars(DIARY)} 个字")

print("\n--- 全部日记 ---")
show_numbered(DIARY)

print("\n--- 按日期查找 ---")
found = find_by_date(DIARY, "2026-09-04")
if found is None:
    print("  这一天没写")
else:
    print(f"  找到了：{found}")

missing = find_by_date(DIARY, "2020-01-01")
if missing is None:
    print("  2020-01-01：这一天没写")

keyword = input("\n想搜什么关键词？").strip()
hits = search(DIARY, keyword)
if len(hits) == 0:
    print(f"  没有找到含「{keyword}」的日记")
else:
    print(f"  找到 {len(hits)} 条：")
    for line in hits:
        print(f"    · {line}")
