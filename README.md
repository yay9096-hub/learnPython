# 派森酱学院 ✨

一个本地部署的、面向零基础高中生的 Python 学习网站。
**每天一个小项目**，当天的知识点全部融进项目里，浏览器内直接写代码、运行、调试。

- 学习者：高中生，零编程基础，中文，喜欢二次元
- 部署：本机 `docker compose up -d`，浏览器打开即可，**断网也能用**
- 已完成：**全部 70 天** ✅ 七章内容全部上线

---

## 快速开始

```bash
make up
```

然后打开 <http://localhost:8080>

> 首次构建要几分钟（前端会把 13MB 的 Pyodide 运行时打进镜像）。
> 之后再启动就是秒开。

停止（**学习进度会保留**）：

```bash
make down
```

看看还有哪些命令：

```bash
make help
```

### 常用命令

| 命令 | 作用 |
|---|---|
| `make up` | 起服务，自动构建并等它就绪 |
| `make down` | 停服务（进度保留） |
| `make logs` | 跟踪日志，排查问题用 |
| `make health` | 后端还活着吗 |
| `make backup` | 手动备份学习进度 |
| `make backups` | 列出所有备份，看每份存了几天 |
| `make restore FILE=xxx.db` | 从备份恢复 |
| `make doctor` | 环境体检：docker / node / npm / python 齐了吗 |
| `make verify` | 课程内容自检 |
| `make clean` | 删镜像和构建产物，**进度不动** |
| `make reset-data` | ⚠ 清空学习进度（会先自动备份，要输 `yes`） |

`./data` 是 bind mount 不是 docker volume，所以 `up` / `down` / `clean` 都碰不到进度库。
**唯一会清掉进度的是 `make reset-data`。**

### 进度数据在哪、怎么找回

- 数据库：`data/progress.db`（一个 SQLite 文件，`make dev-api` 和 `make up` 用的是**同一个**）
- **后端每次启动会自动备份一份**到 `data/backups/`，保留最近 30 份
- 后端启动时会把路径和已通关天数打在日志里，一眼能看见
- 出事了：`make backups` 看有哪些备份 → `make restore FILE=progress-xxx.db` 恢复 → 重启后端

> ⚠️ 手动 `rm data/progress.db` 会删掉她的全部学习记录。
> 要清空请用 `make reset-data`（会先自动备份，且需要输入 yes 确认）。

### Windows 上怎么用 make

```
winget install ezwinports.make
```

装完**关掉终端重开**（PATH 要重新加载），然后 `cd` 到项目目录跑 `make help`。

**Git Bash 和 PowerShell 都能用** —— Makefile 会自动找到 Git for Windows 自带的
`sh.exe` 并把它的 `/usr/bin` 补进 PATH，所以不用特意切终端。
前提是装了 Git for Windows（装在默认路径 `C:\Program Files\Git`）。

不想折腾 make 的话，所有命令都能换回原始写法，比如 `make up` → `docker compose up -d --build`。

### 还需要装 Docker

`make up` / `make build` 要 Docker：

```
winget install Docker.DockerDesktop
```

装完**要重启电脑**，并且**先把 Docker Desktop 打开**（托盘图标变绿）再跑 `make up`。

> 暂时不想装 Docker 也能用 —— 走下面的「不用 Docker 的话」，功能完全一样。

### 不用 Docker 的话

先装依赖，然后开**两个终端**：

```bash
make install
```

```bash
make dev-api
```

```bash
make dev-web
```

然后打开 <http://localhost:5173>

> ⚠️ **不要直接双击 html 文件打开**。`input()` 依赖 SharedArrayBuffer，
> 需要 `COOP`/`COEP` 响应头，只有通过上面两种方式访问才有。

---

## 它长什么样

三栏布局：**左边讲解 / 中间编辑器 / 右边输出**。

| 区域 | 内容 |
|---|---|
| 左栏 | 今日剧情（讲解，每个知识点都带一张**可当场运行、可随手改**的知识卡）+ 练习题标签页 |
| 中栏 | 代码编辑器（CodeMirror）· 运行 / 停止 / 检查任务 · 出错时整行标红 |
| 右栏 | 输出终端（`input()` 会在这里长出输入框）· 🐢 turtle 画布 · 任务清单 · 分级提示 |

### 几个关键设计

- **中文报错翻译器** —— 30+ 条常见 Traceback 翻译成人话，附「改之前 / 改之后」对照代码，
  还能一键跳回相关知识点。零基础最大的劝退点就是看不懂英文报错。
  源码在 [frontend/src/errors/translate.js](frontend/src/errors/translate.js)。
