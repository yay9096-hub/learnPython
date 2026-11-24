# Day 45 · 防呆登记处
# ⚠️ 每个 except 都要写明错误类型，不许写光秃秃的 except:


# TODO 1: to_int(text, default=0) -> 转整数，失败返回 default
#   接住 ValueError


# TODO 2: to_float(text, default=0.0) -> 转小数，失败返回 default


# TODO 3: safe_divide(a, b) -> 安全除法
#   接住 ZeroDivisionError，返回 0 并提示


# TODO 4: safe_get(data, key, default="未知") -> 从字典安全取值
#   接住 KeyError


# TODO 5: safe_index(lst, i, default=None) -> 从列表安全取值
#   接住 IndexError


# TODO 6: register() -> 问名字、年龄、身高，返回一个字典
#   年龄用 to_int，身高用 to_float


# ---------- 主流程 ----------
# TODO 7: 调用 register() 并打印结果
# TODO 8: 用 safe_divide 演示除以 0
# TODO 9: 用 safe_get 取一个不存在的键
# TODO 10: 用 safe_index 取一个越界的编号
