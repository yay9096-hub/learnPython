/**
 * 中文报错翻译器 —— 这是这个网站最重要的一个文件。
 *
 * 零基础学习者看不懂英文 Traceback，一条看不懂的报错就足以让人放弃。
 * 每条规则给出：她做了什么 → 为什么不行 → 怎么改，全部用她能懂的话。
 *
 * 加新规则时的要求：
 *   1. 绝不说"你错了"，只说"这里再看看"
 *   2. 一定要给「改之前 / 改之后」的具体代码
 *   3. 能指到知识点就带上 concept，让她一键跳回去复习
 */

const R = (type, pattern, build) => ({ type, pattern, build })

/** 从报错信息里挖出变量名、类型名之类的关键信息 */
const g = (m, i, fallback = "") => (m && m[i] !== undefined ? m[i] : fallback)

const Q = String.fromCharCode(39) // 单引号，避免在示例代码里写出不配对的引号

/** Python 的类型名对她来说是天书，全部换成中文 */
const TYPE_CN = {
  str: "文字",
  int: "整数",
  float: "小数",
  bool: "对错值",
  list: "列表",
  tuple: "元组",
  dict: "字典",
  set: "集合",
  NoneType: "空值",
  function: "函数",
}
const cn = (t) => TYPE_CN[t] || t

