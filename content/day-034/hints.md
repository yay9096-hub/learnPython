## 提示 1 · 先算总分，再做别的

所有后面的功能都依赖 `total`，所以第一步就把它加上：

```python
for s in students:
    s["total"] = s["chinese"] + s["math"] + s["english"]
```

Day 31 学过 —— 遍历时给字典**新增字段**，原数据真的会变。

然后成绩单就是普通遍历：

```python
for s in students:
    print(f"  {s['name']}  语文 {s['chinese']}  数学 {s['math']}  "
          f"英语 {s['english']}  总分 {s['total']}")
```

⚠️ 一行太长可以拆成两段字符串写（像上面那样），Python 会自动接起来。

## 提示 2 · 单科统计：先收集，再算

「数学这一科所有人的分数」不是现成的，得先收集出来：

```python
SUBJECTS = ["chinese", "math", "english"]
CN = {"chinese": "语文", "math": "数学", "english": "英语"}

for subject in SUBJECTS:
    scores = []
    for s in students:
        scores.append(s[subject])

    avg = round(sum(scores) / len(scores), 1)
    print(f"  {CN[subject]}：最高 {max(scores)}  最低 {min(scores)}  平均 {avg}")
```

外层循环管「哪一科」，内层循环管「收集这一科的分数」——
又是 Day 18 的嵌套循环。

## 提示 3 · 排行榜、等第、查询

排序一句话（Day 31 学的）：

```python
students.sort(key=lambda s: s["total"], reverse=True)

for i, s in enumerate(students):
    print(f"  第 {i + 1} 名  {s['name']}  {s['total']} 分")
```

等第统计用**字典当计数器**，比四个变量清爽：

```python
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

for level, count in grades.items():
    print(f"  {level}：{'█' * count} {count} 人")
```

⚠️ 分档一定要**从高到低**写（Day 12 的分支顺序，第四次出现了 😉）。

查询要同时找到人和名次 —— 用 `enumerate` 一趟搞定：

```python
who = input("想查谁的成绩？").strip()

found = None
place = 0
for i, s in enumerate(students):
    if s["name"] == who:
        found = s
        place = i + 1

if found:
    print(f"🔎 {found['name']}  第 {place} 名")
    print(f"   语文 {found['chinese']}  ...  总分 {found['total']}")
else:
    print(f"🔎 查无此人：「{who}」")
```

⚠️ 名次要在**排序之后**再找，否则名次是错的。
