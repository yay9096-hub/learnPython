## 提示 1 · 一步一步来，别想着一行写完

先把要用的材料准备好：

```python
name = input("请输入你的名字：")
element = input("请输入属性英文：")
rank = len(name)
stars = "★" * rank
```

最后再拼句子。**先备料，再下锅**，这是写程序的通用顺序。

## 提示 2 · strip 接在哪

`.strip()` 直接跟在 `input(...)` 后面，一气呵成：

```python
name = input("请输入你的名字：").strip()
```

也可以分两步写，效果一样：

```python
name = input("请输入你的名字：")
name = name.strip()
```

⚠️ 第二行的 `name =` 不能省 —— 方法不会改原来的变量，得自己接住结果。

## 提示 3 · 最后的称号怎么拼

```python
print(f"✧･ﾟ:*  {stars}  *:･ﾟ✧")
print(f"【{element.upper()} 之子】{name} · {rank} 阶魔导士")
```

大括号里是可以**放方法调用**的，`{element.upper()}` 完全合法。