export const RULES = [
  // ---------------------------------------------------------------- 语法
  R("SyntaxError", /unterminated string literal|EOL while scanning string literal/, () => ({
    title: "引号没有关上",
    lines: [
      "字符串必须**两边都有引号**把它包起来，你这里只写了开头那个。",
      "Python 一路找到行尾也没找到另一半，就懵了。",
    ],
    code: {
      bad: "print(" + Q + "你好)",
      good: "print(" + Q + "你好" + Q + ")",
    },
    concept: { day: 1, name: "字符串和引号" },
  })),

  R("SyntaxError", /was never closed/, () => ({
    title: "括号没有关上",
    lines: ["有一个左括号一直没等到它的右括号。检查一下这一行，还有它上面那一行。"],
    code: { bad: 'print("你好"', good: 'print("你好")' },
    concept: { day: 1, name: "print 的写法" },
  })),

  R("SyntaxError", /expected .:./, () => ({
    title: "这一行结尾少了个冒号",
    lines: [
      "`if`、`for`、`while`、`def` 这些行的**末尾必须有冒号 `:`**，",
      "它是「下面要开始一段了」的标志。",
    ],
    code: {
      bad: 'if score > 60\n    print("过了")',
      good: 'if score > 60:\n    print("过了")',
    },
  })),

  R("SyntaxError", /Perhaps you forgot a comma/, () => ({
    title: "这里可能少了个逗号",
    lines: ["两个东西挨在一起、中间什么都没有，Python 猜你是想用逗号把它们分开。"],
    code: { bad: 'print("等级" 5)', good: 'print("等级", 5)' },
  })),

  R("SyntaxError", /cannot assign to (literal|function call|expression)/, () => ({
    title: "等号左边只能放变量名",
    lines: [
      "`=` 的意思是「把右边的值装进左边的盒子」，所以**左边必须是一个盒子的名字**。",
      "数字、文字、函数调用都不是盒子，装不进去。",
    ],
    code: { bad: "5 = level", good: "level = 5" },
    concept: { day: 2, name: "变量与赋值" },
  })),

  R("SyntaxError", /invalid character/, () => ({
    title: "用到了中文标点",
    lines: [
      "代码里的括号、引号、逗号、冒号**必须是英文半角**的。",
      "中文输入法打出来的那几个长得很像，但 Python 不认识。",
      "👉 按 `Shift` 切回英文输入法再打一遍。",
    ],
    code: { bad: 'print（"你好"）', good: 'print("你好")' },
  })),

  R("SyntaxError", /.*/, () => ({
    title: "这一行的写法 Python 看不懂",
    lines: [
      "常见原因，按可能性从高到低：",
      "① 用了**中文标点**（括号、引号、逗号）",
      "② 括号或引号少了一半",
      "③ 上一行末尾少了冒号 `:`",
      "④ 把 `=`（赋值）和 `==`（比较）搞混了",
      "💡 如果报错指的那一行看着没问题，就去看**它上面那一行**。",
    ],
  })),

  // ---------------------------------------------------------------- 缩进
  R("IndentationError", /unexpected indent/, () => ({
    title: "这一行前面多了空格",
    lines: [
      "Python 用**行首的空格**表示层级关系，所以不能随便空。",
      "这一行前面不该有空格，或者比上一行多空了。",
    ],
    code: {
      bad: 'print("第一行")\n    print("第二行")',
      good: 'print("第一行")\nprint("第二行")',
    },
  })),

  // Python 报这条错时，行号指的是「发现问题的地方」—— 往往是文件最后一行，
  // 真正缺内容的冒号在前面好几十行。消息里带着 "on line 22"，用那个才对。
  // 真事：Day 31 有人写了 `for m in strong:` 就去写别的，下面全是 TODO 注释，
  // 结果红框标在第 39 行一行注释上，她盯着那行注释完全想不通。
  R("IndentationError", /expected an indented block(?: after (.+?) on line (\d+))?/, (m) => {
    const where = g(m, 2) ? Number(g(m, 2)) : null
    return {
      title: where ? `第 ${where} 行的冒号下面是空的` : "冒号下面那行要往右缩进",
      lines: [
        "写了 `:` 就等于说「接下来这一段属于我」，那一段**必须往右缩进 4 个空格**。",
        ...(where
          ? [
              `第 ${where} 行以冒号结尾，可它下面**一行真正的代码都没有** —— ` +
                "**注释和空行不算数**，Python 会一路往下找，找到最后才报错。",
              "要么把下面那段写完，要么这一行还没想好就先删掉。",
            ]
          : []),
      ],
      code: {
        bad: 'for m in strong:\n# TODO: 待会儿再写',
        good: 'for m in strong:\n    print(m["name"])',
      },
      line: where,
    }
  }),

  R("IndentationError", /unindent does not match/, () => ({
    title: "缩进对不齐",
    lines: ["同一层的代码，前面的空格数必须**完全一样**。建议统一用 4 个空格。"],
  })),

  R("TabError", /.*/, () => ({
    title: "Tab 和空格混着用了",
    lines: [
      "有的行用 Tab 缩进、有的行用空格，看起来一样但 Python 认为不一样。",
      "统一用空格就好（编辑器已经帮你把 Tab 键变成 4 个空格了）。",
    ],
  })),

  // ---------------------------------------------------------------- 名字
  R("NameError", /name ['"]([^'"]+)['"] is not defined/, (m) => {
    const n = g(m, 1, "它")
    return {
      title: "Python 不认识 `" + n + "` 这个名字",
      lines: [
        "你用了 `" + n + "`，但之前从来没告诉过 Python 它是什么。",
        "三个可能：",
        "① 忘了先造这个变量：`" + n + " = ...`",
        "② 名字**拼错了或大小写不对**（`Name` 和 `name` 是两个不同的东西）",
        "③ 本来想写一段文字却忘了加引号 —— `print(" + n + ")` 应该写成 `print(\"" + n + "\")`",
      ],
      code: { bad: "print(" + n + ")", good: n + ' = "..."\nprint(' + n + ")" },
      concept: { day: 2, name: "变量与赋值" },
    }
  }),

  R("UnboundLocalError", /local variable ['"]([^'"]+)['"]/, (m) => ({
    title: "`" + g(m, 1, "它") + "` 在函数里被用得太早了",
    lines: ["在函数内部，这个变量要先赋值、再使用。"],
  })),

  // ---------------------------------------------------------------- 类型
  R("TypeError", /can only concatenate str \(not "(.+?)"\) to str/, (m) => ({
    title: "文字和数字不能直接用 + 粘在一起",
    lines: [
      "`+` 两边都是文字时是「拼接」，两边都是数字时是「加法」。",
      "现在一边是文字、一边是" + cn(g(m, 1)) + "，Python 不知道你想干哪个。",
      "两种改法，推荐第二种：",
    ],
    code: {
      bad: 'print("我今年" + 16 + "岁")',
      good: 'print("我今年" + str(16) + "岁")\n\n# 更好用的写法（第 2 天会学到）：\nprint(f"我今年{16}岁")',
    },
    concept: { day: 2, name: "f-string 格式化" },
  })),

  R("TypeError", /unsupported operand type\(s\) for (.+?): ['"]([^'"]+)['"] and ['"]([^'"]+)['"]/, (m) => ({
    title: cn(g(m, 2)) + " 和 " + cn(g(m, 3)) + " 之间不能做 `" + g(m, 1) + "` 运算",
    lines: [
      "最常见的情况：`input()` 拿回来的永远是**文字**，哪怕你输入的是 18。",
      "要把它当数字用，得先转换。",
    ],
    code: {
      bad: 'age = input("年龄：")\nprint(age + 1)',
      good: 'age = int(input("年龄："))\nprint(age + 1)',
    },
    concept: { day: 4, name: "类型转换与 input" },
  })),

  R("TypeError", /['"]([^'"]+)['"] object is not callable/, (m) => ({
    title: "在一个不是函数的东西后面加了括号",
    lines: [
      "`" + g(m, 1) + "`（" + cn(g(m, 1)) + "）不是函数，后面不能跟 `()`。",
      "常见原因：把变量名起成了 `print`、`str`、`int` 这种 Python 自带的名字，",
      "把原来的功能覆盖掉了。换个名字就好。",
    ],
    code: {
      bad: 'str = "小樱"\nprint(str(16))',
      good: 'name = "小樱"\nprint(str(16))',
    },
  })),

  R("TypeError", /takes .+ but .+ given/, () => ({
    title: "给函数的参数个数不对",
    lines: ["括号里塞的东西，数量和这个函数要求的对不上。数一数逗号分开了几个。"],
  })),

  R("TypeError", /['"]([^'"]+)['"] object is not subscriptable/, (m) => ({
    title: cn(g(m, 1)) + " 不能用方括号取值",
    lines: ["只有字符串、列表这类「一串东西」才能写 `x[0]`。单个数字不行。"],
  })),

  R("TypeError", /string indices must be integers/, () => ({
    title: "方括号里要放数字",
    lines: ["取字符串里的某个字要写 `name[0]`（第 1 个字），方括号里放的是位置编号，不是文字。"],
  })),

  R("TypeError", /must be str|argument of type|not .+ instance/, () => ({
    title: "给的东西类型不对",
    lines: ["这个位置需要另一种类型。用 `str()` / `int()` / `float()` 转换一下试试。"],
    concept: { day: 4, name: "类型转换" },
  })),

  R("TypeError", /.*/, () => ({
    title: "类型对不上",
    lines: ["两个不同种类的东西被放在一起运算了。检查一下各自到底是文字还是数字。"],
    concept: { day: 4, name: "类型转换" },
  })),

  // ---------------------------------------------------------------- 值
  R("ValueError", /invalid literal for int\(\) with base 10: ['"](.*?)['"]$/, (m) => {
    const raw = g(m, 1)
    return {
      title: "这段文字变不成整数",
      lines: [
        "`int()` 只能转换「看起来就是整数」的文字，它拿到的是：`" + raw + "`",
        raw.includes(".")
          ? "你给的是小数。先 `float()` 转成小数，再 `int()` 抹掉小数点。"
          : "常见原因：输入时多打了空格、打了中文，或者直接回车什么都没输。",
      ],
      code: { bad: 'int("3.5")', good: 'int(float("3.5"))   # 结果是 3' },
      concept: { day: 4, name: "类型转换" },
    }
  }),

  R("ValueError", /could not convert string to float/, () => ({
    title: "这段文字变不成小数",
    lines: ["`float()` 需要 `\"3.14\"` 这种样子的文字。看看是不是混进了空格或者单位。"],
  })),

  R("ValueError", /.*/, () => ({
    title: "值不对头",
    lines: ["类型是对的，但内容不符合要求。看看括号里给进去的到底是什么。"],
  })),

  R("ZeroDivisionError", /.*/, () => ({
    title: "除数是 0",
    lines: [
      "数学上 0 不能当除数，Python 也一样。",
      "常见原因：当除数的那个变量，这一刻的值意外是 0。",
    ],
    code: { bad: "total = 0\nprint(100 / total)", good: "total = 5\nprint(100 / total)" },
  })),

  // ---------------------------------------------------------------- 取值
  R("IndexError", /(list|string|tuple) index out of range/, (m) => ({
    title: "位置编号超出范围了",
    lines: [
      "这个" + (g(m, 1) === "string" ? "字符串" : "列表") + "没有那么长。",
      "⚠️ 记住：Python 从 **0** 开始数。3 个东西的编号是 `0`、`1`、`2`，**没有 `3`**。",
      "想取最后一个，可以直接写 `[-1]`。",
    ],
    code: {
      bad: 'name = "小樱"\nprint(name[2])',
      good: 'name = "小樱"\nprint(name[1])   # 或者 name[-1]',
    },
  })),

  R("KeyError", /(.*)/, (m) => ({
    title: "字典里没有 " + g(m, 1) + " 这个键",
    lines: ["检查一下拼写和大小写，或者这个键是不是还没被放进去。"],
  })),

  R("AttributeError", /['"]([^'"]+)['"] object has no attribute ['"]([^'"]+)['"]/, (m) => ({
    title: cn(g(m, 1)) + "没有 `" + g(m, 2) + "` 这个功能",
    lines: [
      "`." + g(m, 2) + "` 这个用法在" + cn(g(m, 1)) + "上不存在。",
      "多半是**拼写错了**，或者这个方法属于另一种类型 ——",
      "比如 `.upper()` 是字符串才有的，数字没有。",
    ],
    concept: { day: 5, name: "字符串方法" },
  })),

  // ---------------------------------------------------------------- 导入
  R("ModuleNotFoundError", /No module named ['"]([^'"]+)['"]/, (m) => ({
    title: "找不到 `" + g(m, 1) + "` 这个模块",
    lines: [
      "先检查拼写。",
      "如果拼写没问题，那就是这个网站的 Python 里暂时没装它 ——",
      "现阶段课程只会用到 `turtle`、`random`、`math`、`datetime` 这几个。",
    ],
    concept: { day: 8, name: "import 是什么" },
  })),

  R("ImportError", /.*/, () => ({
    title: "导入的东西不存在",
    lines: ["模块找到了，但里面没有你要的那个名字。检查拼写。"],
  })),

  // ---------------------------------------------------------------- 运行时
  R("EOFError", /.*/, () => ({
    title: "程序还想再问一次，但没有输入了",
    lines: [
      "判题的时候，派森酱会按剧本喂给程序几个答案。",
      "如果程序问的次数比剧本准备的多，就会卡在这里。",
      "数一数：你写了几个 `input()`？是不是多写了一个？",
    ],
  })),

  R("RecursionError", /.*/, () => ({
    title: "函数把自己叫醒了太多次",
    lines: ["一个函数一直在调用自己，停不下来。检查递归的出口条件。"],
  })),

  R("FileNotFoundError", /.*/, () => ({
    title: "找不到这个文件",
    lines: ["检查文件名拼写。文件读写要到第 5 阶段才学到，现在还用不上。"],
  })),

  R("OutputOverflow", /.*/, () => ({
    title: "输出太多了，我先把它拦下来了",
    lines: [
      "程序打印了超过 20 万个字，多半是**循环停不下来**。",
      "检查一下：循环里那个用来计数的变量，有没有在每一轮都变大？",
    ],
    code: {
      bad: "n = 0\nwhile n < 5:\n    print(n)",
      good: "n = 0\nwhile n < 5:\n    print(n)\n    n = n + 1   # ← 少了这句就停不下来",
    },
  })),

  R("RuntimeError", /不支持交互输入/, () => ({
    title: "这个环境没法交互输入",
    lines: [
      "浏览器需要「跨域隔离」才能支持 `input()` 停下来等你打字。",
      "请通过 `docker compose` 起的地址访问，或者用 `npm run dev`。",
      "直接双击 html 文件打开是不行的。",
    ],
  })),
]

