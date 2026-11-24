# Day 47 · 我的日记本 📝

> 「到今天为止，你的程序有个共同的悲剧：
> **一关掉，什么都没了。**
>
> Day 24 的背包、Day 31 的队伍、Day 39 造的角色 ——
> 全在内存里，程序一结束就烟消云散。
>
> 今天开始，它们能活下来了。」

---

## 📌 知识卡 1 · 写第一个文件 ⭐

```python runnable 三行，产生一个真的文件
with open("我的日记.txt", "w", encoding="utf-8") as f:
    f.write("2026 年 9 月 2 日\n")
    f.write("今天我的程序学会记住东西了！")

print("写好了！看看右边的「📁 文件」标签页 →")
```

点 ▶ 运行，然后**切到右边的「📁 文件」标签** —— 你会看到 `我的日记.txt` 躺在那里。

**更神奇的是：刷新页面，它还在。**（试试看！）

---

## 📌 知识卡 2 · 拆解这一行

```
with open("我的日记.txt", "w", encoding="utf-8") as f:
 ↑     ↑        ↑          ↑         ↑           ↑
 |   打开    文件名       模式      编码       起个名字
 用完自动关
```

| 部分 | 作用 |
|---|---|
| `open(...)` | 打开文件 |
| `"w"` | **模式**：写入 |
| `encoding="utf-8"` | 编码。**中文必须写这个** |
| `as f` | 给打开的文件起个名字，后面用 `f` 操作它 |
| `with` | 用完**自动关掉**文件 |

### ⚠️ 中文和 encoding

```python runnable 不写 encoding 在有些电脑上会乱码
with open("测试.txt", "w", encoding="utf-8") as f:
    f.write("星野樱")

with open("测试.txt", encoding="utf-8") as f:
    print(f.read())
```

Windows 上不写 `encoding="utf-8"` 会默认用 GBK，
在别的电脑上打开就是乱码。**养成习惯：读写都带上它。**

---

## 📌 知识卡 3 · 为什么要 `with`

不用 `with` 的写法长这样：

```python runnable 手动开关（不推荐）
f = open("手动.txt", "w", encoding="utf-8")
f.write("手动开的文件")
f.close()

print("要自己记得 close()")
```

问题在于：**中间一旦出错，`close()` 就跑不到了**，文件一直开着。

`with` 帮你解决了 —— 不管中间发生什么（包括抛异常），
离开这个块时文件**一定**会被关上。这就是 Day 45 学的 `finally` 的思路。

> 🧠 铁律：**操作文件永远用 `with`。**

---

## 📌 知识卡 4 · `"w"` 会清空原来的内容 ⚠️

```python runnable w 是覆盖，不是追加
with open("覆盖测试.txt", "w", encoding="utf-8") as f:
    f.write("第一次写的内容")

with open("覆盖测试.txt", "w", encoding="utf-8") as f:
    f.write("第二次写的内容")

with open("覆盖测试.txt", encoding="utf-8") as f:
    print(f.read())
```

第一次写的**完全没了**。

`"w"` 的意思是「从头开始写」，它会先把文件清空。

想接在后面写？用 `"a"`（append）：

```python runnable a 是追加
with open("追加测试.txt", "w", encoding="utf-8") as f:
    f.write("第一行\n")

with open("追加测试.txt", "a", encoding="utf-8") as f:
    f.write("第二行\n")

with open("追加测试.txt", "a", encoding="utf-8") as f:
    f.write("第三行\n")

with open("追加测试.txt", encoding="utf-8") as f:
    print(f.read())
```

| 模式 | 意思 | 文件不存在时 |
|---|---|---|
| `"w"` | 写入（**先清空**） | 自动创建 |
| `"a"` | 追加（接在末尾） | 自动创建 |
| `"r"` | 只读（默认） | **报错** |

---

## 📌 知识卡 5 · `write` 不会自动换行 ⚠️

```python runnable 忘了 \n 会全挤在一起
with open("挤一起.txt", "w", encoding="utf-8") as f:
    f.write("第一句")
    f.write("第二句")
    f.write("第三句")

with open("挤一起.txt", encoding="utf-8") as f:
    print(f.read())
```

跟 `print` 不一样，**`write` 不会自动加换行**。要换行得自己写 `\n`：

```python runnable 自己加 \n
lines = ["第一句", "第二句", "第三句"]

with open("分行.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")

with open("分行.txt", encoding="utf-8") as f:
    print(f.read())
```

也可以用 Day 28 的 `join` 一次搞定：

```python runnable join 一次写完
lines = ["第一句", "第二句", "第三句"]

with open("join版.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

with open("join版.txt", encoding="utf-8") as f:
    print(f.read())
```

---

## 📌 知识卡 6 · `writelines` 和一个坑

```python runnable writelines 也不加换行
lines = ["甲\n", "乙\n", "丙\n"]

with open("多行.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

with open("多行.txt", encoding="utf-8") as f:
    print(f.read())
```

`writelines` 名字里有 lines，**但它一样不会帮你加换行** ——
列表里的每一项都得自己带 `\n`。

（说实话，用 `"\n".join(...)` 更省心。）

---

## 🛠 今天的任务 · 我的日记本

做一个能记日记的程序：

| 函数 | 说明 |
|---|---|
| `write_diary(filename, date, content)` | 用 `"w"` 写一篇日记，包含日期和正文 |
| `append_diary(filename, date, content)` | 用 `"a"` 追加一篇，不覆盖原来的 |
| `write_lines(filename, lines)` | 把一个列表写成多行，**每行都要换行** |
| `save_role(filename, role)` | 把一个角色字典写成好看的多行文本 |

主流程要求：

- 用 `write_diary` 写第一篇日记到 `日记.txt`
- 用 `append_diary` 再追加**两篇**，三篇都要在文件里
- 用 `write_lines` 把一个至少 4 项的清单写到 `待办.txt`
- 用 `save_role` 把一个角色写到 `角色卡.txt`
- 问玩家写一句话，追加到 `日记.txt` 里
- 每写完一个文件，用 `open(...)` 读回来打印，**证明真的写进去了**

> 💡 全部用 `with open(...)`，全部带 `encoding="utf-8"`。
>
> ✨ 做完之后**刷新一下页面**，看看右边「📁 文件」里的东西还在不在 ——
> 那就是你的程序第一次真正记住了东西。
