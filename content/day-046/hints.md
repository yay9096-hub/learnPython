## 提示 1 · 校验函数只管 raise

```python
MIN_NAME = 2
MAX_NAME = 8


def validate_name(name):
    """检查名字。不合法就抛错，合法返回清理后的名字。"""
    if not isinstance(name, str):
        raise TypeError(f"名字得是文字，你给的是 {type(name).__name__}")

    name = name.strip()
    if len(name) < MIN_NAME:
        raise ValueError(f"名字太短了，至少 {MIN_NAME} 个字（你给的是「{name}」）")
    if len(name) > MAX_NAME:
        raise ValueError(f"名字太长了，最多 {MAX_NAME} 个字（你给了 {len(name)} 个）")
    return name
```

三个要点：

- **类型不对用 `TypeError`，值不对用 `ValueError`**
- 错误信息里带上**实际收到了什么**（判题会检查）
- 合法时返回 `.strip()` 之后的干净名字

⚠️ 这个函数里**一个 `try` 都不要写**。它只负责发现问题、喊出来。

## 提示 2 · 属性校验要列出可选项

```python
ELEMENTS = ["火", "水", "风", "雷"]


def validate_element(el):
    """检查属性。必须是预设的几种之一。"""
    if el not in ELEMENTS:
        options = " / ".join(ELEMENTS)
        raise ValueError(f"不认识的属性「{el}」，只能是：{options}")
    return el
```

用 Day 28 的 `join` 把可选项拼出来 —— 不告诉用户有哪些选择，
她只能瞎猜。

`create_role` 什么都不用管，异常自己会往外传：

```python
def create_role(name, age, element):
    """造一个角色。任何一项不合法都会抛错。"""
    return {
        "name": validate_name(name),
        "age": validate_age(age),
        "element": validate_element(element),
    }
```

## 提示 3 · try 只出现在这一个函数里

```python
def try_register(name, age, element):
    """安全地登记。成功返回 (True, 角色)，失败返回 (False, 错误说明)。"""
    try:
        role = create_role(name, age, element)
    except (ValueError, TypeError) as e:
        return False, str(e)
    return True, role
```

`except (ValueError, TypeError)` —— 括号里写多个类型，一次接住两种。

`str(e)` 把异常对象转成它携带的那句说明文字。

主流程用解包接住两个返回值（Day 39 学的）：

```python
ok, result = try_register("  星野樱  ", 16, "火")
if ok:
    print(f"  ✓ 登记成功：{result}")
else:
    print(f"  ✗ {result}")
```

批量测试非法数据用循环：

```python
bad_cases = [
    ("樱", 16, "火"),
    ("星野樱", -5, "火"),
    ("星野樱", 16, "土"),
]
for name, age, el in bad_cases:
    ok, result = try_register(name, age, el)
    if not ok:
        print(f"  ✗ {result}")
```
