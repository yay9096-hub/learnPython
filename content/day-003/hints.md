## 提示 1 · 先把公式翻译成代码

数学写法 → Python 写法，几乎是一比一：

```
伤害 = 攻击力 - 防御力
damage = atk - defense
```

等号右边先算，算完的结果装进左边的盒子。

## 提示 2 · 暴击要注意括号

```
暴击 = (攻击力 - 防御力) × 倍率
```

Python 里乘号是 `*`，而且 —— **括号不能省**！

```python
crit_damage = (atk - defense) * crit_rate
```

如果不加括号，Python 会先算 `defense * crit_rate`，答案就完全不一样了。

## 提示 3 · round 套在最外面

```python
crit_damage = round((atk - defense) * crit_rate, 1)
```

`round()` 有两个参数，中间用逗号隔开：

- 第一个：要处理的数
- 第二个：保留几位小数

最后用 f-string 报出来：

```python
print(f"普通攻击：造成 {damage} 点伤害")
```
