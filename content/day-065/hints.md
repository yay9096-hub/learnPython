## 提示 1 · 先筛出「已完成」的天

```python
with open(DATA, encoding="utf-8") as f:
    records = json.load(f)

done = [r for r in records if r["status"] == "done"]

if len(done) == 0:
    print("  还没有完成任何一天，先去学几天再回来 😉")
else:
    # 后面所有的统计和画图都写在这里面
    ...
```

⚠️ **防空这一步不能省**。没做过的天 `minutes` 是 0，
混进来会把平均值拉低；一天都没完成时更是会画出空白图。

统计用累加器（第三章的老本事）：

```python
    total_minutes = 0
    total_runs = 0
    total_errors = 0
    for r in done:
        total_minutes += r["minutes"]
        total_runs += r["runs"]
        total_errors += r["errors"]

    avg_minutes = round(total_minutes / len(done), 1)
    error_rate = round(total_errors / total_runs * 100, 1) if total_runs else 0.0
```

⚠️ 最后那个 `if total_runs else 0.0` 是防除零 —— 万一一次都没运行过。

## 提示 2 · 三张折线图

画图前先把数据抽成一个个列表：

```python
    days = [r["day"] for r in done]
    minutes = [r["minutes"] for r in done]
    runs = [r["runs"] for r in done]
    errors = [r["errors"] for r in done]
```

累计要用循环，一路加上去：

```python
    cumulative = []
    running_total = 0
    for r in done:
        running_total += r["minutes"]
        cumulative.append(round(running_total, 1))
```

⚠️ **`cumulative` 必须是递增的** —— 每一项都比前一项大（或相等）。
判题会检查这一点，也是检验你有没有写对累加器的最好方式。

双折线要 label + legend 配套：

```python
    plt.plot(days, runs, marker="o", label="运行次数", color="#8B5CF6")
    plt.plot(days, errors, marker="s", label="报错次数", color="#EC6FA9")
    plt.legend()          # ← 少了这句，label 是看不见的
```

## 提示 3 · 饼图和四格布局

按章汇总用字典计数（Day 30 的 `.get(键, 默认值)`）：

```python
    by_stage = {}
    for r in done:
        key = f"第 {r['stage']} 章"
        by_stage[key] = by_stage.get(key, 0) + r["minutes"]

    plt.pie(list(by_stage.values()), labels=list(by_stage.keys()),
            autopct="%1.0f%%")
```

⚠️ `.values()` 和 `.keys()` 要 `list(...)` 包一下再给 `pie`。

四格布局：

```python
    plt.figure(figsize=(11, 7))

    plt.subplot(2, 2, 1)      # 左上
    ...
    plt.subplot(2, 2, 2)      # 右上
    ...
    plt.subplot(2, 2, 3)      # 左下
    ...
    plt.subplot(2, 2, 4)      # 右下
    ...

    plt.tight_layout()
    plt.show()
```

`subplot(2, 2, n)` 的编号从左上开始横着数：1 左上、2 右上、3 左下、4 右下。

> 💡 图出来之后，试着改改 `figsize` 和配色 ——
> **这张图是你自己的成长记录，值得多花几分钟调好看点。**
