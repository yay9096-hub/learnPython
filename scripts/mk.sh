#!/bin/sh
# Makefile 的帮手脚本。
#
# 为什么要有这个文件：
#   Windows 上的 make 会把「配方命令行里的中文」搞成乱码（GNU Make 3.81 实测如此）。
#   把中文提示和稍长的逻辑放进这个 .sh，由 sh 直接读文件执行，
#   字节不经过 make 的命令行，就不会乱码了。
#   顺带 Makefile 也变干净了 —— 配方全是一行调用。
#
# 用法： sh scripts/mk.sh <子命令>

set -u

# 从 PowerShell / cmd 里启动 make 时，Git 的 /usr/bin 不在 PATH 上，
# awk / curl / sed / date 这些全都找不到。
# 这个脚本本身跑在 Git 的 sh 里，所以 /usr/bin 一定是对的，补上即可。
if ! command -v awk >/dev/null 2>&1; then
  PATH="/usr/bin:/bin:$PATH"
  export PATH
fi

URL=${URL:-http://localhost:8080}
DB=data/progress.db

cmd=${1:-help}
[ $# -gt 0 ] && shift

case "$cmd" in

# ------------------------------------------------------------------ 帮助
help)
  # 直接读 Makefile 里的 ## 注释生成。awk 是按字节读文件的，中文不会坏。
  awk '
    BEGIN { FS = ":.*?## " }
    /^##! / { printf "\n  \033[1;35m%s\033[0m\n", substr($0, 5); next }
    /^##\. / { foot = foot substr($0, 5); next }
    /^##@ / { printf "\n  \033[1m%s\033[0m\n", substr($0, 5); next }
    /^[a-zA-Z_-]+:.*?## / { printf "    \033[36m%-13s\033[0m %s\n", $1, $2 }
    END { printf "\n"; if (foot != "") printf "  \033[2m%s\033[0m\n\n", foot }
  ' Makefile
  ;;

# ------------------------------------------------------------------ 环境体检
doctor)
  # 一个字段一行：哪块缺了一眼就能看出来
  probe() {   # probe <显示名> <命令> <取版本的参数> <缺了怎么办>
    name=$1; bin=$2; verarg=$3; fix=$4
    if command -v "$bin" >/dev/null 2>&1; then
      ver=$("$bin" $verarg 2>&1 | head -1)
      printf "  \033[32m✓\033[0m %-10s %s\n" "$name" "$ver"
    else
      printf "  \033[31m✗\033[0m %-10s 没找到 —— %s\n" "$name" "$fix"
    fi
  }

  printf "\n  \033[1;35m环境体检\033[0m\n\n"
  printf "  \033[1m跑网站必须的\033[0m\n"
  probe "docker" docker --version "winget install Docker.DockerDesktop（或走 make dev-api/dev-web）"
  probe "node" node --version "winget install OpenJS.NodeJS.LTS"
  probe "npm" npm --version "跟 node 一起装"
  probe "python" python --version "已经有 Anaconda 的话通常没问题"

  printf "\n  \033[1mmake 自己要用的\033[0m\n"
  probe "sh" sh --version "装 Git for Windows"
  probe "bash" bash --version "装 Git for Windows"
  probe "awk" awk --version "Git for Windows 自带"
  probe "curl" curl --version "系统自带"

  if command -v docker >/dev/null 2>&1; then
    printf "\n  \033[1mDocker 起来了吗\033[0m\n"
    if docker info >/dev/null 2>&1; then
      printf "  \033[32m✓\033[0m 已启动，可以 make up\n"
    else
      printf "  \033[33m!\033[0m 装了但没启动 —— 打开 Docker Desktop 等托盘图标变绿\n"
    fi
  fi

  printf "\n  \033[1m进度数据\033[0m\n"
  if [ -f "$DB" ]; then
    done_days=$(python -c "
import sqlite3,sys
try:
    c=sqlite3.connect(sys.argv[1])
    print(c.execute(\"SELECT COUNT(*) FROM progress WHERE status='done'\").fetchone()[0])
except Exception:
    print('?')
" "$DB" 2>/dev/null)
    printf "  \033[32m✓\033[0m %s（%s）—— 已通关 \033[1m%s\033[0m 天\n" \
      "$DB" "$(ls -lh "$DB" | awk '{print $5}')" "$done_days"
  else
    printf "  \033[2m·\033[0m 还没有进度（第一次跑很正常）\n"
  fi
  n=$(ls -1 data/backups/progress-*.db 2>/dev/null | wc -l | tr -d ' ')
  if [ "$n" -gt 0 ]; then
    printf "  \033[32m✓\033[0m 备份 %s 份（data/backups/，make backups 可查看）\n" "$n"
  else
    printf "  \033[2m·\033[0m 还没有备份 —— 后端启动一次就会自动存\n"
  fi
  printf "\n"
  ;;

# ------------------------------------------------------------------ 前置检查
# make 在 Windows 上会把 `docker compose build` 直接丢给 CreateProcess，
# docker 不存在时报的是 "CreateProcess ... failed, e=2 系统找不到指定的文件"，
# 完全看不出是缺 docker。所以在真正跑之前先自己查一遍，给句人话。
require-docker)
  if ! command -v docker >/dev/null 2>&1; then
    printf "\n  \033[1;31mDocker 还没装\033[0m —— make up / build / logs 都要用它。\n\n"
    printf "  装它：\n"
    printf "      \033[1mwinget install Docker.DockerDesktop\033[0m\n"
    printf "  装完要重启电脑，并且先把 Docker Desktop 打开（托盘图标变绿）再回来。\n\n"
    printf "  \033[1m不装 Docker 也能用\033[0m，功能一模一样：\n"
    printf "      make install     装依赖（只用做一次）\n"
    printf "      make dev-api     终端 1\n"
    printf "      make dev-web     终端 2\n"
    printf "  然后打开 \033[1;36mhttp://localhost:5173\033[0m\n\n"
    exit 1
  fi
  if ! docker info >/dev/null 2>&1; then
    printf "\n  \033[1;33mDocker 装了，但还没启动\033[0m。\n"
    printf "  打开 Docker Desktop，等托盘图标变绿，再跑一次。\n\n"
    exit 1
  fi
  ;;

# ------------------------------------------------------------ 起服务/停服务
wait-ready)
  printf "  等待后端就绪"
  i=0
  while [ "$i" -lt 60 ]; do
    if curl -fsS "$URL/api/days" >/dev/null 2>&1; then
      printf "\n\n  ✨ 派森酱学院已启动： \033[1;36m%s\033[0m\n\n" "$URL"
      exit 0
    fi
    printf "."
    sleep 1
    i=$((i + 1))
  done
  printf "\n\n  ⚠ 60 秒还没起来，看看日志： make logs\n\n"
  exit 1
  ;;

said-down)
  printf "  已停止。进度还在 ./data 里，下次 make up 接着用。\n"
  ;;

