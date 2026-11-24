## 提示 1 · 写文件的固定形状

```python
def write_diary(filename, date, content):
    """用 w 模式写一篇日记。会清空文件原有内容。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"【{date}】\n")
        f.write(content + "\n\n")
```

四个零件缺一不可：

- `with` —— 用完自动关
- `"w"` 或 `"a"` —— 模式
- `encoding="utf-8"` —— 中文必须写
- `as f` —— 后面用 `f.write(...)`

⚠️ **`write` 不会自动换行**，每行末尾要自己加 `"\n"`。

追加版只改一个字母：

```python
def append_diary(filename, date, content):
    """用 a 模式追加一篇日记，保留之前写的。"""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"【{date}】\n")
        f.write(content + "\n\n")
```

`"w"` 会**清空**，`"a"` 会**接在后面**。第一篇用 w、后面用 a，三篇才都在。

## 提示 2 · 列表和字典怎么写进文件

列表 —— 遍历时每行补一个换行：

```python
def write_lines(filename, lines):
    """把一个列表写成多行文本，每行末尾都有换行。"""
    with open(filename, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")
```

字典 —— 用 Day 30 的 `.items()`：

```python
def save_role(filename, role):
    """把一个角色字典写成好看的多行文本。"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== 角色卡 ===\n")
        for key, value in role.items():
            f.write(f"{key}: {value}\n")
        f.write("==============\n")
```

## 提示 3 · 读回来验证

写一个小函数专门用来「证明真的写进去了」：

```python
def show_file(filename):
    """把文件内容读回来打印。"""
    with open(filename, encoding="utf-8") as f:
        print(f.read())
```

⚠️ 读的时候**模式可以省略**（默认就是 `"r"` 只读），
但 `encoding="utf-8"` 还是要写。

主流程串起来：

```python
write_diary("日记.txt", "2026-09-02", "今天我的程序学会记住东西了！")
append_diary("日记.txt", "2026-09-03", "写文件比我想的简单。")
append_diary("日记.txt", "2026-09-04", "刷新页面文件还在，有点感动。")

extra = input("\n再写一句今天的心情：").strip()
append_diary("日记.txt", "2026-09-04 补记", extra)

print("--- 日记.txt ---")
show_file("日记.txt")
```

> ✨ 做完记得**刷新页面**，去右边「📁 文件」看看它们还在不在。
