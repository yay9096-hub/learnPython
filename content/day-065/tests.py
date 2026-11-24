import ast

# 判题时自己造一份学习记录（网站上这个文件由前端注入她的真实数据）
SETUP = '''
import json
_rows = [
    {"day": 1, "title": "角色出场卡", "stage": 1, "status": "done",
     "minutes": 42.0, "runs": 12, "errors": 3, "hints": 1, "completed_at": "2026-09-01"},
    {"day": 2, "title": "角色属性面板", "stage": 1, "status": "done",
     "minutes": 35.0, "runs": 9, "errors": 2, "hints": 0, "completed_at": "2026-09-02"},
    {"day": 3, "title": "伤害计算器", "stage": 1, "status": "done",
     "minutes": 58.0, "runs": 20, "errors": 7, "hints": 2, "completed_at": "2026-09-02"},
    {"day": 11, "title": "魔法结界", "stage": 2, "status": "done",
     "minutes": 40.0, "runs": 14, "errors": 4, "hints": 1, "completed_at": "2026-09-03"},
    {"day": 12, "title": "属性克制判定", "stage": 2, "status": "done",
     "minutes": 45.0, "runs": 15, "errors": 5, "hints": 0, "completed_at": "2026-09-04"},
    {"day": 23, "title": "队伍名单", "stage": 3, "status": "opened",
     "minutes": 5.0, "runs": 1, "errors": 0, "hints": 0, "completed_at": ""},
    {"day": 24, "title": "背包系统", "stage": 3, "status": "locked",
     "minutes": 0, "runs": 0, "errors": 0, "hints": 0, "completed_at": ""},
]
with open("我的学习记录.json", "w", encoding="utf-8") as _f:
    json.dump(_rows, _f, ensure_ascii=False, indent=2)
'''

# 上面五天 done：42+35+58+40+45 = 220 分钟，平均 44.0
# runs 12+9+20+14+15 = 70，errors 3+2+7+4+5 = 21，报错率 30.0%
# 最长是 Day 3（58 分钟）
# 各章：第1章 135、第2章 85


def _calls(ctx, name):
    n = 0
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == name:
                n += 1
    return n


def reads_data(ctx):
    return "我的学习记录.json" in ctx["code"]


def filters_done(ctx):
    """只统计 status == done 的天。"""
    return '"done"' in ctx["code"] or "'done'" in ctx["code"]


def guards_empty(ctx):
    """一天都没完成时不能崩 —— 代码里要有对应的判断。"""
    src = ctx["code"].replace(" ", "")
    return ("len(done)==0" in src or "ifnotdone" in src
            or "len(done)>0" in src or "ifdone" in src)


def four_subplots(ctx):
    return _calls(ctx, "subplot") >= 4


def four_axes(ctx):
    return ctx["plot"].get("axes", 0) >= 4


def four_titles(ctx):
    return len(ctx["plot"].get("titles", [])) >= 4


def has_lines(ctx):
    """三张折线图：每天时长 1 条、累计 1 条、运行报错 2 条 = 至少 4 条。"""
    return ctx["plot"].get("lines", 0) >= 4


def has_legend(ctx):
    return ctx["plot"].get("legends", 0) >= 1


def uses_label(ctx):
    return "label=" in ctx["code"]


def has_pie(ctx):
    """饼图的扇形会记进 wedges。"""
    return ctx["plot"].get("wedges", 0) >= 2


def uses_autopct(ctx):
    return "autopct" in ctx["code"]


def uses_fill_between(ctx):
    return _calls(ctx, "fill_between") >= 1


def uses_tight_layout(ctx):
    return _calls(ctx, "tight_layout") >= 1


def cumulative_correct(ctx):
    """累计列表最后一项要是 220。"""
    for k, v in ctx["ns"].items():
        if k.startswith("__") or not isinstance(v, list) or len(v) < 3:
            continue
        try:
            nums = [float(x) for x in v]
        except (TypeError, ValueError):
            continue
        if abs(nums[-1] - 220) < 0.5 and all(
                nums[i] <= nums[i + 1] for i in range(len(nums) - 1)):
            return True
    return False


def summary_counts(ctx):
    out = ctx["stdout"]
    return "5" in out and "220" in out


def summary_avg(ctx):
    return "44" in ctx["stdout"]


def summary_runs(ctx):
    out = ctx["stdout"]
    return "70" in out and "21" in out


def summary_error_rate(ctx):
    return "30" in ctx["stdout"]


