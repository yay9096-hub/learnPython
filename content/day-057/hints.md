## 提示 1 · 夹取：一行守住上下界

```python
    def take_damage(self, amount):
        """受伤。血量最低到 0，返回实际扣掉的血。"""
        if amount < 0:
            raise ValueError(f"伤害不能是负数（收到 {amount}）")
        before = self.hp                          # ① 先记下来
        self.hp = max(0, self.hp - amount)        # ② 夹取：不低于 0
        self.alive = self.hp > 0                  # ③ 同步状态
        actual = before - self.hp                 # ④ 算实际变化
        return actual
```

四个动作缺一不可：

- **参数校验**在最前面（负数直接拒绝）
- **`max(0, ...)`** 守住下界
- **同步 `alive`** —— 血量和存活状态必须一致
- **返回实际值** —— 100 血挨 999 点，实际只扣了 100

治疗是镜像版：

```python
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)   # 守住上界
        return self.hp - before
```

## 提示 2 · 「不能做」的情况提前返回

```python
    def heal(self, amount):
        if amount < 0:
            raise ValueError(f"治疗量不能是负数（收到 {amount}）")
        if not self.alive:
            print(f"     ⚠️ {self.name} 已经倒下了，治不了")
            return 0            # ← 提前返回，后面的都不跑
        ...
```

`attack` 同理：

```python
    def attack(self, target):
        if not self.alive:
            print(f"     ⚠️ {self.name} 已经倒下了，攻击不了")
            return 0
        ...
```

⚠️ 判题会检查「倒下时攻击**不能真的扣到对方的血**」——
所以 `return 0` 必须在扣血**之前**。

复活要注意最低 1 血：

```python
    def revive(self, ratio=0.5):
        if self.alive:
            return False
        self.hp = max(1, int(self.max_hp * ratio))    # ← 至少 1
        self.alive = True
        return True
```

不写 `max(1, ...)` 的话，10 血的角色按 0.01 复活会得到 0 —— 复活完还是死的。

## 提示 3 · 血条

```python
    def hp_percent(self):
        """血量百分比，0~100 的整数。"""
        return int(self.hp / self.max_hp * 100)

    def status(self):
        """返回一行状态文字，带血条。"""
        percent = self.hp_percent()
        filled = percent // 10
        bar = "█" * filled + "░" * (10 - filled)
        state = "存活" if self.alive else "倒下"
        return (f"{self.name} Lv.{self.level}  {bar} "
                f"{self.hp}/{self.max_hp}（{percent}%）  [{state}]")
```

`percent // 10` 把 0~100 变成 0~10 格（Day 3 的整除）。

主流程演示 raise 时记得用 `try` 接住，不然程序会中断：

```python
try:
    hero.take_damage(-100)
except ValueError as e:
    print(f"  ✓ 被拦下了：{e}")
```