const FALLBACK = (err) => ({
  title: err.type + "：这条报错我还没学会翻译",
  lines: [
    "派森酱查了半天也没查到这条 (｡•́︿•̀｡)",
    "把下面的英文原文给爸爸看，他能看懂。",
  ],
})

/**
 * @param {{type:string, message:string, line:number|null, traceback?:string}} err
 * @returns {null | {title:string, lines:string[], code?:{bad:string,good:string}, concept?:{day:number,name:string}, line:number|null, raw:string}}
 */
export function translateError(err) {
  if (!err) return null
  for (const rule of RULES) {
    if (rule.type !== err.type) continue
    const m = err.message ? String(err.message).match(rule.pattern) : null
    if (rule.pattern.source === ".*" || m) {
      const built = rule.build(m || [])
      return {
        ...built,
        // 规则能从消息里挖出更准的行号时用规则的
        line: built.line ?? err.line ?? null,
        raw: err.traceback || err.type + ": " + err.message,
      }
    }
  }
  return {
    ...FALLBACK(err),
    line: err.line ?? null,
    raw: err.traceback || err.type + ": " + err.message,
  }
}

/** 报错时派森酱说的话，随机换一句，避免看腻 */
const MASCOT_LINES = [
  "呜哇，程序卡住了…… (；´д｀) 别慌，我来翻译一下他在说什么：",
  "诶？出了点小状况！让派森酱看看…… (・_・;)",
  "报错不是坏事哦，它其实在告诉你哪里需要改～",
  "嗯嗯，这个报错我认识！(๑•̀ㅂ•́)و 它的意思是：",
]

export const errorMascotLine = () =>
  MASCOT_LINES[Math.floor(Math.random() * MASCOT_LINES.length)]
