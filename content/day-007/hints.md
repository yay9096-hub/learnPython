## 提示 1 · 一幕一幕来，别想着一口气写完

这一关比前面长，但**每一块你都做过**。

建议顺序：

1. 先只写第一幕，运行一次，看到标题框出现
2. 再加第二幕的四个 input，运行一次，确认它会问你问题
3. 再加计算，运行一次，用 `print(hp)` 检查算得对不对
4. 最后才做第三幕的排版

**每写完一小块就运行一次**，这是程序员最重要的习惯 ——
出错时你能一眼知道是刚才那几行的问题。

## 提示 2 · 第二幕的四问

```python
name = input("旅人，你叫什么名字？").strip()
age = int(input("你今年多大？"))
element = input("你的属性是？").strip()
lucky = int(input("说一个幸运数字："))
```

对照检查三件事：

- 名字有没有 `.strip()`
- 年龄和幸运数字有没有 `int()`
- 顺序对不对（测试会按这个顺序喂数据）

## 提示 3 · 计算和排版

```python
hp = age * 20 + lucky
mp = age * 10 + lucky * 2
rank = len(name)
title = element.upper()
stars = "★" * rank
```

角色卡：

```python
print(f"{stars} 角色创建完成 {stars}")
print(f"【{title} 之子】{name} · {rank} 阶魔导士")
print("HP: " + str(hp), "MP: " + str(mp), sep="  |  ")
print(f"\n樱花飘落。\n{name}，你的故事从这里开始。")
```

最后那个 `\n` 就是旁白的换行，别忘了 ✨
