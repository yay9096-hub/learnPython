# Day 63 · 宠物养成 🐣

> 「第六章最后一关。做一只**电子宠物** ——
> 会饿、会困、会开心、会长大，而且**关掉浏览器它还活着**。
>
> 这一关要把第五章的存档和第六章的类**合起来用**。」

---

## 🔍 第六章你拿到的武器

| 天 | 学到的 | 一句话 |
|---|---|---|
| D55 | `class` / `__init__` / `self` | 数据和本事装进一个盒子 |
| D56 | 方法 | 对象自己会做事 |
| D57 | 属性保护 | 类自己守住不变量 |
| D58 | 类的组合 | 一个类装着一堆别的对象 |
| D59 | 继承 / `super()` | 共同的写一次 |
| D60 | 重写 / 多态 | 同名方法，各自的实现 |
| D61 | 特殊方法 | 用起来像内置类型 |
| D62 | 多类协作 | 一个完整的游戏 |

**九天前你还在用字典存角色。现在你能设计一整套类了。**

---

## 🧩 复习卡 · 四个最容易忘的

### 1. 子类 `__init__` 第一句是 `super()`

```python runnable 忘了就没有父类的属性
class A:
    def __init__(self, name):
        self.name = name

class B(A):
    def __init__(self, name, extra):
        super().__init__(name)
        self.extra = extra

b = B("樱", 1)
print(b.name, b.extra)
```

### 2. 属性要夹在合法范围里

```python runnable 夹取
value = 150
print(max(0, min(value, 100)))
```

### 3. 特殊方法让类好用

```python runnable __str__ 和 __len__
class Box:
    def __init__(self):
        self.items = ["a", "b"]
    def __str__(self):
        return f"盒子（{len(self.items)} 件）"
    def __len__(self):
        return len(self.items)

b = Box()
print(b)
print(len(b))
```

### 4. 对象存进 json 要先转成字典

```python runnable 对象不能直接存 json
import json

class Pet:
    def __init__(self, name):
        self.name = name

    def to_dict(self):
        """转成能存进 json 的字典。"""
        return {"name": self.name}


p = Pet("小樱")
print(json.dumps(p.to_dict(), ensure_ascii=False))
```

> 🧠 **json 只认字典、列表、数字、字符串** —— 对象存不进去。
> 标准做法是给类加一对方法：
> **`to_dict()` 转出去，`from_dict()` 读回来。**

---

## 📌 知识卡 · `@classmethod` —— 另一种造对象的方式 ⭐

今天唯一的新东西。

存档读回来是一个**字典**，怎么变回 `Pet` 对象？

```python runnable classmethod 造对象
class Pet:
    def __init__(self, name, hunger=50):
        self.name = name
        self.hunger = hunger

    def to_dict(self):
        return {"name": self.name, "hunger": self.hunger}

    @classmethod
    def from_dict(cls, data):
        """从字典造一只宠物回来。cls 就是 Pet 这个类本身。"""
        return cls(data["name"], data["hunger"])

    def __str__(self):
        return f"{self.name}（饥饿 {self.hunger}）"


p = Pet("小樱", 30)
saved = p.to_dict()
print(saved)

restored = Pet.from_dict(saved)
print(restored)
```

三个要点：

- **`@classmethod`** 写在 `def` 上面一行，叫**装饰器**
- 第一个参数不是 `self` 而是 **`cls`** —— 它指的是**类本身**
- 调用时用**类名**：`Pet.from_dict(...)`，不需要先有一个对象

> 💡 为什么不写成普通函数？
> 因为 `from_dict` 逻辑上就属于 `Pet` —— 挂在类上，
> 别人一看 `Pet.` 就知道有这个入口。

不想用 `@classmethod` 也行，写个普通函数 `def pet_from_dict(data):` 一样能过，
但学会它你就看得懂真实项目里的代码了。

---

## 🎯 今天的作品 · 电子宠物

### `Pet` 类

| 成员 | 说明 |
|---|---|
| `__init__(self, name, species="史莱姆")` | 属性：`name` `species` `hunger=50` `energy=50` `mood=50` `age=0` `alive=True` |
| `feed(self, amount=20)` | 喂食：饥饿 **-amount**，心情 +5。**都夹在 0~100**。返回实际减少的饥饿值 |
| `sleep(self, hours=1)` | 睡觉：精力 `+hours*20`，饥饿 `+hours*10`，年龄 `+hours`。夹取 |
| `play(self, cost=15)` | 玩耍：精力不足 20 时返回 `False` 并提示；否则精力 -cost、心情 +15、饥饿 +10，返回 `True` |
| `tick(self)` | 时间流逝一小时：饥饿 +8、精力 -5、年龄 +1；**饥饿满 100 时心情 -20**；心情/精力都归零时 `alive=False` |
| `is_hungry(self)` | 饥饿 > 70 |
| `stage(self)` | 按 `age` 返回成长阶段：<10 幼年、<30 少年、否则成年 |
| `to_dict(self)` | 转成字典 |
| `from_dict(cls, data)` | **类方法**，从字典造回来 |
| `__str__(self)` | 一行状态，含名字、阶段、三条状态**条**（用方块画） |

### 存档

| 函数 | 说明 |
|---|---|
| `save_pet(filename, pet)` | 用 json 存 `pet.to_dict()` |
| `load_pet(filename)` | 读回来变成 `Pet` 对象；文件不存在或损坏返回 `None` |

### 主流程

- 先 `load_pet`，没有存档就新建一只并提示
- 打印初始状态
- 演示 `feed`、`sleep`、`play` 各至少一次，每次打印状态
- 演示**精力不足时 `play` 会失败**
- 用循环让时间流逝至少 5 小时（`tick`），每小时打印状态
- 打印它现在的成长阶段
- 问玩家想做什么（`喂食` / `睡觉` / `玩耍`），执行并打印
- **存档**，再 `load_pet` 读回来验证数据一致

> ⚠️ 所有状态值都要**夹在 0~100** —— 判题会用极端值试。
