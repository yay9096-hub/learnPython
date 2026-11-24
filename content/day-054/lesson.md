# Day 54 · 带存档的冒险 🗺

> 「Day 21 你做过一个文字冒险游戏，但它有个遗憾：
> **关掉就从头开始。**
>
> 今天给它加上存档。玩到一半关掉浏览器，
> 明天打开还能接着走 —— 这才是一个完整的游戏。」

---

## 🔍 第五章你拿到的武器

| 天 | 学到的 | 一句话 |
|---|---|---|
| D45 | `try` / `except` | 乱输也不崩 |
| D46 | `raise` | 里层报错、外层处理 |
| D47 | 写文件 | 程序第一次记住东西 |
| D48 | 读文件 | 读回来还能查、能统计 |
| D49 | 文件不存在 | 第一次运行的兜底 |
| D50 | `json` | 整个结构原样存取 |
| D51 | `datetime` | 时间戳和连续天数 |
| D52 | CSV | 真实世界的表格格式 |
| D53 | 综合 | 一个真能用的记账本 |

**十天前你的程序一关就忘。现在它有记忆了。**

---

## 🧩 复习卡 · 四个最容易忘的

### 1. 只有「读」需要担心文件不存在

```python runnable w 和 a 会自动创建
with open("全新文件.txt", "a", encoding="utf-8") as f:
    f.write("追加一行\n")
print("写入不用检查文件在不在 ✓")
```

### 2. json 存日期要先转文字

```python runnable 日期不能直接进 json
import json
from datetime import date
print(json.dumps({"d": date.today().isoformat()}))
```

### 3. 读档要接两种错

```python runnable 两种都要防
import json

def load(fn):
    try:
        with open(fn, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

print(load("没有的.json"))
```

### 4. 里层 raise，外层 try

```python runnable 分工要清楚
def check(x):
    if x < 0:
        raise ValueError("不能是负数")
    return x

try:
    check(-1)
except ValueError as e:
    print(f"接住了：{e}")
```

---

## 📌 知识卡 · 用字典描述一整张地图 ⭐

今天唯一的新技巧。Day 21 你用一堆 `if` 写剧情分支，代码又长又乱。

**把剧情做成数据**，代码就短了：

```python runnable 地图 = 一个字典
SCENES = {
    "森林入口": {
        "text": "你站在一片幽暗的森林前。",
        "options": {"进去": "森林深处", "回头": "村庄"},
    },
    "森林深处": {
        "text": "树影摇曳，你听到了水声。",
        "options": {"找水源": "小溪", "回去": "森林入口"},
    },
    "小溪": {
        "text": "一条清澈的小溪。你捡到了一枚硬币。",
        "options": {"回去": "森林深处"},
        "item": "硬币",
    },
    "村庄": {
        "text": "温暖的村庄。冒险结束了。",
        "options": {},
    },
}

here = "森林入口"
scene = SCENES[here]
print(scene["text"])
print("你可以：", " / ".join(scene["options"].keys()))
print("去「进去」会到：", scene["options"]["进去"])
```

**加一个新场景 = 加一个字典条目**，一行 `if` 都不用改。

> 🧠 这个思路叫「**数据驱动**」—— 把会变的东西做成数据，
> 把不变的流程写成代码。真实游戏的剧情系统就是这么做的。

存档只要记住「现在在哪个场景」就够了：

```python runnable 存档只需要几个字段
save = {"scene": "小溪", "items": ["硬币"], "steps": 3}
print(save)
```

---

## 🎯 今天的作品 · 带存档的文字冒险

### 必须有的函数

| 函数 | 说明 |
|---|---|
| `new_game()` | 返回新存档：`scene` 为起点、`items=[]`、`steps=0`、`visited=[起点]` |
| `load_game(filename)` | 读档。不存在或损坏返回 `None`（各给一句提示） |
| `save_game(filename, save)` | 存档 |
| `show_scene(save)` | 打印当前场景的描述和可选项 |
| `move(save, choice)` | 按选项移动。**选项不存在要 `raise ValueError`**；成功则 `steps+1`、记录 `visited`、捡走 `item` |
| `is_ending(save)` | 当前场景没有任何选项 = 结局 |
| `show_status(save)` | 打印步数、背包、去过的地方数量 |

### 地图要求

- 至少 **5 个场景**
- 至少 **2 个场景有可捡的 `item`**
- 至少 **1 个结局场景**（`options` 为空）
- 场景之间要能来回走（不能是单向死路）

### 主流程要求

- 开局 `load_game`；**没有存档就 `new_game`**，有存档要提示「读档成功，你在 xxx」
- 循环：显示场景 → 问玩家选什么 → `move` → 存档
- 玩家输入不存在的选项，要接住 `ValueError` 并提示，**不消耗步数**
- 玩家输入 `退出` 时存档并结束
- 走到结局场景时打印通关信息和 `show_status`
- **每走一步都要存盘** —— 这样任何时候关掉都不丢进度

> 💡 判题会喂一串固定选项，跑完检查存档文件里的场景和背包对不对。
>
> 🏆 做完这一关第五章就通关了 —— 你的程序从此有了记忆。
