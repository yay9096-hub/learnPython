## 提示 1 · 每次改状态都要夹取

先写一个共用的小工具，后面全靠它：

```python
def clamp(value, low=0, high=100):
    """把值夹在 low..high 之间。"""
    return max(low, min(value, high))
```

然后每个方法都用它：

```python
    def feed(self, amount=20):
        """喂食。返回实际减少的饥饿值。"""
        before = self.hunger
        self.hunger = clamp(self.hunger - amount)
        self.mood = clamp(self.mood + 5)
        return before - self.hunger
```

⚠️ 判题会用极端值试：`feed(999)` 之后饥饿必须是 **0** 不是负数。

`play` 要**先判断再扣**：

```python
    def play(self, cost=15):
        if self.energy < 20:
            print(f"     😴 {self.name} 太累了，玩不动")
            return False          # ← 提前返回，一个属性都不能动
        self.energy = clamp(self.energy - cost)
        self.mood = clamp(self.mood + 15)
        self.hunger = clamp(self.hunger + 10)
        return True
```

判题会检查「玩不动的时候心情和精力都没变」。

## 提示 2 · to_dict / from_dict 这一对

json 存不了对象，所以要转成字典：

```python
    def to_dict(self):
        """转成能存进 json 的字典。"""
        return {
            "name": self.name,
            "species": self.species,
            "hunger": self.hunger,
            "energy": self.energy,
            "mood": self.mood,
            "age": self.age,
            "alive": self.alive,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典造一只宠物回来。cls 就是 Pet 这个类。"""
        pet = cls(data["name"], data.get("species", "史莱姆"))
        pet.hunger = data.get("hunger", 50)
        pet.energy = data.get("energy", 50)
        pet.mood = data.get("mood", 50)
        pet.age = data.get("age", 0)
        pet.alive = data.get("alive", True)
        return pet
```

三个要点：

- **`@classmethod` 不能漏**，判题会查
- 第一个参数是 **`cls`** 不是 `self`
- 用 `.get(键, 默认值)` 兜底，老存档缺字段也不会崩

## 提示 3 · 存档读档和状态条

```python
def load_pet(filename):
    """读回一只宠物。文件不存在或损坏返回 None。"""
    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("  （还没有宠物，领养一只吧）")
        return None
    except json.JSONDecodeError:
        print("  （存档损坏了）")
        return None
    return Pet.from_dict(data)
```

**两种错要分开接**（Day 50 的规矩）。

状态条抽成一个小方法，三条共用：

```python
    def _bar(self, value):
        """把 0~100 的值画成 10 格的条。"""
        filled = value // 10
        return "█" * filled + "░" * (10 - filled)

    def __str__(self):
        state = "健康" if self.alive else "虚弱"
        return (f"{self.name}（{self.species}·{self.stage()}·{self.age}h）[{state}]\n"
                f"     饥饿 {self._bar(self.hunger)} {self.hunger}\n"
                f"     精力 {self._bar(self.energy)} {self.energy}\n"
                f"     心情 {self._bar(self.mood)} {self.mood}")
```

> 💡 方法名前面加一个下划线 `_bar`，是程序员之间的约定：
> 「这是内部用的，外面别调」。Python 不会真的拦你，纯靠自觉。

主流程开头就是 Day 50 那个套路：

```python
pet = load_pet(SAVE)
if pet is None:
    pet = Pet("小樱", "樱花史莱姆")
    print(f"  ✨ 领养了一只 {pet.species}")
```
