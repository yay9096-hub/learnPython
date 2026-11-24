# Day 49 · 错题本 📓

> 「昨天的阅读器有个致命弱点：**文件必须已经存在**。
>
> 但真实的程序第一次运行时，什么文件都没有 ——
> 用户第一次打开你的日记本，`日记.txt` 还不存在呢。
>
> 今天学会优雅地处理『还没有』这件事。」

---

## 📌 知识卡 1 · 读不存在的文件会崩

```python runnable 第一次运行的惨状
with open("从来没有的文件.txt", encoding="utf-8") as f:
    print(f.read())
```

`FileNotFoundError` —— 程序当场结束。

回忆一下 Day 47 的表：

| 模式 | 文件不存在时 |
|---|---|
| `"w"` | 自动创建 ✅ |
| `"a"` | 自动创建 ✅ |
| `"r"`（读） | **报错** ❌ |

只有**读**会出这个问题。

---

## 📌 知识卡 2 · 办法一：先检查 `os.path.exists`

```python runnable 读之前先问一句
import os

filename = "错题本.txt"

if os.path.exists(filename):
    with open(filename, encoding="utf-8") as f:
        print(f.read())
else:
    print("错题本还是空的，加油别错题 ✨")
```

`os.path.exists(路径)` 返回 `True` / `False`。

配套的还有两个：

```python runnable 三个检查工具
import os

with open("测试.txt", "w", encoding="utf-8") as f:
    f.write("x")

print(os.path.exists("测试.txt"))
print(os.path.isfile("测试.txt"))
print(os.path.isdir("测试.txt"))
print(os.listdir("."))
```

`os.listdir(".")` 列出当前目录的所有文件 —— 跟右边「📁 文件」标签看到的一样。

---

## 📌 知识卡 3 · 办法二：`try` 接住（更推荐）⭐

```python runnable try 版
def load_notes(filename):
    """读错题本。文件还没有就返回空列表。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

print(load_notes("还没有的错题本.txt"))
print(len(load_notes("还没有的错题本.txt")))
```

**返回空列表而不是 None** —— 这样调用方可以直接拿去遍历，
不用先判断（Day 41 学过的原则）。

### 两种办法怎么选

| | `os.path.exists` | `try / except` |
|---|---|---|
| 好读 | ✅ 意图明显 | 稍微绕一点 |
| 安全 | ⚠️ 有个小缝隙 | ✅ 更可靠 |

那个「小缝隙」是：检查完到真正打开之间，文件**有可能刚好被删掉**。
概率极低，但 `try` 版从原理上就没这个问题。

> 🧠 Python 社区的习惯说法：
> **「请求原谅比请求许可容易」** —— 先做，出错再处理。

---

## 📌 知识卡 4 · 追加模式做日志 ⭐

错题本天生适合用 `"a"`：

```python runnable 一条条往上加
def add_note(filename, question, answer):
    """往错题本里追加一条。"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{question} | {answer}\n")


def load_notes(filename):
    try:
        with open(filename, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []


add_note("错题.txt", "int 和 str 能相加吗", "不能，要先 str() 转换")
add_note("错题.txt", "列表编号从几开始", "从 0")
add_note("错题.txt", "sort 返回什么", "什么都不返回，它直接改原列表")

for i, note in enumerate(load_notes("错题.txt"), start=1):
    print(f"{i}. {note}")
```

⚠️ 注意 `add_note` **一次都没检查文件存不存在** ——
因为 `"a"` 模式会自动创建。**只有读才需要担心。**

---

## 📌 知识卡 5 · 用分隔符存多个字段

上面用 `|` 把题目和答案分开，读出来时用 `split` 拆开（Day 28）：

```python runnable 存进去、拆出来
with open("错题.txt", "w", encoding="utf-8") as f:
    f.write("列表编号从几开始 | 从 0\n")
    f.write("sort 返回什么 | 什么都不返回\n")

with open("错题.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split("|")
        question = parts[0].strip()
        answer = parts[1].strip() if len(parts) > 1 else ""
        print(f"  ❓ {question}")
        print(f"  ✅ {answer}")
```

⚠️ 分隔符要挑**内容里不会出现的字符**。用逗号的话，
题目里本来就有逗号就会拆错。`|` 比较安全。

> 💡 这种「一行一条记录、字段用符号分开」的格式，
> 就是 CSV 的雏形 —— 第 52 天会正式学。
> 明天学的 `json` 则是更省心的做法：不用自己拆。

---

## 📌 知识卡 6 · 删除和覆盖

```python runnable 清空 vs 删除
import os

with open("临时.txt", "w", encoding="utf-8") as f:
    f.write("一些内容")
print(f"存在吗：{os.path.exists('临时.txt')}")

with open("临时.txt", "w", encoding="utf-8") as f:
    pass
print(f"清空后还在吗：{os.path.exists('临时.txt')}")

os.remove("临时.txt")
print(f"删除后还在吗：{os.path.exists('临时.txt')}")
```

- 用 `"w"` 打开再什么都不写 = **清空但文件还在**
- `os.remove(路径)` = **文件真的没了**

⚠️ `os.remove` 删不存在的文件会抛 `FileNotFoundError`，
所以删之前也要检查或者 try。

---

## 🛠 今天的任务 · 我的错题本

| 函数 | 说明 |
|---|---|
| `load_notes(filename)` | 读全部错题，**文件不存在返回空列表** |
| `add_note(filename, question, answer)` | 追加一条，格式 `题目 \| 答案` |
| `count_notes(filename)` | 有几条 |
| `search_notes(filename, keyword)` | 搜题目或答案里含关键词的，返回列表 |
| `show_notes(filename)` | 带编号显示全部，一条都没有要提示 |
| `clear_notes(filename)` | 清空错题本（用 `"w"` 写空） |

主流程要求：

- **一开始就调用 `show_notes`** —— 此时文件还不存在，必须不崩
- 用 `add_note` 加至少 3 条错题
- 用 `show_notes` 再显示一次
- 打印总条数
- 问玩家一道错题（题目 + 答案），加进去
- 用 `search_notes` 搜一个关键词，找不到要提示
- 最后 `clear_notes` 清空，再 `show_notes` 一次证明真的空了

> ⚠️ **第一次运行时错题本文件是不存在的** —— 这正是今天要解决的问题。
> 判题会先确保文件不存在，再跑你的代码。
