"""判题器。

tests.py 里写：

    CASES = [
        {
            "stdin": ["小樱", "16"],
            "checks": [
                {"id": "name", "desc": "学生证上有名字",
                 "type": "stdout_contains", "value": "小樱",
                 "fail": "输出里没看到你输入的名字哦"},
            ],
        },
    ]

只有一组的话也可以直接写 CHECKS = [...]。

判题原则（写在这里提醒自己）：
  * stdout 比对一律**宽松**：忽略首尾空白、把连续空格压成一个。
    绝不能因为多打一个空格判她错。
  * 每个 check 必须带 desc（任务清单上显示）和 fail（没过时的具体提示）。
"""
import ast
import io
import json
import random as _random
import re
import sys

import runtime

# 判题时可以在 case 里写 setup，把 random 换成固定值，好让猜数字这类
# 带随机的项目也能被稳定判题。判完必须还原，否则她接下来正常「运行」时
# random 就一直返回同一个数了。
_RANDOM_FUNCS = (
    "randint", "randrange", "random", "choice", "choices",
    "shuffle", "sample", "uniform",
)


def _norm(s: str) -> str:
    s = s.replace("\r\n", "\n").strip()
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n{2,}", "\n", s)


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------ 检查器

def _c_stdout_contains(ctx, c):
    needles = c.get("value") if isinstance(c.get("value"), list) else [c.get("value")]
    out = _norm(ctx["stdout"])
    if not c.get("case_sensitive"):
        out = out.lower()
    for n in needles:
        n = _norm(str(n))
        if not c.get("case_sensitive"):
            n = n.lower()
        if n not in out:
            return False
    return True


def _c_stdout_not_contains(ctx, c):
    return not _c_stdout_contains(ctx, c)


def _c_stdout_regex(ctx, c):
    return re.search(c["pattern"], ctx["stdout"], re.M) is not None


def _c_stdout_lines_min(ctx, c):
    lines = [l for l in ctx["stdout"].splitlines() if l.strip()]
    return len(lines) >= int(c["value"])


def _c_stdout_has_number(ctx, c):
    """输出里出现某个数字，容忍小数位差异。"""
    target = float(c["value"])
    tol = float(c.get("tol", 0.01))
    for m in re.finditer(r"-?\d+(?:\.\d+)?", ctx["stdout"]):
        if abs(float(m.group()) - target) <= tol:
            return True
    return False


def _c_var_equals(ctx, c):
    if c["name"] not in ctx["ns"]:
        return False
    got, want = ctx["ns"][c["name"]], c["value"]
    gn, wn = _num(got), _num(want)
    if gn is not None and wn is not None:
        return abs(gn - wn) <= float(c.get("tol", 1e-6))
    return _norm(str(got)) == _norm(str(want))


def _c_var_exists(ctx, c):
    return c["name"] in ctx["ns"]


def _c_value_present(ctx, c):
    """算出了某个值就算过 —— **不管她把它存进哪个变量**。

    真事：有人把 birth_year 写成 birthday、student_id 写成 number，
    值全对、输出全对，却被判错。为变量名判一个初学者错，太苛刻了，
    而且当天的知识点是 input 和类型转换，本来就不是命名。

    只有当天的讲解里**明确写出了变量名**（比如 Day 2 的 name/level/hp/mp），
    才用 var_equals 去卡名字。
    """
    want = c["value"]
    tol = float(c.get("tol", 1e-6))
    wn = _num(want)
    for k, v in ctx["ns"].items():
        if k.startswith("__") or isinstance(v, bool):
            continue
        if wn is not None:
            vn = _num(v)
            if vn is not None and abs(vn - wn) <= tol:
                return True
        if isinstance(v, str) and _norm(v) == _norm(str(want)):
            return True
    return False


def _c_list_equals(ctx, c):
    """列表内容对就行，**变量名随意**。

    给了 name 就只看那一个变量；没给就在所有变量里找一个对得上的。
    ordered=False 时忽略顺序（比如「队伍成员有这几个」不关心排列）。
    """
    want = list(c["value"])
    ordered = c.get("ordered", True)
    name = c.get("name")
    if name:
        cands = [ctx["ns"][name]] if name in ctx["ns"] else []
    else:
        cands = [v for k, v in ctx["ns"].items() if not k.startswith("__")]

    for v in cands:
        if not isinstance(v, (list, tuple, set)):
            continue
        got = list(v)
        if ordered and not isinstance(v, set):
            if [_norm(str(x)) for x in got] == [_norm(str(x)) for x in want]:
                return True
        else:
            if sorted(_norm(str(x)) for x in got) == sorted(_norm(str(x)) for x in want):
                return True
    return False


