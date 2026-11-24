## 提示 1 · try/except 的形状

五个 safe 函数都是同一个套路，只是异常类型不同：

```python
def to_int(text, default=0):
    """把文字转成整数。转不了就返回 default，不崩。"""
    try:
        return int(text)
    except ValueError:
        return default
```

照着换类型就行：

| 函数 | try 里放什么 | 接住哪种错 |
|---|---|---|
| `to_int` | `int(text)` | `ValueError` |
| `to_float` | `float(text)` | `ValueError` |
| `safe_divide` | `a / b` | `ZeroDivisionError` |
| `safe_get` | `data[key]` | `KeyError` |
| `safe_index` | `lst[i]` | `IndexError` |

⚠️ **一定要写明类型**。光写 `except:` 会把你自己写错变量名之类的 bug 也吞掉，
判题会检查这一点。

## 提示 2 · try 里只放可能出错的那一行

```python
def safe_divide(a, b):
    """安全除法。除数为 0 时提示并返回 0。"""
    try:
        return a / b
    except ZeroDivisionError:
        print("  ⚠️ 除数不能是 0，先当作 0 处理")
        return 0
```

`try` 里就一行 `a / b`。别把 `print` 之类不会出错的也包进去 ——
包多了出错时都不知道是哪一行的问题。

## 提示 3 · register 就是把安全函数串起来

```python
def register():
    """完成一次入学登记，返回一个信息字典。乱输也不会崩。"""
    name = input("请输入你的名字：").strip()
    age = to_int(input("请输入你的年龄："))
    height = to_float(input("请输入你的身高（米）："))

    return {
        "name": name,
        "age": age,
        "height": height,
        "birth_year": 2026 - age,
    }
```

它自己不写 `try` —— 因为 `to_int` / `to_float` 已经把危险的事包好了。
**这就是把防御封装成函数的好处：用的地方看起来干干净净。**

主流程记得把三种演示都跑一遍：

```python
print(f"  10 / 0 = {safe_divide(10, 0)}")

role = {"name": "星野樱", "hp": 340}
print(f"  mp = {safe_get(role, 'mp')}")

team = ["星野樱", "月见琉璃"]
print(f"  第 9 个 = {safe_index(team, 9)}")

print("\n✅ 全程没有崩溃")
```
