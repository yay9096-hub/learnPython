## 提示 1 · 每个函数就一行

```python
def find_dates(text):
    """找出所有 YYYY-MM-DD 格式的日期。"""
    return re.findall(r"\d{4}-\d{2}-\d{2}", text)
```

模式怎么读：**4 个数字、横杠、2 个数字、横杠、2 个数字**。
你怎么描述它，就怎么写 —— 这就是正则的思路。

⚠️ **数字要自己转**：

```python
def find_numbers(text):
    """找出所有整数，返回数字列表。"""
    return [int(n) for n in re.findall(r"\d+", text)]
```

`re.findall` 返回的**全是文字**。判题会检查类型是不是 `int`。

## 提示 2 · 分组：括号圈出想要的部分

```python
def find_day_minutes(text):
    """找出所有「Day N 用了 M 分钟」，返回 [(N, M), ...] 的数字元组。"""
    pairs = re.findall(r"Day (\d+) 用了 (\d+) 分钟", text)
    return [(int(d), int(m)) for d, m in pairs]
```

两个括号 → `findall` 返回**元组的列表**，比如 `[("1", "42"), ("3", "58")]`。

`for d, m in pairs` 是解包（Day 33），再各自 `int()` 转成数字。

邮箱和网址：

```python
def find_emails(text):
    return re.findall(r"[\w.]+@[\w.]+\w", text)


def find_urls(text):
    return re.findall(r"https?://[\w./\-]+", text)
```

- 邮箱结尾那个 `\w` 是防止把后面的句号也吃进去
- 网址里 `s?` 表示「s 可有可无」，所以 `http` 和 `https` 都能匹配

## 提示 3 · 替换和防 None

打码用 `\1` `\2` 引用括号里的内容：

```python
def mask_phones(text):
    """把 11 位手机号的中间四位换成 ****。"""
    return re.sub(r"(\d{3})\d{4}(\d{4})", r"\1****\2", text)
```

读法：**抓 3 位（第 1 组）+ 跳过 4 位 + 抓 4 位（第 2 组）**，
然后拼成「第 1 组 + **** + 第 2 组」。

⚠️ 替换字符串也要加 `r`，不然 `\1` 会被当成转义符。

中文计数：

```python
def count_chinese(text):
    return len(re.findall(r"[\u4e00-\u9fa5]", text))
```

`re.search` 一定要判断 None：

```python
first = re.search(r"\d{4}-\d{2}-\d{2}", LOG)
if first:
    print(f"日志从 {first.group(0)} 开始")
else:
    print("日志里没有日期")
```

**`re.search` 找不到时返回 `None`，直接 `.group()` 会崩** —— 这是今天最容易踩的坑。
