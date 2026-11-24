# Day 69 · 个人学习仪表盘
import json
import matplotlib.pyplot as plt

DATA = "我的学习记录.json"
REPORT = "学习报告.txt"
CHART = "学习图表.png"

STAGE_NAMES = {
    1: "会说话", 2: "会判断和重复", 3: "会管理数据", 4: "会拆分问题",
    5: "会和外界打交道", 6: "会造东西", 7: "会做出好看的",
}


def load_records(filename):
    """读学习记录。文件不存在或损坏返回空列表。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


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


def by_stage(records):
    """按章汇总，返回 {章号: (完成数, 总数, 总时长)}。"""
    result = {}
    for r in records:
        stage = r["stage"]
        done, total, minutes = result.get(stage, (0, 0, 0))
        total += 1
        if r["status"] == "done":
            done += 1
            minutes += r["minutes"]
        result[stage] = (done, total, round(minutes, 1))
    return result


def bar(value, total, width=20):
    """画一条文字进度条。total 为 0 时返回空条，不崩。"""
    if total <= 0:
        return "░" * width + "   0%"
    filled = int(value / total * width)
    filled = max(0, min(filled, width))
    percent = int(value / total * 100)
    return "█" * filled + "░" * (width - filled) + f" {percent:>4}%"


def highlights(records):
    """返回 (最投入的, 最顺的, 最费劲的)。没数据返回三个 None。"""
    done = [r for r in records if r["status"] == "done"]
    if not done:
        return None, None, None

    longest = done[0]
    smoothest = done[0]
    hardest = done[0]
    for r in done:
        if r["minutes"] > longest["minutes"]:
            longest = r
        if r["errors"] < smoothest["errors"]:
            smoothest = r
        if r["errors"] > hardest["errors"]:
            hardest = r
    return longest, smoothest, hardest


def build_report(records):
    """生成整份报告的文字，返回字符串。"""
    o = overview(records)
    longest, smoothest, hardest = highlights(records)

    lines = []
    lines.append("╔" + "═" * 44 + "╗")
    lines.append("║" + "派森酱学院 · 学习仪表盘".center(32) + "║")
    lines.append("╚" + "═" * 44 + "╝")
    lines.append("")

    lines.append("  总览")
    lines.append(f"    完成天数    {o['done']} / {o['total']}")
    lines.append(f"    总时长      {o['minutes']} 分钟"
                 f"（{round(o['minutes'] / 60, 1)} 小时）")
    lines.append(f"    平均每天    {o['avg']} 分钟")
    lines.append(f"    运行次数    {o['runs']}    "
                 f"报错 {o['errors']} 次（{o['rate']}%）")
    lines.append("")

    lines.append("  各章进度")
    stages = by_stage(records)
    for stage in sorted(stages):
        done, total, minutes = stages[stage]
        name = STAGE_NAMES.get(stage, f"第 {stage} 章")
        lines.append(f"    第 {stage} 章 {name:<8} {bar(done, total, 10)}"
                     f"  ({done}/{total})  {minutes} 分钟")
    lines.append("")

    lines.append("  记录")
    if longest is not None:
        lines.append(f"    最投入的一天   Day {longest['day']}"
                     f"「{longest['title']}」{longest['minutes']} 分钟")
        lines.append(f"    最顺的一天     Day {smoothest['day']}"
                     f"（{smoothest['errors']} 次报错）")
        lines.append(f"    最费劲的一天   Day {hardest['day']}"
                     f"（{hardest['errors']} 次报错）")
    lines.append("")
    lines.append("=" * 46)

    return "\n".join(lines)


def draw_charts(records, filename):
    """画四格图表并存成图片。"""
    done = [r for r in records if r["status"] == "done"]
    days = [r["day"] for r in done]
    minutes = [r["minutes"] for r in done]
    runs = [r["runs"] for r in done]
    errors = [r["errors"] for r in done]

    cumulative = []
    total = 0
    for r in done:
        total += r["minutes"]
        cumulative.append(round(total, 1))

    stages = by_stage(records)
    stage_labels = []
    stage_percents = []
    for stage in sorted(stages):
        d, t, _m = stages[stage]
        stage_labels.append(f"第{stage}章")
        stage_percents.append(round(d / t * 100, 1) if t else 0)

    plt.figure(figsize=(11, 7))

    plt.subplot(2, 2, 1)
    plt.plot(days, minutes, marker="o", color="#8B5CF6")
    plt.title("每天学习时长")
    plt.xlabel("第几天")
    plt.ylabel("分钟")
    plt.grid(alpha=0.3)

    plt.subplot(2, 2, 2)
    plt.barh(stage_labels, stage_percents, color="#EC6FA9")
    plt.title("各章完成度")
    plt.xlabel("完成百分比")
    plt.xlim(0, 100)

    plt.subplot(2, 2, 3)
    plt.plot(days, cumulative, marker="o", color="#34D399")
    plt.fill_between(days, cumulative, alpha=0.2, color="#34D399")
    plt.title(f"累计学习时长（共 {round(total)} 分钟）")
    plt.xlabel("第几天")
    plt.ylabel("累计分钟")
    plt.grid(alpha=0.3)

    plt.subplot(2, 2, 4)
    plt.plot(days, runs, marker="o", label="运行", color="#8B5CF6")
    plt.plot(days, errors, marker="s", label="报错", color="#EC6FA9")
    plt.title("运行与报错")
    plt.xlabel("第几天")
    plt.ylabel("次数")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=110)
    plt.show()


# ---------- 主流程 ----------
records = load_records(DATA)
done_count = len([r for r in records if r["status"] == "done"])

if done_count == 0:
    print("还没有完成任何一天，先去学几天再回来生成报告 😉")
else:
    report = build_report(records)
    print(report)

    with open(REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\n📄 报告已存进 {REPORT}")

    draw_charts(records, CHART)
    print(f"📊 图表已存进 {CHART}")
    print("\n去右边「📁 文件」和「📊 图表」看看你的作品 ✨")
