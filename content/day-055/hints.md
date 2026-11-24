## 提示 1 · 类的形状

```python
class Role:
    """一个游戏角色。除了名字，其余属性都有默认值。"""

    def __init__(self, name, hp=100, mp=50, atk=30, element="无"):
        self.name = name
        self.hp = hp
        self.max_hp = hp        # 满血值记下来，以后治疗要用
        self.mp = mp
        self.atk = atk
        self.element = element
        self.alive = True
```

三个必须注意的点：

- **`self` 是第一个参数**，而且调用时不用你传（`Role("樱")` 只给一个值）
- **`self.xxx = xxx`** 才是「存进这个对象」；只写 `xxx = ...` 是函数里的临时变量
- `max_hp` 和 `alive` **不是参数**，是在 `__init__` 里现设的 ——
  属性不一定都来自参数

## 提示 2 · 造对象和取属性

```python
passerby = Role("路人甲")                          # 全用默认值
sakura = Role("星野樱", 340, 180, 88, "火")        # 全部按顺序给
ruri = Role("月见琉璃", element="水", atk=95)      # 关键字参数
rin = Role("水城凛", 250, 90, 110, "水")
```

取属性用**点号**，不是方括号：

```python
print(f"  {r.name}  HP {r.hp}/{r.max_hp}  ATK {r.atk}  [{r.element}]")
```

⚠️ `r["name"]` 是字典的写法，对象会报 TypeError。

## 提示 3 · 第三章的本事全都能用

把对象装进列表之后，排序、统计、筛选一模一样：

```python
team = [passerby, sakura, ruri, rin]

for r in team:
    print(f"  {r.name}  HP {r.hp}  ATK {r.atk}")

total = sum(r.hp for r in team)
strongest = max(team, key=lambda r: r.atk)
```

唯一的区别：**`r["hp"]` 变成了 `r.hp`**。

最后验证「实例独立」：

```python
sakura.hp = sakura.hp - 100

for r in team:
    print(f"  {r.name}  HP {r.hp}/{r.max_hp}")
```

只有星野樱掉血，别人纹丝不动 —— 因为每个对象的属性都存在**它自己**身上。
