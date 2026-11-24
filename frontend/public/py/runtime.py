"""在 Pyodide 里执行学生代码的外壳：接管 input()、格式化报错、收集 turtle 画面。"""
import builtins
import json
import sys
import types
import traceback

USER_FILE = "<你写的代码>"

_turtle_mod = None
_stdin_queue = []
_js_input = None          # 由 worker 注入的同步 JS 函数（SharedArrayBuffer 实现）


def install_turtle(source):
    """把 turtle_shim 注册成名叫 turtle 的模块，让 import turtle 正常工作。"""
    global _turtle_mod
    mod = types.ModuleType("turtle")
    mod.__dict__["__name__"] = "turtle"
    exec(compile(source, "turtle_shim.py", "exec"), mod.__dict__)
    sys.modules["turtle"] = mod
    _turtle_mod = mod


def turtle_dump():
    if _turtle_mod is None:
        return {"bg": None, "cmds": []}
    return _turtle_mod._dump()


def plot_dump():
    """把当前 matplotlib 图表的结构摘出来，给判题用。

    只在 matplotlib 已经被载入时有意义；没画图就返回空壳。
    读完顺手把图关掉，免得下一次判题看到上一次的残留。
    """
    empty = {"figures": 0, "axes": 0, "lines": 0, "bars": 0,
             "wedges": 0, "titles": [], "xlabels": [], "ylabels": [],
             "legends": 0, "texts": []}
    if "matplotlib" not in sys.modules:
        return empty
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return empty

    nums = plt.get_fignums()
    if not nums:
        return empty

    info = dict(empty)
    info["figures"] = len(nums)
    for num in nums:
        fig = plt.figure(num)
        for ax in fig.get_axes():
            info["axes"] += 1
            info["lines"] += len(ax.lines)
            info["bars"] += len(ax.patches)
            info["wedges"] += sum(
                1 for p in ax.patches if type(p).__name__ == "Wedge")
            if ax.get_title():
                info["titles"].append(ax.get_title())
            if ax.get_xlabel():
                info["xlabels"].append(ax.get_xlabel())
            if ax.get_ylabel():
                info["ylabels"].append(ax.get_ylabel())
            if ax.get_legend() is not None:
                info["legends"] += 1
            for t in ax.texts:
                info["texts"].append(t.get_text())
    return info


def turtle_dump_json():
    return json.dumps(turtle_dump(), ensure_ascii=False, default=str)


def turtle_reset():
    if _turtle_mod is not None:
        _turtle_mod._reset_all()
        _turtle_mod._t.__init__()


def set_js_input(fn):
    global _js_input
    _js_input = fn


def _echo(prompt, value):
    """把「提示语 + 她输入的内容」写进 stdout，让终端里留下完整对话记录。"""
    sys.stdout.write(str(prompt) + str(value) + "\n")
    sys.stdout.flush()


def _make_input(preset):
    """preset 为 None 时走交互模式；否则从预设队列里取，取完就报一个看得懂的错。"""
    if preset is None:
        def _input(prompt=""):
            if _js_input is None:
                raise RuntimeError("这个环境暂时不支持交互输入")
            sys.stdout.flush()                 # 先把之前 print 的内容刷出去
            value = _js_input(str(prompt))
            _echo(prompt, value)
            return value
        return _input

    queue = list(preset)

    def _input(prompt=""):
        if not queue:
            sys.stdout.write(str(prompt))
            sys.stdout.flush()
            raise EOFError("程序还想再要一次输入，但已经没有可用的输入了")
        value = queue.pop(0)
        _echo(prompt, value)
        return value
    return _input


def format_error(exc) -> dict:
    """把 Traceback 拆成前端能用的结构：类型、原信息、出错行号。"""
    tb = exc.__traceback__
    line = None
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == USER_FILE:
            line = tb.tb_lineno
        tb = tb.tb_next
    if line is None and isinstance(exc, SyntaxError):
        line = exc.lineno
    frames = traceback.format_exception(type(exc), exc, exc.__traceback__)
    text = "".join(f for f in frames if "/lib/python" not in f and "runtime.py" not in f)
    return {
        "type": type(exc).__name__,
        "message": str(exc),
        "line": line,
        "traceback": text.strip(),
    }


def run_user_code(code, preset_stdin=None, namespace=None):
    """执行学生代码。返回 (namespace, error_dict|None)。stdout 由 pyodide 直接转发。"""
    turtle_reset()
    ns = namespace if namespace is not None else {"__name__": "__main__"}
    original_input = builtins.input
    builtins.input = _make_input(preset_stdin)
    try:
        exec(compile(code, USER_FILE, "exec"), ns)
        return ns, None
    except SystemExit:
        return ns, None
    except BaseException as e:                       # noqa: BLE001 - 学生代码什么都可能抛
        return ns, format_error(e)
    finally:
        builtins.input = original_input
        sys.stdout.flush()