health)
  if curl -fsS "$URL/api/days" >/dev/null 2>&1; then
    printf "  ✓ 服务正常： %s\n" "$URL"
  else
    # 故意不返回非 0：这是给人看的检查，不想让 make 再糊一堆 Error 1 上去
    printf "  ✗ 连不上 %s，先 make up\n" "$URL"
  fi
  ;;

open)
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL"
  elif command -v open >/dev/null 2>&1; then
    open "$URL"
  elif command -v explorer.exe >/dev/null 2>&1; then
    explorer.exe "$URL" || true   # explorer 成功也返回非 0，别让它把 make 带崩
  else
    printf "  自己点开吧： %s\n" "$URL"
  fi
  ;;

# ------------------------------------------------------------------ 数据
backup)
  if [ ! -f "$DB" ]; then
    printf "  还没有进度可备份（%s 不存在）\n" "$DB"
    exit 0
  fi
  mkdir -p data/backups
  cp "$DB" "data/backups/progress-$(date +%Y%m%d-%H%M%S).db"
  printf "  已备份 → data/backups/\n"
  ls -1t data/backups | head -5 | sed 's/^/    /'
  ;;

backups)
  if [ ! -d data/backups ] || [ -z "$(ls -A data/backups 2>/dev/null)" ]; then
    printf "\n  还没有任何备份。后端每次启动会自动存一份。\n\n"
    exit 0
  fi
  printf "\n  \033[1m可用的备份\033[0m（新的在上面）\n\n"
  i=0
  for f in $(ls -1t data/backups/progress-*.db 2>/dev/null); do
    i=$((i + 1))
    size=$(ls -lh "$f" | awk '{print $5}')
    days=$(python -c "
import sqlite3,sys
try:
    c=sqlite3.connect(sys.argv[1])
    print(c.execute(\"SELECT COUNT(*) FROM progress WHERE status='done'\").fetchone()[0])
except Exception:
    print('?')
" "$f" 2>/dev/null)
    printf "  %2d) %-42s %6s  已通关 %s 天\n" "$i" "$(basename "$f")" "$size" "$days"
  done
  printf "\n  恢复： \033[36mmake restore FILE=progress-20260901-2256.db\033[0m\n\n"
  ;;

restore)
  f=${FILE:-}
  if [ -z "$f" ]; then
    printf "\n  用法： \033[36mmake restore FILE=<备份文件名>\033[0m\n"
    printf "  先看看有哪些备份： \033[36mmake backups\033[0m\n\n"
    exit 1
  fi
  # 只给文件名也行，自动补上 data/backups/ 前缀
  case "$f" in
    */*) src="$f" ;;
    *)   src="data/backups/$f" ;;
  esac
  if [ ! -f "$src" ]; then
    printf "\n  找不到这个备份： %s\n" "$src"
    printf "  用 \033[36mmake backups\033[0m 看看有哪些可选\n\n"
    exit 1
  fi
  # 覆盖之前，先把当前的也存一份 —— 万一恢复错了还能再翻回来
  if [ -f "$DB" ]; then
    mkdir -p data/backups
    cp "$DB" "data/backups/progress-before-restore-$(date +%Y%m%d-%H%M%S).db"
  fi
  cp "$src" "$DB"
  printf "\n  ✓ 已恢复： %s\n" "$(basename "$src")"
  printf "  （恢复前的那份也存起来了，翻车了还能再翻回来）\n"
  printf "  \033[1m重启后端才会生效\033[0m —— Ctrl+C 之后重新 make dev-api\n\n"
  ;;

reset-data)
  printf "\n  \033[1;31m这会清空所有学习进度\033[0m（做过的天数、代码、作品陈列馆）。\n"
  printf "  清空前会自动备份一份到 backups/。\n"
  printf "  确定的话输入 yes ： "
  # 读不到输入（比如被管道喂了个 EOF）就当成「取消」——
  # 删数据这种事，默认必须是不删
  ans=""
  read -r ans || true
  if [ "$ans" != "yes" ]; then
    printf "  取消了，什么都没动。\n"
    exit 0
  fi
  if [ ! -f "$DB" ]; then
    printf "  本来就是空的，没事做。\n"
    exit 0
  fi
  mkdir -p data/backups
  cp "$DB" "data/backups/progress-before-reset-$(date +%Y%m%d-%H%M%S).db"
  rm -f "$DB"
  printf "  已清空（旧的那份在 backups/ 里）。\n"
  ;;

# ------------------------------------------------------------------ 清理
clean)
  rm -rf frontend/dist frontend/node_modules frontend/public/pyodide
  rm -rf backend/app/__pycache__ frontend/public/py/__pycache__ docs/__pycache__
  printf "  清理完毕。\033[1m学习进度没有动\033[0m，还在 ./data 里。\n"
  printf "  下次 make up 会重新构建，要几分钟。\n"
  ;;

*)
  printf "  不认识的子命令： %s\n" "$cmd"
  exit 1
  ;;

esac
