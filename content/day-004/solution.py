# Day 4 · 入学登记处

print("=== 派森学院 · 入学登记处 ===")

name = input("请输入你的名字：")
age = int(input("请输入你的年龄："))
lucky = int(input("请输入你的幸运数字："))

birth_year = 2026 - age
student_id = age * 100 + lucky

print("--- 学生证 ---")
print(f"姓名：{name}")
print(f"年龄：{age}")
print(f"出生年份：{birth_year}")
print(f"学号：{student_id}")
print("--- 欢迎入学 ---")
