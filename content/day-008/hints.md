## 提示 1 · 五角星就是同一句话说五遍

一颗五角星 = 重复 5 次「前进 200，右转 144」。

starter 里已经写好第 1 组了，你把剩下的 4 组复制粘贴出来就行：

```python
turtle.forward(200)
turtle.right(144)
```

⚠️ 最后一条边画完之后可以不用再转，星星就闭合了。

（是的，这很啰嗦。第 11 天学了循环，这 9 行会变成 3 行。）

## 提示 2 · 挪窝的标准三步

想换个地方画东西，永远是这三步：

```python
turtle.penup()          # 1. 抬笔
turtle.goto(0, -60)     # 2. 挪过去
turtle.pendown()        # 3. 落笔
```

少了第 1 步，会拖出一条难看的线；少了第 3 步，后面画什么都不会显示。

## 提示 3 · 光环和署名

```python
# 光环
turtle.penup()
turtle.goto(0, -60)
turtle.pendown()
turtle.pencolor("#8B5CF6")
turtle.circle(120)

# 署名
turtle.penup()
turtle.goto(-40, -140)
turtle.pendown()
turtle.pencolor("#EC6FA9")
turtle.write("星野樱", font=("", 22, "normal"))
```

坐标系提醒：画布正中间是 `(0, 0)`，**往右 x 变大，往上 y 变大**，
所以 `-140` 是画布下方。
