## 提示 1 · 输入校验的固定套路

「输错了要能重问」的标准写法：

```python
road = ""                              # 先给个肯定不合法的值
while road not in ["1", "2"]:
    print("  1) 走进樱花森林")
    print("  2) 走进幽暗洞穴")
    road = input("你的选择（1/2）：").strip()
    if road not in ["1", "2"]:
        print("❓ 听不懂，请输入 1 或 2\n")
```

念一遍：「**只要**选择还不在合法列表里，**就一直**重问」。

⚠️ 第一行 `road = ""` 不能省 —— 循环条件要用到它，得先让它存在（Day 14 学过）。

## 提示 2 · 两个选择点是嵌套的

第二个选择点在第一个的**分支里面**：

```python
if road == "1":
    print("\n🌸 你走进森林，一只影狼挡住了去路。")
    choice = ""
    while choice not in ["1", "2"]:
        choice = input("  1) 迎战  2) 绕开\n你的选择：").strip()

    if choice == "1":
        # 这里打一场（Day 20 的战斗循环）
        ending = "勇者结局"
    else:
        ending = "平凡结局"
else:
    # 洞穴那条路，结构一模一样
    ...
```

💡 用一个 `ending` 变量记住走到了哪种结局，最后统一打印 ——
比在每个分支里都写一遍结局文字清爽得多。

## 提示 3 · 战斗直接抄 Day 20

```python
wolf_hp = 100
while wolf_hp > 0 and hp > 0:
    turns += 1
    wolf_hp -= atk
    print(f"  第 {turns} 回合：你砍出 {atk} 点伤害，影狼剩 {wolf_hp} HP")
    if wolf_hp <= 0:
        break
    bite = random.randint(10, 25)
    hp -= bite
    print(f"  第 {turns} 回合：影狼咬了你 {bite} 点，你剩 {hp} HP")

if hp > 0:
    ending = "勇者结局"
else:
    ending = "陨落结局"
```

最后的结局区：

```python
if ending == "勇者结局":
    print(f"⚔️  【勇者结局】{name} 击败了影狼！")
elif ending == "宝藏结局":
    print(f"💎 【宝藏结局】{name} 富可敌国！")
elif ending == "陨落结局":
    print(f"💀 【陨落结局】{name} 倒下了……")
else:
    print(f"🌾 【平凡结局】{name} 平安回家。")

print(f"你走了 {steps} 步，打了 {turns} 个回合，剩余 HP {hp}")
```
