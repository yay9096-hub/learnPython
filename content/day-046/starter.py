# Day 46 · 严格的登记处
# ⚠️ 前四个函数只管 raise，一个 try 都不许写
ELEMENTS = ["火", "水", "风", "雷"]


# TODO 1: validate_name(name)
#   不是字符串 -> TypeError
#   strip 后长度 <2 或 >8 -> ValueError（信息里带上实际情况）
#   合法 -> 返回 strip 后的名字


# TODO 2: validate_age(age)
#   不是 int -> TypeError
#   不在 0~120 -> ValueError
#   合法 -> 返回 age


# TODO 3: validate_element(el)
#   不在 ELEMENTS 里 -> ValueError（信息里要列出可选值）
#   合法 -> 返回 el


# TODO 4: create_role(name, age, element)
#   调用上面三个校验，全过才返回字典


# TODO 5: try_register(name, age, element)
#   这里才用 try
#   成功 -> 返回 (True, 角色字典)
#   失败 -> 返回 (False, 错误信息字符串)


# ---------- 主流程 ----------
# TODO 6: 用合法数据调一次，打印角色
# TODO 7: 用三种非法数据各调一次，打印错误信息
# TODO 8: 问玩家输入一次（名字/年龄/属性），用 try_register 处理
