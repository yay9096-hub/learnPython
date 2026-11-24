## 提示 1 · overview 返回字典，不是一堆变量

```python
def overview(records):
    """算总览数据，返回一个字典。"""
    done = [r for r in records if r["status"] == "done"]
    minutes = 0
    runs = 0
    errors = 0
    for r in done:
        minutes += r["minutes"]
        runs += r["runs"]
        errors += r["errors"]

    return {
        "done": len(done),
        "total": len(records),
        "minutes": round(minutes, 1),
        "avg": round(minutes / len(done), 1) if done else 0.0,
        "runs": runs,
        "errors": errors,
        "rate": round(errors / runs * 100, 1) if runs else 0.0,
    }
```

**七项一次返回**，比返回七个值好用得多（Day 39 的经验法则：超过三个就用字典）。

⚠️ 两处 `if ... else 0.0` 是防除零 —— 判题会用空数据试。

分章汇总注意：**总数算上没完成的，时长只算完成的**。

```python
def by_stage(records):
    result = {}
    for r in records:
        stage = r["stage"]
        done, total, minutes = result.get(stage, (0, 0, 0))
        total += 1                      # ← 每天都算进总数
        if r["status"] == "done":
            done += 1
            minutes += r["minutes"]     # ← 只有完成的才算时长
        result[stage] = (done, total, round(minutes, 1))
    return result
```

`result.get(stage, (0, 0, 0))` —— 第一次遇到这一章就从 0 开始（Day 29 的 get）。

## 提示 2 · build_report 只返回字符串

```python
def build_report(records):
    """生成整份报告的文字，返回字符串。"""
    o = overview(records)
    longest, smoothest, hardest = highlights(records)

    lines = []
    lines.append("=" * 46)
    lines.append("  总览")
    lines.append(f"    完成天数    {o['done']} / {o['total']}")
    lines.append(f"    总时长      {o['minutes']} 分钟")
    ...
    return "\n".join(lines)
```

⚠️ **函数里一个 `print` 都不要写**（判题会检查）。

为什么？因为返回字符串之后，主流程能**同时**做两件事：

```python
report = build_report(records)
print(report)                                   # 打印到终端

with open(REPORT, "w", encoding="utf-8") as f:
    f.write(report)                             # 同一份写进文件
```

如果 `build_report` 自己 print 了，就没法写进文件了 ——
这正是 Day 37「print 是说给人听，return 是交给程序」的实战。

进度条要防除零：

```python
def bar(value, total, width=20):
    if total <= 0:
        return "░" * width + "   0%"
    filled = int(value / total * width)
    filled = max(0, min(filled, width))         # 夹取（Day 57）
    percent = int(value / total * 100)
    return "█" * filled + "░" * (width - filled) + f" {percent:>4}%"
```

## 提示 3 · 画图 + 存图

四格布局跟 Day 65 一样，唯一的新东西是**存成文件**：

```python
    plt.tight_layout()
    plt.savefig(filename, dpi=110)     # ← 必须在 show 之前
    plt.show()
```

⚠️ `plt.show()` 之后图就被清空了，`savefig` 会存出一张白图。**顺序不能反。**

主流程开头要防空：

```python
records = load_records(DATA)
done_count = len([r for r in records if r["status"] == "done"])

if done_count == 0:
    print("还没有完成任何一天，先去学几天再回来生成报告 😉")
else:
    ...
```

> 🏆 跑完去「📁 文件」看看 `学习报告.txt` 和 `学习图表.png` ——
> 这两个文件就是你的作品，可以直接发给别人看。
