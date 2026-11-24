## 提示 1 · input 的基本形状

```python
name = input("请输入你的名字：")
```

三个零件：

1. `input(...)` —— 括号里放要问的话
2. `=` —— 把回答装进盒子
3. 盒子的名字

## 提示 2 · 数字要套一层 int()

年龄要拿来算数，所以必须转成数字：

```python
age = int(input("请输入你的年龄："))
```

注意括号的层次 —— `int(` 在最外面，`input(` 在里面，**结尾有两个 `)`**。

数一数你的括号够不够。

## 提示 3 · 后面就是熟悉的老朋友了

算出来：

```python
birth_year = 2026 - age
student_id = age * 100 + lucky
```

打印出来（Day 2 学的 f-string）：

```python
print(f"姓名：{name}")
print(f"出生年份：{birth_year}")
```

剩下两行你自己来 ✨
