# Day 50 · 游戏存档 💾

> 「Day 49 你把错题存成 `题目 | 答案`，读回来还得自己 `split` 拆。
>
> 如果要存的是一个**嵌套的队伍数据**（Day 31 那种列表套字典）呢？
> 自己拆能拆到崩溃。
>
> 今天学 `json` —— **存进去什么样，读出来还什么样。**」

---

## 📌 知识卡 1 · 手工存字典有多痛苦

```python runnable 手工版：存
role = {"name": "星野樱", "level": 12, "hp": 340, "skills": ["樱花斩", "结界术"]}

with open("手工存档.txt", "w", encoding="utf-8") as f:
    f.write(f"{role['name']}|{role['level']}|{role['hp']}|{','.join(role['skills'])}\n")

with open("手工存档.txt", encoding="utf-8") as f:
    print(f.read())
```

存是存进去了。现在读回来试试 —— 注意每个字段都要**手动转类型**：

```python runnable 手工版：读（够烦的）
with open("手工存档.txt", encoding="utf-8") as f:
    line = f.read().strip()

parts = line.split("|")
role = {
    "name": parts[0],
    "level": int(parts[1]),
    "hp": int(parts[2]),
    "skills": parts[3].split(","),
}
print(role)
```

四个字段就这么麻烦了。要是名字里正好有个 `|` 呢？直接崩。

---

## 📌 知识卡 2 · `json` —— 一行存，一行读 ⭐

```python runnable json 版：存
import json

role = {"name": "星野樱", "level": 12, "hp": 340, "skills": ["樱花斩", "结界术"]}

with open("存档.json", "w", encoding="utf-8") as f:
    json.dump(role, f, ensure_ascii=False, indent=2)

print("存好了，去右边「📁 文件」看看长什么样")
```

```python runnable json 版：读
import json

with open("存档.json", encoding="utf-8") as f:
    role = json.load(f)

print(role)
print(type(role))
print(role["skills"][0])
print(role["level"] + 1)
```

**读出来就是字典**，字段类型全都对 —— 数字还是数字，列表还是列表。
一次 `split` 都不用写。

---

## 📌 知识卡 3 · 两个必写的参数 ⚠️

```python runnable 不加 ensure_ascii=False 会怎样
import json

role = {"name": "星野樱"}

with open("坏的.json", "w", encoding="utf-8") as f:
    json.dump(role, f)

with open("坏的.json", encoding="utf-8") as f:
    print(f.read())
```

中文变成了 `\u661f\u91ce\u6a31` —— 程序读得懂，但**人看不懂**。

```python runnable 加上就正常了
import json

role = {"name": "星野樱", "level": 12, "skills": ["樱花斩", "结界术"]}

with open("好的.json", "w", encoding="utf-8") as f:
    json.dump(role, f, ensure_ascii=False, indent=2)

with open("好的.json", encoding="utf-8") as f:
    print(f.read())
```

| 参数 | 作用 | 不写会怎样 |
|---|---|---|
| `ensure_ascii=False` | 中文原样保存 | 变成 `\uXXXX` 天书 |
| `indent=2` | 缩进两格，分行显示 | 全挤成一行 |

> 🧠 **写 json 的固定咒语：**
> `json.dump(数据, f, ensure_ascii=False, indent=2)`
> 记住它，以后天天用。

---

## 📌 知识卡 4 · 嵌套结构也一样简单 ⭐

Day 31 的队伍数据库，用 json 存起来毫无压力：

```python runnable 整个队伍一次存完
import json

team = [
    {"name": "星野樱", "hp": 340, "skills": ["樱花斩"]},
    {"name": "月见琉璃", "hp": 280, "skills": ["水镜", "治愈"]},
]

save = {
    "player": "小樱",
    "chapter": 3,
    "team": team,
    "items": {"药水": 5, "钥匙": 1},
}

with open("完整存档.json", "w", encoding="utf-8") as f:
    json.dump(save, f, ensure_ascii=False, indent=2)

with open("完整存档.json", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded["team"][1]["skills"])
print(loaded["items"]["药水"])
print(f"章节 {loaded['chapter'] + 1} 即将开始")
```

**列表套字典套列表** —— json 全都原样存取，一点额外代码都不用写。

---

## 📌 知识卡 5 · 不用文件的版本：`dumps` / `loads`

```python runnable 转成字符串，不落盘
import json

role = {"name": "星野樱", "level": 12}

text = json.dumps(role, ensure_ascii=False)
print(text)
print(type(text))

back = json.loads(text)
print(back["name"])
```

| 函数 | 干什么 |
|---|---|
| `json.dump(数据, f)` | 存**进文件** |
| `json.load(f)` | 从**文件**读 |
| `json.dumps(数据)` | 转成**字符串** |
| `json.loads(文本)` | 从**字符串**读 |

> 💡 带 `s` 的是 **s**tring 版。网络传输、日志记录常用它们。

---

## 📌 知识卡 6 · 两个坑

**坑一：json 只认几种类型**

```python runnable 集合存不了（会报错）
import json
data = {"friends": {"樱", "琉璃"}}
print(json.dumps(data))
```

| 能存 | 存不了 |
|---|---|
| 字典、列表、字符串、数字、`True`/`False`/`None` | **集合 `set`**、元组会变成列表、自定义对象 |

集合要先 `list(...)` 转一下。

**坑二：读档文件不存在 / 内容损坏**

```python runnable 双重保护
import json

def load_save(filename):
    """读档。文件不存在或格式坏了都返回 None。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("  （还没有存档）")
        return None
    except json.JSONDecodeError:
        print("  （存档文件损坏了）")
        return None

print(load_save("不存在的存档.json"))

with open("坏存档.json", "w", encoding="utf-8") as f:
    f.write("这不是 json{{{")
print(load_save("坏存档.json"))
```

`json.JSONDecodeError` 是 json 特有的异常 —— 存档被手动改坏时会遇到。

---

## 🛠 今天的任务 · 游戏存档系统

| 函数 | 说明 |
|---|---|
| `new_save(player)` | 返回一个**新存档字典**：player、chapter=1、gold=100、team=[]、items={} |
| `save_game(filename, data)` | 用 json 存档。必须带 `ensure_ascii=False` 和 `indent=2` |
| `load_game(filename)` | 读档。文件不存在或损坏都返回 `None`，各给一句不同的提示 |
| `add_member(data, name, hp)` | 往 `team` 里加一个成员（字典），返回 data |
| `add_item(data, item, count=1)` | 往 `items` 里加道具，**已有就累加数量** |
| `show_save(data)` | 打印存档内容：玩家、章节、金币、队伍、道具 |

主流程要求：

- 开局先 `load_game`，**此时文件不存在**，要提示并用 `new_save` 造一个新的
- 加至少 2 个队员、至少 3 种道具（其中一种要加两次，验证累加）
- 章节 +1、金币 +50
- `save_game` 存盘
- **再 `load_game` 读回来**，用 `show_save` 打印，证明数据完好
- 问玩家一个道具名，加进存档并再次存盘
- 最后写一个损坏的存档文件，用 `load_game` 读它，验证不崩

> ✨ 做完刷新页面，去「📁 文件」里点开 `存档.json` —— 你会看到一个漂亮的、
> 人能读懂的存档文件。**这就是真实游戏存档的样子。**
