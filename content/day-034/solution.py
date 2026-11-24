# Day 34 · 班级成绩管理系统
students = [
    {"name": "星野樱",   "chinese": 88, "math": 92, "english": 79},
    {"name": "月见琉璃", "chinese": 95, "math": 78, "english": 91},
    {"name": "天野灯",   "chinese": 72, "math": 85, "english": 68},
    {"name": "水城凛",   "chinese": 90, "math": 99, "english": 94},
    {"name": "夜刀神澪", "chinese": 65, "math": 71, "english": 82},
    {"name": "风见幽香", "chinese": 84, "math": 88, "english": 87},
]

SUBJECTS = ["chinese", "math", "english"]
CN = {"chinese": "语文", "math": "数学", "english": "英语"}

print("📊 === 班级成绩管理系统 === 📊")

# ---------- 1. 算总分 ----------
for s in students:
    s["total"] = s["chinese"] + s["math"] + s["english"]

# ---------- 2. 成绩单 ----------
print("\n--- 成绩单 ---")
for s in students:
    print(f"  {s['name']}  语文 {s['chinese']}  数学 {s['math']}  "
          f"英语 {s['english']}  总分 {s['total']}")

# ---------- 3. 单科统计 ----------
print("\n--- 单科统计 ---")
for subject in SUBJECTS:
    scores = []
    for s in students:
        scores.append(s[subject])

    avg = round(sum(scores) / len(scores), 1)
    print(f"  {CN[subject]}：最高 {max(scores)}  最低 {min(scores)}  平均 {avg}")

# ---------- 4. 排行榜 ----------
students.sort(key=lambda s: s["total"], reverse=True)

print("\n--- 总分排行榜 ---")
for i, s in enumerate(students):
    print(f"  第 {i + 1} 名  {s['name']}  {s['total']} 分")

# ---------- 5. 等第统计 ----------
grades = {"优秀": 0, "良好": 0, "及格": 0, "待努力": 0}

for s in students:
    if s["total"] >= 270:
        grades["优秀"] += 1
    elif s["total"] >= 240:
        grades["良好"] += 1
    elif s["total"] >= 210:
        grades["及格"] += 1
    else:
        grades["待努力"] += 1

print("\n--- 等第分布 ---")
for level, count in grades.items():
    bar = "█" * count
    print(f"  {level}：{bar} {count} 人")

# ---------- 6. 查询 ----------
who = input("\n想查谁的成绩？").strip()

found = None
place = 0
for i, s in enumerate(students):
    if s["name"] == who:
        found = s
        place = i + 1

if found:
    print(f"🔎 {found['name']}  第 {place} 名")
    print(f"   语文 {found['chinese']}  数学 {found['math']}  "
          f"英语 {found['english']}  总分 {found['total']}")
else:
    print(f"🔎 查无此人：「{who}」")
