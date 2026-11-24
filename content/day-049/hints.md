## 提示 1 · 今天的核心：读之前先兜底

```python
def load_notes(filename):
    """读全部错题。文件还不存在就返回空列表。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
```

⚠️ 返回 **`[]` 而不是 `None`** —— 这样调用方能直接 `for` 遍历、直接 `len()`，
不用每次先判断。

也可以用 `os.path.exists` 版：

```python
import os

def load_notes(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]
```

两种都算过。

## 提示 2 · 写入完全不用担心

```python
def add_note(filename, question, answer):
    """追加一条错题。a 模式会自动创建文件，不用检查。"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{question} | {answer}\n")
```

`"a"` 模式**文件不存在就自动创建** —— 所以这里一个检查都不用写。

**只有读才需要担心文件在不在。**

清空用 `"w"` 写个空字符串：

```python
def clear_notes(filename):
    """清空错题本，但文件保留。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")
```

## 提示 3 · 显示时拆开两个字段

```python
def show_notes(filename):
    """带编号显示全部错题。一条都没有时给个提示。"""
    notes = load_notes(filename)
    if len(notes) == 0:
        print("  📭 错题本还是空的，加油别错题 ✨")
        return

    for i, note in enumerate(notes, start=1):
        parts = note.split("|")
        question = parts[0].strip()
        answer = parts[1].strip() if len(parts) > 1 else ""
        print(f"  {i}. ❓ {question}")
        print(f"     ✅ {answer}")
```

两个要点：

- 空的时候**提前 `return`**，省掉 else（Day 37 学的）
- `parts[1] if len(parts) > 1 else ""` 是防御：万一某行没有分隔符也不会崩

主流程第一句就是考验：

```python
print("\n--- 第一次打开（文件还不存在）---")
show_notes(NOTES)
```

这时候文件确实不存在。撑住了，说明今天的功课到位了 ✨