- **四种题型混着来** —— 预测（先猜再跑）、修 bug、补全、创作。
  不是每天都从空白文件写起，不然第 5 天就崩溃了。
- **分级提示** —— 思路 → 伪代码 → 关键代码，参考答案要二次确认才给。
- **作品陈列馆** —— 每完成一天自动生成作品卡（turtle 作品会存画布截图）。
- **派森酱** —— 紫发双马尾的 AI 搭档，纯 SVG 手绘，会换表情。
  绝不说「你错了」，只说「这里再看看」。

---

## 课程表

| Day | 知识点 | 项目 |
|---|---|---|
| 1 | print / 字符串 / 注释 | 二次元角色出场卡 |
| 2 | 变量 / f-string | 角色属性面板 |
| 3 | 数字 / 运算符 / 整除取余 | 伤害计算器 |
| 4 | input / 类型转换 | 入学登记处 |
| 5 | 字符串方法 / len | 中二称号生成器 |
| 6 | 转义字符 / 三引号 / sep end | 剧情对话框 |
| 7 | **复习作品日** | RPG 开场白系统 |
| 8 | import / turtle | 画一颗魔法星星 🌟 |
| 9 | turtle 坐标 / 填充 | 专属魔法阵 🔮 |
| 10 | random | 命运抽卡机 🎴 |

### 第二章 · 会判断和重复（D11–22）

| Day | 知识点 | 项目 |
|---|---|---|
| 11 | `if` / `else` | 魔法结界 |
| 12 | `elif` / 多分支 | 属性克制判定 |
| 13 | `and` / `or` / `not` / `in` | 入学资格审查 |
| 14 | `while` | **猜数字游戏** 🎯 |
| 15 | `for` + `range` | 星星金字塔 |
| 16 | 循环 + turtle | **万花筒**（Day 8 的 9 行变 3 行）🌸 |
| 17 | `break` / `continue` / 统计 | **十连抽**（回收 Day 10）🎴 |
| 18 | 嵌套循环 | 图案生成器 |
| 19 | 循环 + 随机 + turtle | 星空生成器 ✨ |
| 20 | 状态循环 | 回合制战斗模拟 |
| 21 | **复习作品日** | 文字冒险游戏 🎮 |
| 22 | 综合挑战 | 猜数字 · 进化版 |

D1–10 刻意**不引入 `if` 和循环**（那是第二章的事），视觉化靠 turtle 撑场面。
第二章刻意安排了三个「**回收时刻**」（D16、D17、D22）——
让她亲眼看到「上周那个笨办法，今天三行就写完了」。

### 第三章 · 会管理数据（D23–34）

| Day | 知识点 | 项目 |
|---|---|---|
| 23 | 列表 / 索引 / `len` | 队伍名单 |
| 24 | `append` / `remove` / `pop` | 背包系统 🎒 |
| 25 | 遍历统计 / `sum` `max` `min` | 队伍属性统计 |
| 26 | 切片 | 抽卡记录分析 🔪 |
| 27 | `sort` / `key=lambda` | 战力排行榜 🏆 |
| 28 | `split` / `join` | 弹幕分析器 💬 |
| 29 | 字典 | 角色档案 🗂 |
| 30 | `.items()` / `.values()` | 图鉴系统 📖 |
| 31 | 列表套字典 | 队伍数据库 🗃 |
| 32 | 集合 `set` | 共同好友 🔗 |
| 33 | 元组 / 解包 / `zip` | 星座连线图 ✨ |
| 34 | **复习作品日** | 班级成绩管理系统 📊 |

第四至七章（D35–70）的完整设计见 [docs/07](docs/07-第二至七章设计.md)。

---

## 目录结构

```
learnPython/
├── Makefile            ← make help 看全部命令
├── scripts/mk.sh       ← Makefile 的帮手脚本（中文提示都在这里）
├── docker-compose.yml
├── content/            ← 课程内容，改完刷新页面就生效，不用重建镜像
│   └── day-001/ …
├── frontend/           ← Vite + React + CodeMirror + Pyodide
│   ├── public/py/      ← 跑在 Pyodide 里的 Python：判题器 / turtle / 运行外壳
│   └── src/errors/     ← ★ 中文报错翻译器
├── backend/            ← FastAPI，只管进度和作品，不碰代码执行
├── data/               ← progress.db（备份 = 复制这个目录）
└── docs/               ← 设计文档
```

Python **跑在浏览器里**（Pyodide + WebAssembly），后端完全不执行学生代码。
所以写死循环最多卡住一个 Web Worker，点「停止」就没事，机器很安全。

---

## 怎么加新的一天

新建 `content/day-011/`，放这 7 个文件：

