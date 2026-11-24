## 提示 1 · 建字典和取值

```python
role = {
    "name": "星野樱",
    "level": 12,
    "hp": 340,
    "mp": 180,
    "element": "火",
}
```

**大括号**，里面 `键: 值`，逗号隔开。竖着写更好读。

取值时方括号里放**键名**（要带引号）：

```python
print(f"姓名：{role['name']}")
print(f"等级：{role['level']}")
```

⚠️ f-string 里面已经用了双引号，里层就用**单引号** `role['name']`，
不然引号会打架（Day 6 学过的坑）。

## 提示 2 · 改和新增写法一样

```python
role["hp"] = 500              # 键已存在 -> 修改
role["title"] = "樱花剑姬"     # 键不存在 -> 新增
```

字典不用像列表那样担心「越界」—— 键不存在，赋值就自动加上了。

用 `len(role)` 数有几项：

```python
print(f"档案现在有 {len(role)} 项属性")
```

## 提示 3 · 安全查询和删除

```python
key = input("想查哪一项？").strip()

if key in role:
    print(f"🔎 {key} = {role[key]}")
else:
    print(f"🔎 档案里没有这一项：「{key}」")
```

⚠️ `in` 查的是**键**，不是值。查「星野樱」是查不到的，要查「name」。

也可以用 `.get()` 一句搞定：

```python
value = role.get(key, "（没有这一项）")
print(f"🔎 {key} = {value}")
```

删除并拿到被删的值：

```python
removed = role.pop("mp")
print(f"🗑 移除了 mp，它原来的值是 {removed}")
```

`.pop()` 跟列表的用法一样 —— **删掉并返回**，所以要用 `=` 接住。
