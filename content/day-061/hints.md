## 提示 1 · 两个「显示」方法

```python
    def __str__(self):
        """print(角色) 时显示的样子。给用户看。"""
        return f"【{self.name}】HP {self.hp}/{self.max_hp}  ATK {self.atk}"

    def __repr__(self):
        """调试时显示的样子。给程序员看。"""
        return f"Role({self.name!r}, {self.hp}, {self.atk})"
```

区别：

- `print(r)` 和 f-string 用 **`__str__`**
- `print([r, r])`（打印列表）用 **`__repr__`**

`{self.name!r}` 里的 `!r` 让字符串自带引号，输出成 `Role('星野樱', 340, 88)`。

⚠️ 两个都**必须返回字符串**，返回别的会报错。

## 提示 2 · `__eq__` 的类型检查不能少

```python
    def __eq__(self, other):
        """名字一样就算同一个角色。"""
        if not isinstance(other, Role):
            return False                      # ← 这一句很关键
        return self.name == other.name
```

不写第一句的话，`角色 == "星野樱"` 会去取字符串的 `.name`，直接崩。

有了 `__eq__`，**`in` 也跟着变聪明** —— 因为 `in` 内部用的就是 `==`：

```python
print(Role("星野樱") in roles)      # True
```

`__lt__` 更简单：

```python
    def __lt__(self, other):
        """比大小的规则：按攻击力。"""
        return self.atk < other.atk
```

有了它，`sorted(roles)` / `max(roles)` / `min(roles)` **全都不用写 `key=`**。

## 提示 3 · Team 的三个方法

```python
    def __str__(self):
        return f"《{self.name}》共 {len(self.members)} 人"

    def __len__(self):
        return len(self.members)

    def __contains__(self, name):
        """支持「名字 in 队伍」。"""
        for m in self.members:
            if m.name == name:
                return True
        return False
```

有了 `__len__`，**空队伍在 `if` 里自动就是 `False`** —— 不用额外写什么：

```python
if team:
    print("有人")
if not empty:
    print("空的")
```

⚠️ 主流程里**不许出现 `.members`**。判题会检查。
这正是特殊方法的意义：把内部实现藏起来，外面只看到干净的 `len(team)` 和 `in`。

## 提示 4 · 主流程要演示的清单

```python
print(sakura)                                # __str__
print(roles)                                 # __repr__（列表）
print(sakura == same_name)                   # True，同名
print(sakura == "星野樱")                     # False，跟字符串比
print(Role("星野樱") in roles)                # True，__eq__ 让 in 变聪明
print(sorted(roles))                         # __lt__，不写 key
print(max(roles).name, min(roles).name)
print(len(team), "星野樱" in team)            # __len__ 和 __contains__
```
