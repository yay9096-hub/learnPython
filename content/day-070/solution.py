"""追番管理器 —— 我的毕业作品。

记录看过的番剧、打分、写短评，支持：
  · 添加 / 查找 / 按评分排序
  · 存进 json 存档，关掉再打开还在
  · 把评分分布画成柱状图存成图片

这是我学 Python 的第 70 天写的。
"""
import json

import matplotlib.pyplot as plt

SAVE_FILE = "我的番剧.json"
CHART_FILE = "评分分布.png"
MAX_SCORE = 10
MIN_SCORE = 1


class Anime:
    """一部番剧的记录。"""

    def __init__(self, name, score=5, comment=""):
        if not name.strip():
            raise ValueError("番剧名不能是空的")
        self.name = name.strip()
        self.score = self._clamp(score)
        self.comment = comment

    def _clamp(self, score):
        """把评分夹在 1~10 之间。"""
        return max(MIN_SCORE, min(int(score), MAX_SCORE))

    def rate(self, score):
        """重新打分，返回新的分数。"""
        self.score = self._clamp(score)
        return self.score

    def stars(self):
        """把分数变成星星条。"""
        return "★" * self.score + "☆" * (MAX_SCORE - self.score)

    def to_dict(self):
        """转成能存进 json 的字典。"""
        return {"name": self.name, "score": self.score, "comment": self.comment}

    def __str__(self):
        text = f"{self.name:<12} {self.stars()} {self.score}/10"
        if self.comment:
            text += f"  「{self.comment}」"
        return text


def make_anime(data):
    """从字典造一部番剧回来。"""
    return Anime(data["name"], data.get("score", 5), data.get("comment", ""))


def load_list(filename):
    """读存档。文件不存在或损坏都返回空列表。"""
    try:
        with open(filename, encoding="utf-8") as f:
            rows = json.load(f)
    except FileNotFoundError:
        print("  （还没有存档，从空列表开始）")
        return []
    except json.JSONDecodeError:
        print("  （存档损坏了，从空列表开始）")
        return []
    return [make_anime(r) for r in rows]


def save_list(filename, animes):
    """把整个列表存进 json。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump([a.to_dict() for a in animes], f,
                  ensure_ascii=False, indent=2)


def find(animes, name):
    """按名字找。找不到返回 None。"""
    for a in animes:
        if a.name == name:
            return a
    return None


def top_rated(animes, n=3):
    """按评分从高到低取前 n 部。"""
    return sorted(animes, key=lambda a: a.score, reverse=True)[:n]


def score_stats(animes):
    """返回 (平均分, 最高分, 最低分)。空列表返回三个 0。"""
    if not animes:
        return 0, 0, 0
    scores = [a.score for a in animes]
    return round(sum(scores) / len(scores), 1), max(scores), min(scores)


def draw_chart(animes, filename):
    """把评分分布画成柱状图并存成图片。"""
    if not animes:
        print("  （没有数据，画不了图）")
        return

    names = [a.name for a in animes]
    scores = [a.score for a in animes]

    plt.figure(figsize=(8, 4))
    plt.barh(names, scores, color="#8B5CF6")
    plt.title("我的番剧评分")
    plt.xlabel("评分")
    plt.xlim(0, MAX_SCORE)
    plt.grid(axis="x", alpha=0.3)

    for i in range(len(names)):
        plt.text(scores[i] + 0.15, i, str(scores[i]), va="center")

    plt.tight_layout()
    plt.savefig(filename, dpi=110)
    plt.show()


# ---------- 主流程 ----------
print("🎬 === 我的追番管理器 === 🎬\n")

animes = load_list(SAVE_FILE)

if not animes:
    animes = [
        Anime("魔法少女小圆", 10, "看完睡不着"),
        Anime("紫罗兰永恒花园", 9, "画面太美了"),
        Anime("孤独摇滚", 9, "波奇酱！"),
        Anime("莉可丽丝", 8, ""),
        Anime("间谍过家家", 8, "阿尼亚哈哈"),
    ]
    print(f"  ✨ 初始化了 {len(animes)} 部番剧")

print("\n--- 我的收藏 ---")
for a in animes:
    print("  " + str(a))

avg, best, worst = score_stats(animes)
print(f"\n  共 {len(animes)} 部，平均 {avg} 分（最高 {best}，最低 {worst}）")

print("\n--- 评分 TOP 3 ---")
for i, a in enumerate(top_rated(animes, 3), start=1):
    print(f"  第 {i} 名  {a}")

print("\n--- 查找 ---")
found = find(animes, "孤独摇滚")
print(f"  孤独摇滚：{found if found else '没找到'}")
print(f"  不存在的番：{find(animes, '完全不存在的番')}")

print("\n--- 改分 ---")
if found:
    print(f"  改分前 {found.score}，改分后 {found.rate(10)}")

print("\n--- 非法数据会被挡住 ---")
try:
    Anime("   ", 5)
except ValueError as e:
    print(f"  ✓ 拦下了：{e}")

save_list(SAVE_FILE, animes)
print(f"\n💾 已存进 {SAVE_FILE}")

draw_chart(animes, CHART_FILE)
print(f"📊 图表已存进 {CHART_FILE}")

print("\n" + "=" * 42)
print("  70 天前我连 print 是什么都不知道，")
print("  今天我写完了自己的第一个软件。")
print("  谢谢派森酱，也谢谢没有放弃的自己 ✨")
print("=" * 42)
