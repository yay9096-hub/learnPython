## 提示 1 · 先算再画

文字摘要用第三章的老本事：

```python
total_hp = sum(hp)
avg_atk = round(sum(atk) / len(atk), 1)
best_index = atk.index(max(atk))

print(f"  总血量：{total_hp}")
print(f"  平均攻击：{avg_atk}")
print(f"  最强：{names[best_index]}（{max(atk)}）")
```

`atk.index(max(atk))` —— 先找最大值，再找它在第几个位置，
最后用这个位置去 `names` 里取名字（Day 25 学过的招）。

## 提示 2 · 两格布局

```python
plt.figure(figsize=(9, 4))        # ① 整张图多大

plt.subplot(1, 2, 1)              # ② 左边这格
plt.barh(names, hp, color="#EC6FA9")
plt.title("队伍血量")
plt.xlabel("血量")

plt.subplot(1, 2, 2)              # ③ 右边这格
plt.bar(names, atk, color="#8B5CF6")
plt.title("队伍攻击力")
plt.ylabel("攻击力")

plt.tight_layout()                # ④ 自动调间距
plt.show()
```

记住这个顺序：**figure → subplot → 画 → 标题 → 下一个 subplot → tight_layout → show**。

⚠️ `subplot(1, 2, 1)` 读作「1 行 2 列，我要第 1 格」。

⚠️ 血量那张用 **`barh`**（横着），因为名字长；攻击力那张用 `bar`。

## 提示 3 · 在柱子上标数值

```python
plt.ylim(0, 130)                  # 先把上限拉高，给数字留地方

for i in range(len(names)):
    plt.text(i, atk[i] + 3, str(atk[i]), ha="center")
```

三个参数：

- `i` —— 第几根柱子（横坐标，从 0 开始）
- `atk[i] + 3` —— 比柱子顶端高一点点
- `ha="center"` —— 文字水平居中，正好压在柱子中线上

⚠️ 不写 `plt.ylim(0, 130)` 的话，110 那根柱子上的数字会顶到图外面看不见。

名字挤在一起的话，还可以转个角度：

```python
plt.xticks(rotation=30, ha="right")
```

> 💡 **调图是个反复试的过程** —— 跑一次看看，觉得挤就改尺寸、改角度、改颜色。
> 没有一次成功的，专业的人也是这么调的。
