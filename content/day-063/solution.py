# Day 63 · 电子宠物
import json

SAVE = "宠物存档.json"


def clamp(value, low=0, high=100):
    """把值夹在 low..high 之间。"""
    return max(low, min(value, high))


class Pet:
    """一只会饿、会困、会长大的电子宠物。"""

    def __init__(self, name, species="史莱姆"):
        self.name = name
        self.species = species
        self.hunger = 50
        self.energy = 50
        self.mood = 50
        self.age = 0
        self.alive = True

    def feed(self, amount=20):
        """喂食。返回实际减少的饥饿值。"""
        before = self.hunger
        self.hunger = clamp(self.hunger - amount)
        self.mood = clamp(self.mood + 5)
        return before - self.hunger

    def sleep(self, hours=1):
        """睡觉。精力回复，但也会饿、会长大。"""
        self.energy = clamp(self.energy + hours * 20)
        self.hunger = clamp(self.hunger + hours * 10)
        self.age = self.age + hours
        return self.energy

    def play(self, cost=15):
        """玩耍。精力不足就玩不动。"""
        if self.energy < 20:
            print(f"     😴 {self.name} 太累了，玩不动")
            return False
        self.energy = clamp(self.energy - cost)
        self.mood = clamp(self.mood + 15)
        self.hunger = clamp(self.hunger + 10)
        return True

    def tick(self):
        """时间流逝一小时。"""
        self.hunger = clamp(self.hunger + 8)
        self.energy = clamp(self.energy - 5)
        self.age = self.age + 1

        if self.hunger >= 100:
            self.mood = clamp(self.mood - 20)

        if self.mood <= 0 and self.energy <= 0:
            self.alive = False
        return self.alive

    def is_hungry(self):
        """饿了吗。"""
        return self.hunger > 70

    def stage(self):
        """成长阶段。"""
        if self.age < 10:
            return "幼年"
        if self.age < 30:
            return "少年"
        return "成年"

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


def save_pet(filename, pet):
    """把宠物存进 json。"""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(pet.to_dict(), f, ensure_ascii=False, indent=2)


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


# ---------- 主流程 ----------
print("🐣 === 电子宠物 === 🐣")

pet = load_pet(SAVE)
if pet is None:
    pet = Pet("小樱", "樱花史莱姆")
    print(f"  ✨ 领养了一只 {pet.species}，取名 {pet.name}")
else:
    print(f"  ✓ 欢迎回来，{pet.name}")

print("\n--- 初始状态 ---")
print("  " + str(pet))

print("\n--- 喂食 ---")
reduced = pet.feed(30)
print(f"     饥饿减少了 {reduced}")
print("  " + str(pet))

print("\n--- 玩耍 ---")
print(f"     玩成功了吗：{pet.play()}")
print("  " + str(pet))

print("\n--- 睡觉 2 小时 ---")
pet.sleep(2)
print("  " + str(pet))

print("\n--- 累到玩不动 ---")
pet.energy = 10
print(f"     玩成功了吗：{pet.play()}")

print("\n--- 时间流逝 5 小时 ---")
for hour in range(5):
    pet.tick()
    hungry = "（饿了！）" if pet.is_hungry() else ""
    print(f"     第 {hour + 1} 小时：饥饿 {pet.hunger} 精力 {pet.energy} "
          f"心情 {pet.mood} {hungry}")

print(f"\n现在是 {pet.stage()} 期，已经 {pet.age} 小时大了")

action = input("\n想做什么？（喂食/睡觉/玩耍）").strip()
if action == "喂食":
    pet.feed()
elif action == "睡觉":
    pet.sleep()
elif action == "玩耍":
    pet.play()
else:
    print("  它歪着头看着你，没听懂")

print("\n--- 最终状态 ---")
print("  " + str(pet))

save_pet(SAVE, pet)
reloaded = load_pet(SAVE)
print(f"\n💾 已存档。读回来：{reloaded.name}，"
      f"饥饿 {reloaded.hunger}，年龄 {reloaded.age}h ✓")
