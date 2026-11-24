# -*- coding: utf-8 -*-
"""内容自检：新增或修改课程内容之后跑一下。

做两件事：
  1. 每天的 solution.py 必须**通过**全部任务  —— 否则任务写得自相矛盾
  2. 每天的 starter.py 必须**通不过**        —— 否则等于白送答案

用法（Windows 下记得带编码变量，不然中文输出会炸）：
    PYTHONIOENCODING=utf-8 python docs/verify_content.py
"""
import atexit
import io
import json
import os
import re
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = os.path.join(ROOT, "frontend", "public", "py")
sys.path.insert(0, PY)

# 第七章的内容会画图。浏览器里 pyworker 已经强制了 AGG 后端，
# 但这个脚本跑在真 CPython 上 —— 不设的话 plt.show() 会弹窗并**阻塞等你关窗**，
# 自检直接卡死。
try:
    import matplotlib  # noqa: E402
    matplotlib.use("AGG")
    import matplotlib.pyplot as _plt  # noqa: E402
    _plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]
    _plt.rcParams["axes.unicode_minus"] = False
except ImportError:
    _plt = None

import runtime  # noqa: E402
import judge  # noqa: E402

with io.open(os.path.join(PY, "turtle_shim.py"), encoding="utf-8") as f:
    runtime.install_turtle(f.read())

REQUIRED = ["meta.json", "lesson.md", "starter.py", "solution.py",
            "tests.py", "hints.md", "exercises.json"]

# 第五章起，学生代码会真的写文件。
# 网站上那些文件写在浏览器的持久化目录里，但这个脚本跑在真实文件系统上 ——
# 不换个工作目录的话，跑一次自检就往项目里拉一堆 日记.txt、存档.json。
_SANDBOX = tempfile.mkdtemp(prefix="pyson-verify-")
os.chdir(_SANDBOX)
# 用 atexit 而不是写在文件末尾 —— 末尾有 sys.exit()，写在它后面永远跑不到
atexit.register(lambda: (os.chdir(ROOT),
                         shutil.rmtree(_SANDBOX, ignore_errors=True)))

CONTENT = os.path.join(ROOT, "content")
days = sorted(
    int(m.group(1))
    for m in (re.fullmatch(r"day-(\d{3})", n) for n in os.listdir(CONTENT))
    if m
)

problems = 0
for day in days:
    d = os.path.join(CONTENT, "day-%03d" % day)

    def read(name):
        return io.open(os.path.join(d, name), encoding="utf-8").read()

    missing = [n for n in REQUIRED if not os.path.isfile(os.path.join(d, n))]
    if missing:
        print("Day %02d  ✗ 缺文件：%s" % (day, ", ".join(missing)))
        problems += 1
        continue

    meta = json.loads(read("meta.json"))
    exercises = json.loads(read("exercises.json"))
    tests_src = read("tests.py")

    sol = json.loads(judge.judge(read("solution.py"), tests_src))
    if sol.get("error"):
        print("Day %02d  ✗ 判题器报错：%s" % (day, sol["error"]))
        problems += 1
        continue

    star = json.loads(judge.judge(read("starter.py"), tests_src))
    starter_leaks = not star.get("error") and star.get("all_passed")

    ok = sol["all_passed"] and not starter_leaks
    note = ""
    if not sol["all_passed"]:
        note = "   ← 参考答案没过：" + ", ".join(
            r["id"] for r in sol["results"] if not r["passed"])
    elif starter_leaks:
        note = "   ← starter 直接就能过，任务太松"

    print("Day %02d  %s  %-16s 任务 %2d 项 · 练习 %d 题%s" % (
        day, "✓" if ok else "✗", meta["title"],
        len(sol["results"]), len(exercises), note))

    if not ok:
        problems += 1
    if sol.get("run_error"):
        print("        参考答案运行报错：%s %s" % (
            sol["run_error"]["type"], sol["run_error"]["message"]))
        problems += 1

print()
print("全部通过 ✨" if problems == 0 else "有 %d 处需要修" % problems)
sys.exit(1 if problems else 0)
