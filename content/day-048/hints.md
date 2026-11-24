## 提示 1 · read_lines 是所有函数的地基

先把这一个写好，后面五个都靠它：

```python
def read_lines(filename):
    """读成列表，每项已经 strip 过，空行不要。"""
    result = []
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                result.append(line)
    return result
```

两个关键动作：

- **`.strip()`** 削掉行尾的 `\n`（不削的话统计字数会多算）
- **`if line:`** 跳过空行（空字符串在 `if` 里算 False）

有了它，后面几个都是一两行：

```python
def count_lines(filename):
    """有多少篇日记。"""
    return len(read_lines(filename))
```

**复用已有的函数**，别每个都重新打开文件读一遍。

## 提示 2 · 查找和搜索是老套路

查找 —— 找到就立刻返回（Day 41 学的）：

```python
def find_by_date(filename, date):
    """找出某一天的日记。找不到返回 None。"""
    for line in read_lines(filename):
        if line.startswith(date):
            return line
    return None
```

⚠️ `return None` 要跟 `for` 对齐，写在循环**外面**。

搜索 —— 要全部，所以跑完再返回：

```python
def search(filename, keyword):
    """返回所有含关键词的行。"""
    result = []
    for line in read_lines(filename):
        if keyword in line:
            result.append(line)
    return result
```

> 💡 `line.startswith("2026-09-04")` 判断开头，比 `in` 精确 ——
> 日期在行首，用 startswith 不会误匹配到正文里的数字。

## 提示 3 · 行号和主流程

```python
def show_numbered(filename):
    """带行号打印全部日记。"""
    for i, line in enumerate(read_lines(filename), start=1):
        print(f"  {i}. {line}")
```

`start=1` 让编号从 1 开始，省掉 `i + 1`。

主流程别忘了**先造文件**：

```python
build_diary(DIARY, ENTRIES)

print(f"\n共 {count_lines(DIARY)} 篇，一共写了 {count_chars(DIARY)} 个字")

print("\n--- 全部日记 ---")
show_numbered(DIARY)

found = find_by_date(DIARY, "2026-09-04")
if found is None:
    print("  这一天没写")
else:
    print(f"  找到了：{found}")
```

搜索那段要处理「一条都没有」的情况：

```python
hits = search(DIARY, keyword)
if len(hits) == 0:
    print(f"  没有找到含「{keyword}」的日记")
else:
    print(f"  找到 {len(hits)} 条：")
    for line in hits:
        print(f"    · {line}")
```
