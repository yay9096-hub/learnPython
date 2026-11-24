# Day 52 · CSV 成绩单
SCORES = "成绩.csv"
RANKING = "排名.csv"
SUBJECTS = ["语文", "数学", "英语"]

RAW = [
    "姓名,语文,数学,英语",
    "星野樱,88,92,79",
    "月见琉璃,95,78,91",
    "天野灯,72,85,68",
    "水城凛,90,99,94",
    "夜刀神澪,65,71,82",
]


def write_lines_csv(filename, rows):
    """把若干行字符串写成 CSV 文件。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")


def read_csv(filename):
    """把 CSV 读成列表套字典。纯数字的字段自动转成 int。"""
    with open(filename, encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if len(lines) == 0:
        return []

    header = lines[0].split(",")
    rows = []
    for line in lines[1:]:
        parts = line.split(",")
        row = {}
        for key, value in zip(header, parts):
            value = value.strip()
            if value.isdigit():
                row[key] = int(value)
            else:
                row[key] = value
        rows.append(row)
    return rows


def add_total(rows):
    """给每一行加一个「总分」字段。"""
    for row in rows:
        total = 0
        for s in SUBJECTS:
            total += row[s]
        row["总分"] = total
    return rows


def subject_avg(rows, subject):
    """某一科的平均分，保留 1 位小数。空表返回 0。"""
    if len(rows) == 0:
        return 0
    total = 0
    for row in rows:
        total += row[subject]
    return round(total / len(rows), 1)


def top_student(rows):
    """总分最高的那一行。空表返回 None。"""
    if len(rows) == 0:
        return None
    best = rows[0]
    for row in rows:
        if row["总分"] > best["总分"]:
            best = row
    return best


def sort_by_total(rows):
    """按总分从高到低排序，返回一个新列表，不动原数据。"""
    return sorted(rows, key=lambda r: r["总分"], reverse=True)


def write_csv(filename, rows, header):
    """把列表套字典写回 CSV。先写表头，值都转成文字。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(",".join(header) + "\n")
        for row in rows:
            values = []
            for key in header:
                values.append(str(row[key]))
            f.write(",".join(values) + "\n")


def find_student(rows, name):
    """按姓名找学生。找不到返回 None。"""
    for row in rows:
        if row["姓名"] == name:
            return row
    return None


# ---------- 主流程 ----------
print("📊 === CSV 成绩单 === 📊")

write_lines_csv(SCORES, RAW)
students = read_csv(SCORES)
add_total(students)

print(f"\n读到 {len(students)} 名学生")

print("\n--- 各科平均分 ---")
for s in SUBJECTS:
    print(f"  {s}：{subject_avg(students, s)}")

top = top_student(students)
print(f"\n🥇 总分第一：{top['姓名']}（{top['总分']} 分）")

ranked = sort_by_total(students)
print("\n--- 总分排行榜 ---")
for i, row in enumerate(ranked, start=1):
    print(f"  第 {i} 名  {row['姓名']}  {row['总分']} 分")

write_csv(RANKING, ranked, ["姓名", "语文", "数学", "英语", "总分"])
check = read_csv(RANKING)
print(f"\n排名.csv 写好了，读回来 {len(check)} 行，第一名还是 {check[0]['姓名']} ✓")

who = input("\n想查谁的成绩？").strip()
found = find_student(students, who)
if found is None:
    print(f"  查无此人：「{who}」")
else:
    print(f"  {found['姓名']}：语文 {found['语文']}  数学 {found['数学']}  "
          f"英语 {found['英语']}  总分 {found['总分']}")
