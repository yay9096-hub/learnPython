## 提示 1 · 五种切法，一个个来

```python
recent = records[-5:]        # 最近 5 次
earliest = records[:3]       # 最早 3 次
```

先写这两个，`print` 出来数一数对不对，再往下写。

⚠️ 「最近 5 次」是 `[-5:]` 不是 `[:-5]`：

- `[-5:]` = 从倒数第 5 个**开始**，到最后 → 最后 5 个 ✅
- `[:-5]` = 从头到倒数第 5 个之前 → 前面那一大堆 ❌

## 提示 2 · 步长和倒序

```python
reversed_records = records[::-1]     # 整个倒过来
every_other = records[::2]           # 每隔一个
```

三个位置分别是 `[开始:结束:步长]`。前两个留空就是「全部」，
所以 `[::2]` 读作「全部，每 2 个取 1 个」。

`[::-1]` 是「全部，倒着走」—— Python 里最有名的一句写法，记住它。

## 提示 3 · 中间那段和计数

```python
middle = records[4:8]
```

想要编号 4、5、6、7 这四个，结束位置要写 **8** ——
**结束不包含**，跟 `range(4, 8)` 是同一个规矩。

数 SSR：

```python
ssr_recent = recent.count("SSR")
```

⚠️ 是在 `recent`（最近 5 次）里数，不是在 `records`（全部）里数。

最后打印：

```python
print(f"最近 5 次：{recent}")
print(f"最早 3 次：{earliest}")
print(f"倒序全部：{reversed_records}")
print(f"每隔一个：{every_other}")
print(f"中间 4 次：{middle}")
print(f"最近 5 次里出了 {ssr_recent} 个 SSR")
```
