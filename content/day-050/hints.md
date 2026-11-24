## 提示 1 · json 的固定咒语

存：

```python
def save_game(filename, data):
    """把存档写进 json 文件。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
```

**两个参数一个都不能少**：

- `ensure_ascii=False` —— 中文原样保存，不然变成 `\u661f\u91ce`
- `indent=2` —— 分行缩进，人能读

读：

```python
def load_game(filename):
    """读档。文件不存在或格式损坏都返回 None。"""
    try:
        with open(filename, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("  （还没有存档）")
        return None
    except json.JSONDecodeError:
        print("  （存档文件损坏了）")
        return None
```

⚠️ **两种错要分开接**，各给一句不同的提示 —— 用户才知道是「还没存过」
还是「存档坏了」。

## 提示 2 · 道具要累加不要覆盖

```python
def add_item(data, item, count=1):
    """往背包里加道具。已经有的就累加数量。"""
    if item in data["items"]:
        data["items"][item] = data["items"][item] + count
    else:
        data["items"][item] = count
    return data
```

⚠️ 直接写 `data["items"][item] = count` 是**覆盖**，
加两次药水会变成第二次的数量，而不是加起来。

判题专门有一条在验这个：药水加 3 再加 2，应该是 **5**。

队伍那个简单些：

```python
def add_member(data, name, hp):
    """往队伍里加一个成员。"""
    data["team"].append({"name": name, "hp": hp})
    return data
```

## 提示 3 · 主流程的完整流程

```python
print("\n--- 尝试读档 ---")
data = load_game(SAVE)
if data is None:
    print("  开一份新档吧！")
    data = new_save("小樱")
```

这就是所有游戏开机时干的事 —— **有档就读，没档就新建**。

中间加数据、改数值：

```python
add_member(data, "星野樱", 340)
add_item(data, "红药水", 3)
add_item(data, "红药水", 2)     # 累加到 5

data["chapter"] = data["chapter"] + 1
data["gold"] = data["gold"] + 50

save_game(SAVE, data)
```

最后测损坏存档 —— 自己造一个坏文件：

```python
with open(BROKEN, "w", encoding="utf-8") as f:
    f.write("这不是 json{{{")

broken = load_game(BROKEN)
print(f"  读回来的是：{broken}")
```

> ✨ 跑完记得去右边「📁 文件」点开 `存档.json` 看看 ——
> 那就是真实游戏存档的样子。
