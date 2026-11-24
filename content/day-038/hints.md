## 提示 1 · 默认值写在参数后面

```python
def create_role(name, hp=100, mp=50, atk=30, element="无", level=1):
    """造一个角色字典。除了名字，其余都有默认值。"""
    return {
        "name": name,
        "hp": hp,
        "mp": mp,
        "atk": atk,
        "element": element,
        "level": level,
        "skills": [],
    }
```

⚠️ 没默认值的 `name` 必须放**最前面**，有默认值的排后面。反过来会直接语法错误。

这样一来三种调用方式都能用：

```python
create_role("路人甲")                              # 全用默认
create_role("星野樱", 340, 180, 88, "火", 12)      # 全部给
create_role("月见琉璃", element="水", level=8)      # 点名只改两项
```

## 提示 2 · 今天的重点坑：默认值别用列表

```python
def add_skill(role, skill, skills=None):
    """给角色加一个技能。默认值用 None，避免可变默认值的坑。"""
    if skills is None:
        skills = role["skills"]
    skills.append(skill)
    role["skills"] = skills
    return role
```

⚠️ **绝对不能写 `skills=[]`**。默认的空列表在函数定义时只创建一次，
之后每次调用都是**同一个列表** —— 给甲加的技能会跑到乙身上。

判题专门有一条在验这个：造两个角色，给甲加技能，检查乙有没有被污染。

**记住：默认值只用数字、文字、True/False、None 这些不可变的东西。**

## 提示 3 · 血条要用参数画

```python
def show_role(role, width=20, char="█"):
    """打印角色卡，血条宽度和符号都可以换。"""
    filled = int(role["hp"] / 400 * width)
    if filled > width:
        filled = width
    bar = char * filled + "░" * (width - filled)

    name = role["name"]
    lv = role["level"]
    el = role["element"]
    print(f"  {name} Lv.{lv} [{el}]")
    print(f"    HP {bar} {role['hp']}")
    print(f"    MP {role['mp']}   ATK {role['atk']}")
```

⚠️ `bar` 一定要用参数里的 `char` 拼，不能写死 `"█"` ——
判题会传 `char="@"` 进来检查。

> 💡 f-string 里想取字典的值，里层用**单引号**：`{role['hp']}`。
> 嫌容易搞错，就像上面那样先用普通变量接出来再写进 f-string。