def summary_longest(ctx):
    """最投入的一天是 Day 3「伤害计算器」。"""
    out = ctx["stdout"]
    return "伤害计算器" in out and "58" in out


def survived(ctx):
    return ctx["error"] is None


CASES = [
    {
        "setup": SETUP,
        "checks": [
            {"id": "read", "desc": "读了自己的学习记录",
             "type": "custom", "fn": "reads_data",
             "fail": "`with open(\"我的学习记录.json\", encoding=\"utf-8\") as f:`"},
            {"id": "filter", "desc": "只统计已完成的天",
             "type": "custom", "fn": "filters_done",
             "fail": "用 `[r for r in records if r[\"status\"] == \"done\"]` 筛出来 —— "
                     "没做过的天不该拉低平均值"},
            {"id": "guard", "desc": "一天都没完成时不会崩",
             "type": "custom", "fn": "guards_empty",
             "fail": "⚠️ 真实数据一定要防空。先 `if len(done) == 0:` 打印提示并停下"},
            {"id": "subplots", "desc": "分成了四格",
             "type": "custom", "fn": "four_subplots",
             "fail": "`plt.subplot(2, 2, 1)` 到 `plt.subplot(2, 2, 4)`"},
            {"id": "axes", "desc": "四张图都真的画了",
             "type": "custom", "fn": "four_axes",
             "fail": "每个 subplot 后面都要跟一张图"},
            {"id": "titles", "desc": "四张图都有标题",
             "type": "custom", "fn": "four_titles",
             "fail": "每张图一句 `plt.title(...)`"},
            {"id": "lines", "desc": "折线图画够了（至少 4 条线）",
             "type": "custom", "fn": "has_lines",
             "fail": "每天时长 1 条、累计 1 条、运行和报错各 1 条"},
            {"id": "label", "desc": "双折线图标了 label",
             "type": "custom", "fn": "uses_label",
             "fail": "`plt.plot(days, runs, label=\"运行次数\")`"},
            {"id": "legend", "desc": "调用了 legend() 显示图例",
             "type": "custom", "fn": "has_legend",
             "fail": "⚠️ 光写 `label=` 是看不见的，还要调一次 `plt.legend()`"},
            {"id": "fill", "desc": "累计图用了 fill_between",
             "type": "custom", "fn": "uses_fill_between",
             "fail": "`plt.fill_between(days, cumulative, alpha=0.2, color=...)`"},
            {"id": "cumulative", "desc": "累计算对了（最后 220 分钟）",
             "type": "custom", "fn": "cumulative_correct",
             "fail": "42+35+58+40+45 = **220**。用累加器一路加过去，"
                     "而且列表必须是递增的",
             },
            {"id": "pie", "desc": "画了饼图",
             "type": "custom", "fn": "has_pie",
             "fail": "`plt.pie(values, labels=names, ...)`"},
            {"id": "autopct", "desc": "饼图标了百分比",
             "type": "custom", "fn": "uses_autopct",
             "fail": "`autopct=\"%1.0f%%\"` —— 最后那两个 %% 才是百分号本身"},
            {"id": "tight", "desc": "用了 tight_layout",
             "type": "custom", "fn": "uses_tight_layout",
             "fail": "四格图不加这个，标题会互相压住"},
            {"id": "counts", "desc": "摘要里有完成天数和总时长",
             "type": "custom", "fn": "summary_counts",
             "fail": "已完成 **5** 天，总时长 **220** 分钟"},
            {"id": "avg", "desc": "平均时长算对（44.0）",
             "type": "custom", "fn": "summary_avg",
             "fail": "220 ÷ 5 = **44.0** 分钟"},
            {"id": "runs", "desc": "运行和报错总数对",
             "type": "custom", "fn": "summary_runs",
             "fail": "运行 **70** 次，报错 **21** 次"},
            {"id": "rate", "desc": "报错率算对（30.0%）",
             "type": "custom", "fn": "summary_error_rate",
             "fail": "21 ÷ 70 × 100 = **30.0**%"},
            {"id": "longest", "desc": "找对了最投入的一天",
             "type": "custom", "fn": "summary_longest",
             "fail": "Day 3「伤害计算器」花了 **58** 分钟，最长"},
            {"id": "survive", "desc": "全程没有崩溃",
             "type": "custom", "fn": "survived",
             "fail": "真实数据里会有 minutes 为 0、runs 为 0 的天 —— "
                     "算报错率时小心除以零"},
        ],
    }
]