| 文件 | 作用 |
|---|---|
| `meta.json` | 标题、钩子、知识点、明日预告、速查条目 |
| `lesson.md` | 讲解。用 ` ```python runnable 标题 ` 代码块生成「可运行知识卡」 |
| `starter.py` | 带 `# TODO` 的初始代码 |
| `solution.py` | 参考答案 |
| `tests.py` | 判题用例（写法见下） |
| `hints.md` | 用 `## 提示 N · 标题` 分级 |
| `exercises.json` | 练习题：`predict` / `fixbug` / `fill` |

`tests.py` 的写法：

```python
CASES = [{
    "stdin": ["星野樱", "16"],          # 判题时按顺序喂给 input()
    "checks": [{
        "id": "name",
        "desc": "学生证上有名字",         # 任务清单上显示这句
        "type": "stdout_contains", "value": "星野樱",
        "fail": "把 {name} 打印到学生证上",   # ← 没过时给出**具体**提示，别写「测试失败」
    }],
}]
```

可用的 `type`：`stdout_contains` / `stdout_regex` / `stdout_lines_min` /
`stdout_has_number` / `var_equals` / `var_exists` / `var_type` / `func_returns` /
`ast_has` / `ast_calls` / `ast_imports` / `turtle_min_ops` / `turtle_colors_min` /
`custom`（在 `tests.py` 里自己写个函数）。

全部实现在 [frontend/public/py/judge.py](frontend/public/py/judge.py)。

### 加完之后自检

```bash
make verify
```

会做两件事：确认每天的 `solution.py` **能通过**、`starter.py` **不能通过**。
（不用 make 的话：`PYTHONIOENCODING=utf-8 python docs/verify_content.py`）

---

## 文档

| 文档 | 内容 |
|---|---|
| [01-产品设计](docs/01-产品设计.md) | 三个决定成败的判断、9 个学习网站调研 |
| [02-UI功能设计](docs/02-UI功能设计.md) | 页面布局、交互细节、有意不做的功能 |
| [03-课程大纲](docs/03-课程大纲.md) | 70 天七阶段编排、内容文件规范 |
| [04-技术架构](docs/04-技术架构.md) | 选型理由、两个 Pyodide 坑的解法、判题机制 |
| [05-待决策与风险](docs/05-待决策与风险.md) | 风险清单与落地节奏 |
| [06-已确认决策](docs/06-已确认决策.md) | 拍板结果、派森酱人设与话术、实现记录与已知限制 |

---

## 下一步

先让她真的用这 10 天，然后看三件事：

1. 她卡在哪个知识点（后台记了 `hints_used` 和 `error_count`）
2. 她喜欢哪类项目（文字的还是画图的）
3. 哪些功能她根本没点过

**再决定第二章怎么写。她的真实反馈比任何推测都值钱。**

## 课程全貌

| 章 | 天数 | 主题 | 代表作品 |
|---|---|---|---|
| 一 | D1–10 | 会说话 | 角色卡、伤害计算器、魔法阵、抽卡机 |
| 二 | D11–22 | 会判断和重复 | 猜数字、十连抽、星空生成器、文字冒险 |
| 三 | D23–34 | 会管理数据 | 背包系统、战力排行榜、弹幕分析器、成绩管理系统 |
| 四 | D35–44 | 会拆分问题 | 队伍函数库、代码重构、递归分形树 |
| 五 | D45–54 | 会和外界打交道 | 日记本、错题本、**游戏存档**、学习打卡、记账本 |
| 六 | D55–63 | 会造东西 | 角色类、继承与多态、卡牌对战、电子宠物 |
| 七 | D64–70 | 会做出好看的 | 数据图表、**她自己的学习曲线**、科赫雪花、五子棋、毕业作品 |

每天包含：**讲解 + 可运行知识卡 + 主线项目 + 7~26 项判题 + 4~7 道练习
+ 三级提示 + 参考答案 + 可选挑战关**。

### 技术能力

| 能力 | 说明 |
|---|---|
| 浏览器内跑 Python | Pyodide（WASM），完全离线，不用装任何东西 |
| 真交互 `input()` | SharedArrayBuffer + Atomics 实现阻塞式输入 |
| turtle 绘图 | 自写 Canvas shim，带绘制动画 |
| matplotlib 图表 | 13 个 wheel 打包在本地，按需载入 |
| **文件持久化** | IDBFS 挂载，她写的文件关掉浏览器还在 |
| 中文报错翻译 | 30+ 条常见 Traceback 翻译成人话 + 修改示例 |
| 多维判题 | 输出 / 变量值 / AST 结构 / 函数返回值 / 类结构 / turtle / 图表 |
| 进度持久化 | SQLite，后端每次启动自动备份，保留 30 份 |