def _c_dict_has(ctx, c):
    """字典里有这些键值对（value），或者至少有这些键（keys）。变量名随意。"""
    want = c.get("value") or {}
    keys = c.get("keys") or []
    name = c.get("name")
    if name:
        cands = [ctx["ns"][name]] if name in ctx["ns"] else []
    else:
        cands = [v for k, v in ctx["ns"].items() if not k.startswith("__")]

    for v in cands:
        if not isinstance(v, dict):
            continue
        if keys and not all(k in v for k in keys):
            continue
        if all(k in v and _norm(str(v[k])) == _norm(str(val)) for k, val in want.items()):
            if keys or want:
                return True
    return False


def _c_var_type(ctx, c):
    v = ctx["ns"].get(c["name"])
    return v is not None and type(v).__name__ == c["value"]


def _c_func_returns(ctx, c):
    fn = ctx["ns"].get(c["func"])
    if not callable(fn):
        return False
    try:
        got = fn(*c.get("args", []), **c.get("kwargs", {}))
    except Exception:
        return False
    want = c["expect"]
    gn, wn = _num(got), _num(want)
    if gn is not None and wn is not None:
        return abs(gn - wn) <= float(c.get("tol", 1e-6))
    return got == want


_AST_ALIASES = {
    "for": ast.For, "while": ast.While, "if": ast.If, "def": ast.FunctionDef,
    "class": ast.ClassDef, "import": (ast.Import, ast.ImportFrom),
    "fstring": ast.JoinedStr, "assign": ast.Assign, "try": ast.Try,
}


def _c_ast_has(ctx, c):
    node_type = _AST_ALIASES.get(str(c["node"]).lower())
    if node_type is None:
        node_type = getattr(ast, c["node"], None)
    if node_type is None:
        return False
    n = sum(1 for x in ast.walk(ctx["tree"]) if isinstance(x, node_type))
    return n >= int(c.get("min", 1))


def _c_ast_calls(ctx, c):
    """代码里调用过某个函数，比如 print / input / turtle.forward。"""
    want = c["name"]
    count = 0
    for node in ast.walk(ctx["tree"]):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        name = None
        if isinstance(f, ast.Name):
            name = f.id
        elif isinstance(f, ast.Attribute):
            name = f.attr
            if isinstance(f.value, ast.Name):
                full = f"{f.value.id}.{f.attr}"
                if full == want:
                    count += 1
                    continue
        if name == want:
            count += 1
    return count >= int(c.get("min", 1))


