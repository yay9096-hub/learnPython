# Day 65 · 我的学习报告
import json
import matplotlib.pyplot as plt

DATA = "我的学习记录.json"

with open(DATA, encoding="utf-8") as f:
    records = json.load(f)

done = [r for r in records if r["status"] == "done"]

print("📈 === 我的学习报告 === 📈")

if len(done) == 0:
    print("  还没有完成任何一天，先去学几天再回来 😉")
else:
    # ---------- 文字摘要 ----------
    total_minutes = 0
    total_runs = 0
    total_errors = 0
    for r in done:
        total_minutes += r["minutes"]
        total_runs += r["runs"]
        total_errors += r["errors"]

    avg_minutes = round(total_minutes / len(done), 1)
    error_rate = round(total_errors / total_runs * 100, 1) if total_runs else 0.0

    longest = done[0]
    for r in done:
        if r["minutes"] > longest["minutes"]:
            longest = r

    print(f"  已完成 {len(done)} / {len(records)} 天")
    print(f"  总时长 {round(total_minutes)} 分钟，平均每天 {avg_minutes} 分钟")
    print(f"  运行 {total_runs} 次，报错 {total_errors} 次")
    print(f"  报错率 {error_rate}%")
    print(f"  最投入的一天：Day {longest['day']}「{longest['title']}」"
          f"（{longest['minutes']} 分钟）")

    # ---------- 准备画图用的数据 ----------
    days = [r["day"] for r in done]
    minutes = [r["minutes"] for r in done]
    runs = [r["runs"] for r in done]
    errors = [r["errors"] for r in done]

    cumulative = []
    running_total = 0
    for r in done:
        running_total += r["minutes"]
        cumulative.append(round(running_total, 1))

    by_stage = {}
    for r in done:
        key = f"第 {r['stage']} 章"
        by_stage[key] = by_stage.get(key, 0) + r["minutes"]

    # ---------- 四格报告 ----------
    plt.figure(figsize=(11, 7))

    plt.subplot(2, 2, 1)
    plt.plot(days, minutes, marker="o", color="#8B5CF6")
    plt.title("每天学习时长")
    plt.xlabel("第几天")
    plt.ylabel("分钟")
    plt.grid(alpha=0.3)

    plt.subplot(2, 2, 2)
    plt.plot(days, cumulative, marker="o", color="#34D399")
    plt.fill_between(days, cumulative, alpha=0.2, color="#34D399")
    plt.title(f"累计学习时长（共 {round(running_total)} 分钟）")
    plt.xlabel("第几天")
    plt.ylabel("累计分钟")
    plt.grid(alpha=0.3)

    plt.subplot(2, 2, 3)
    plt.plot(days, runs, marker="o", label="运行次数", color="#8B5CF6")
    plt.plot(days, errors, marker="s", label="报错次数", color="#EC6FA9")
    plt.title("运行与报错")
    plt.xlabel("第几天")
    plt.ylabel("次数")
    plt.legend()
    plt.grid(alpha=0.3)

    plt.subplot(2, 2, 4)
    plt.pie(list(by_stage.values()), labels=list(by_stage.keys()),
            autopct="%1.0f%%",
            colors=["#8B5CF6", "#EC6FA9", "#34D399", "#F59E0B",
                    "#60A5FA", "#F87171", "#A78BFA"])
    plt.title("各章学习时长占比")

    plt.tight_layout()
    plt.show()

    print("\n✅ 报告画好了 —— 这是你自己走过的路 ✨")
