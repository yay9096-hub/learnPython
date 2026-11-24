## 提示 1 · 函数的形状

```python
def show_line():
    """打印一条分隔线，宽度 28。"""
    print("─" * 28)
```

四个零件：

1. `def` 关键字
2. 函数名 + **一对空括号**
3. 这一行结尾的**冒号**
4. 下面**缩进**的函数体（第一行是三引号说明）

⚠️ 写完 `def` 不会有任何输出 —— 那只是「登记」。要执行必须调用：

```python
show_line()
```

## 提示 2 · 小零件拼大零件

```python
def show_title():
    """打印带上下分隔线的战斗标题。"""
    show_line()
    print("      ⚔️  战 斗 开 始  ⚔️")
    show_line()
```

在一个函数里调用另一个函数，完全没问题 —— 这正是拆分问题的意义。

⚠️ 前提是 `show_line` 要**先定义**（写在 `show_title` 上面）。

剩下三个照着写：

```python
def show_hero():
    """打印我方角色信息。"""
    print("【我方】星野樱 · 樱花剑姬")
    print("  HP 340 / 340    ATK 88")
```

## 提示 3 · 主流程写在最下面

所有 `def` 写完之后，空两行，再写主流程：

```python
# ---------- 主流程 ----------
show_title()
show_hero()
show_line()
show_enemy()
show_victory()
```

⚠️ 这里每一句**都要有括号** —— 写 `show_hero` 不加括号，什么都不会发生。

胜利画面里可以用循环，让它更花哨一点：

```python
def show_victory():
    """打印胜利画面。"""
    show_line()
    for i in range(3):
        print("✨" * (i + 1) + " VICTORY " + "✨" * (i + 1))
    print("  获得经验 120 · 金币 45")
    show_line()
```