def _c_ast_imports(ctx, c):
    want = c["name"]
    for node in ast.walk(ctx["tree"]):
        if isinstance(node, ast.Import):
            if any(a.name.split(".")[0] == want for a in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if (node.module or "").split(".")[0] == want:
                return True
    return False


def _c_plot_has(ctx, c):
    """图表里有没有某些东西。

    支持的字段：figures / axes / lines / bars / wedges / legends（数量下限），
    以及 title / xlabel / ylabel（文字包含）。
    """
    p = ctx.get("plot") or {}
    for key in ("figures", "axes", "lines", "bars", "wedges", "legends"):
        if key in c and p.get(key, 0) < int(c[key]):
            return False
    if c.get("title") is not None:
        joined = " ".join(p.get("titles", []))
        if _norm(str(c["title"])) not in _norm(joined):
            return False
    if c.get("has_title") and not p.get("titles"):
        return False
    if c.get("has_xlabel") and not p.get("xlabels"):
        return False
    if c.get("has_ylabel") and not p.get("ylabels"):
        return False
    return True


def _c_turtle_min_ops(ctx, c):
    cmds = ctx["turtle"]["cmds"]
    kinds = c.get("op")
    if kinds:
        cmds = [x for x in cmds if x["op"] == kinds]
    return len(cmds) >= int(c.get("min", 1))


def _c_turtle_colors_min(ctx, c):
    colors = {x.get("color") for x in ctx["turtle"]["cmds"] if x.get("color")}
    return len(colors) >= int(c.get("min", 2))


def _c_class_defined(ctx, c):
    """定义了某个类。可选 methods 指定必须有哪些方法。"""
    name = c["name"]
    cls = ctx["ns"].get(name)
    if not isinstance(cls, type):
        return False
    for m in c.get("methods", []):
        if not callable(getattr(cls, m, None)):
            return False
    if c.get("base"):
        base = ctx["ns"].get(c["base"])
        if not isinstance(base, type) or not issubclass(cls, base):
            return False
    return True


def _c_instance_attr(ctx, c):
    """造一个实例，检查属性对不对。

    args / kwargs 是构造参数，attrs 是期望的属性值。
    """
    cls = ctx["ns"].get(c["name"])
    if not isinstance(cls, type):
        return False
    try:
        obj = cls(*c.get("args", []), **c.get("kwargs", {}))
    except Exception:
        return False
    for key, want in (c.get("attrs") or {}).items():
        if not hasattr(obj, key):
            return False
        got = getattr(obj, key)
        gn, wn = _num(got), _num(want)
        if gn is not None and wn is not None:
            if abs(gn - wn) > float(c.get("tol", 1e-6)):
                return False
        elif _norm(str(got)) != _norm(str(want)):
            return False
    return True


def _c_method_returns(ctx, c):
    """造一个实例，调一个方法，断言返回值。"""
    cls = ctx["ns"].get(c["name"])
    if not isinstance(cls, type):
        return False
    try:
        obj = cls(*c.get("init_args", []), **c.get("init_kwargs", {}))
        method = getattr(obj, c["method"])
        got = method(*c.get("args", []), **c.get("kwargs", {}))
    except Exception:
        return False
    if "expect" not in c:
        return True
    want = c["expect"]
    gn, wn = _num(got), _num(want)
    if gn is not None and wn is not None:
        return abs(gn - wn) <= float(c.get("tol", 1e-6))
    return _norm(str(got)) == _norm(str(want))


def _c_method_changes(ctx, c):
    """造一个实例，调方法，断言某个属性变成了期望值。

    面向对象最常见的判题形状：调用 -> 状态改变。
    """
    cls = ctx["ns"].get(c["name"])
    if not isinstance(cls, type):
        return False
    try:
        obj = cls(*c.get("init_args", []), **c.get("init_kwargs", {}))
        for call in c.get("calls", []):
            method = getattr(obj, call["method"])
            method(*call.get("args", []), **call.get("kwargs", {}))
    except Exception:
        return False
    for key, want in (c.get("attrs") or {}).items():
        if not hasattr(obj, key):
            return False
        got = getattr(obj, key)
        gn, wn = _num(got), _num(want)
        if gn is not None and wn is not None:
            if abs(gn - wn) > float(c.get("tol", 1e-6)):
                return False
        elif _norm(str(got)) != _norm(str(want)):
            return False
    return True


def _c_custom(ctx, c):
    fn = ctx["tests_ns"].get(c["fn"])
    if not callable(fn):
        return False
    try:
        return bool(fn(ctx))
    except Exception:
        return False


CHECKERS = {
    "stdout_contains": _c_stdout_contains,
    "stdout_not_contains": _c_stdout_not_contains,
    "stdout_regex": _c_stdout_regex,
    "stdout_lines_min": _c_stdout_lines_min,
    "stdout_has_number": _c_stdout_has_number,
    "var_equals": _c_var_equals,
    "var_exists": _c_var_exists,
    "value_present": _c_value_present,
    "list_equals": _c_list_equals,
    "dict_has": _c_dict_has,
    "var_type": _c_var_type,
    "func_returns": _c_func_returns,
    "ast_has": _c_ast_has,
    "ast_calls": _c_ast_calls,
    "ast_imports": _c_ast_imports,
    "plot_has": _c_plot_has,
    "turtle_min_ops": _c_turtle_min_ops,
    "turtle_colors_min": _c_turtle_colors_min,
    "class_defined": _c_class_defined,
    "instance_attr": _c_instance_attr,
    "method_returns": _c_method_returns,
    "method_changes": _c_method_changes,
    "custom": _c_custom,
}


# ------------------------------------------------- 残留的「清空」语句检测

_EMPTY_CALLS = {"list", "dict", "set", "tuple", "str"}


def _is_empty_literal(node):
    """判断一个表达式是不是「空值」：[] {} "" 0 () set() list() ..."""
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return not node.elts
    if isinstance(node, ast.Dict):
        return not node.keys
    if isinstance(node, ast.Constant):
        return node.value in ("", 0) and not isinstance(node.value, bool)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return node.func.id in _EMPTY_CALLS and not node.args and not node.keywords
    return False


def _leftover_resets(tree):
    """找出「算完之后又被清空、而且再也没用过」的变量。

    真事：Day 28 有人把代码写在 starter 的 TODO **上面**，
    底下 starter 原本那行 `unique = []` 还留着 ——
    输出全对（因为 print 在前面），但跑到最后 unique 又变回空列表，
    判题看最终状态，于是「去重结果正确」被判红。

    她没做错任何事，是残留的模板代码在最后一刻把结果抹掉了。
    这种错自己极难发现（输出看起来完全正常），所以判题器要主动指出来。
    """
    assigns, loads = {}, {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            line = getattr(node, "lineno", 0)
            if isinstance(node.ctx, ast.Store):
                assigns.setdefault(node.id, []).append(line)
            elif isinstance(node.ctx, ast.Load):
                loads[node.id] = max(loads.get(node.id, 0), line)

    notes = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign) or not _is_empty_literal(node.value):
            continue
        for t in node.targets:
            if not isinstance(t, ast.Name):
                continue
            line = getattr(node, "lineno", 0)
            earlier = [l for l in assigns.get(t.id, []) if l < line]
            # 之前赋过值、之后再也没被读过 —— 这行纯粹是把成果抹掉
            if earlier and line > loads.get(t.id, 0):
                notes.append({"name": t.id, "line": line})
    return notes


# ------------------------------------------------------------------ 主流程

def judge(code: str, tests_src: str) -> str:
    tests_ns: dict = {}
    try:
        exec(compile(tests_src or "", "tests.py", "exec"), tests_ns)
    except Exception as e:                                   # noqa: BLE001
        return json.dumps({"error": f"这一天的判题脚本坏了：{e}"}, ensure_ascii=False)

    cases = tests_ns.get("CASES")
    if not cases:
        cases = [{"stdin": tests_ns.get("STDIN", []), "checks": tests_ns.get("CHECKS", [])}]

    try:
        tree = ast.parse(code, "<你写的代码>")
    except SyntaxError as e:
        return json.dumps({
            "error": "代码还有语法错误，先让它能跑起来吧～",
            "syntax": runtime.format_error(e),
        }, ensure_ascii=False)

    results, run_error = [], None
    saved_random = {k: getattr(_random, k) for k in _RANDOM_FUNCS}
    try:
        results, run_error = _run_cases(cases, code, tree, tests_ns)
    finally:
        # setup 里动过的 random 一律还原
        for k, v in saved_random.items():
            setattr(_random, k, v)

    all_passed = bool(results) and all(r["passed"] for r in results)
    return json.dumps({
        "results": results,
        "all_passed": all_passed,
        "run_error": run_error,
        # 只在有任务没过时才提，全过了就别添乱
        "notes": [] if all_passed else _leftover_resets(tree),
    }, ensure_ascii=False, default=str)


def _run_cases(cases, code, tree, tests_ns):
    results, run_error = [], None
    for case in cases:
        ns0 = {"__name__": "__main__"}
        setup = case.get("setup")
        if setup:
            # setup 在学生代码之前跑，用来固定随机数、预置数据等
            exec(compile(setup, "<setup>", "exec"), ns0)

        buf = io.StringIO()
        real_stdout = sys.stdout
        sys.stdout = buf
        try:
            ns, err = runtime.run_user_code(
                code, preset_stdin=case.get("stdin", []), namespace=ns0)
        finally:
            sys.stdout = real_stdout
        stdout = buf.getvalue()
        if err and run_error is None:
            run_error = err

        ctx = {
            "stdout": stdout, "ns": ns, "tree": tree, "code": code,
            "turtle": runtime.turtle_dump(), "plot": runtime.plot_dump(),
            "tests_ns": tests_ns,
            "error": err, "stdin": case.get("stdin", []),
        }
        for c in case.get("checks", []):
            checker = CHECKERS.get(c.get("type"))
            passed = False
            if checker is not None:
                try:
                    passed = bool(checker(ctx, c))
                except Exception:                            # noqa: BLE001
                    passed = False
            results.append({
                "id": c.get("id") or c.get("desc", ""),
                "desc": c.get("desc", ""),
                "passed": passed,
                "fail": c.get("fail", ""),
                "hint_day": c.get("hint_day"),
            })

    return results, run_error
