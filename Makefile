# 派森酱学院 · 常用命令
#
# 数据安全说明（重要）：
#   ./data 是 bind mount，不是 docker volume。
#   所以 up / down / restart / build / clean 都不会碰到学习进度，
#   唯一会清空进度的是 `make reset-data`，而且要手动输入 yes 确认。
#
# Windows 用户：请在 Git Bash 里运行（不是 cmd / PowerShell），
#   因为配方是 POSIX shell 语法。装 make： winget install ezwinports.make
#
# 注意：所有中文提示都在 scripts/mk.sh 里，配方本身保持纯 ASCII ——
#   Windows 上的 make 会把命令行里的中文搞成乱码（3.81 实测如此）。

# Windows 上 make 默认调 cmd.exe，那样下面的配方一句都跑不了
#   （典型症状：'URL' 不是内部或外部命令）。
# Git Bash 里 sh.exe 就在 PATH 上；PowerShell / cmd 里不在，
# 所以直接指向 Git for Windows 的安装路径。
# 用 8.3 短名（PROGRA~1）是为了绕开路径里的空格 —— make 处理带空格的 SHELL 很不稳。
GIT_SH := $(firstword $(wildcard C:/PROGRA~1/Git/usr/bin/sh.exe C:/PROGRA~2/Git/usr/bin/sh.exe))

ifeq ($(OS),Windows_NT)
ifeq ($(GIT_SH),)
$(warning [make] sh.exe not found. Install Git for Windows, or run make from Git Bash.)
SHELL := sh.exe
else
SHELL := $(GIT_SH)
endif
# 光有 sh 还不够：配方里会用到 awk / curl / sed，npm 本身还是个
# `#!/usr/bin/env bash` 脚本。从 PowerShell 启动时这些都不在 PATH 上
# （症状：/usr/bin/env: 'bash': No such file or directory），所以补进去。
ifneq ($(GIT_SH),)
export PATH := $(patsubst %/sh.exe,%,$(GIT_SH));$(PATH)
endif
else
SHELL := /bin/sh
endif

# docker compose v2 是 `docker compose`，老版本是 `docker-compose`
DC   ?= docker compose
PORT ?= 8080
URL  := http://localhost:$(PORT)

# 本地开发（不走 docker）用的解释器
PY  ?= python
NPM ?= npm

# 用 $(SHELL) 的绝对路径调用，不写裸 `sh` ——
# 从 PowerShell 启动时 PATH 上没有 sh，裸写会报 command not found。
MK := URL=$(URL) $(SHELL) scripts/mk.sh

.DEFAULT_GOAL := help

.PHONY: help doctor check-docker build up down restart rebuild logs logs-api logs-web \
        ps health open verify backup backups restore clean reset-data clean-all \
        install dev-api dev-web

##! 派森酱学院 · make 命令
##. 学习进度存在 ./data，只有 make reset-data 会清掉它。

help: ## 显示这份命令列表
	@$(MK) help

# 内部目标：确认 docker 装了而且起来了。没有 ## 注释，所以不出现在 help 里。
check-docker:
	@$(MK) require-docker

##@ 日常使用

up: check-docker ## 起服务（首次会自动构建），然后等它就绪
	@$(DC) up -d --build
	@$(MK) wait-ready

down: check-docker ## 停服务（学习进度保留）
	@$(DC) down
	@$(MK) said-down

restart: ## 重启服务
	@$(MAKE) down
	@$(MAKE) up

build: check-docker ## 只构建镜像，不启动
	@$(DC) build

rebuild: check-docker ## 不用缓存重新构建（依赖或 Dockerfile 改了之后用）
	@$(DC) build --no-cache

open: ## 用浏览器打开网站
	@$(MK) open

##@ 排查问题

ps: check-docker ## 看容器状态
	@$(DC) ps

logs: check-docker ## 跟踪全部日志（Ctrl+C 退出）
	@$(DC) logs -f --tail=100

logs-api: ## 只看后端日志
	@$(DC) logs -f --tail=100 api

logs-web: ## 只看前端 / nginx 日志
	@$(DC) logs -f --tail=100 web

health: ## 检查后端活着没
	@$(MK) health

doctor: ## 环境体检：docker / node / npm / python 都齐了吗
	@$(MK) doctor

##@ 内容维护

verify: ## 课程内容自检（solution 必须过、starter 必须不过）
	@PYTHONIOENCODING=utf-8 $(PY) docs/verify_content.py

backup: ## 手动备份学习进度（后端每次启动也会自动备份）
	@$(MK) backup

backups: ## 列出所有备份，看每份存了几天进度
	@$(MK) backups

restore: ## 从备份恢复： make restore FILE=progress-xxx.db
	@FILE="$(FILE)" $(MK) restore

##@ 本地开发（不走 docker，要开两个终端）

install: ## 装本地开发依赖（前端 npm + 后端 pip）
	@cd frontend && $(NPM) install
	@$(PY) -m pip install -r backend/requirements.txt

dev-api: ## 终端 1：起后端（端口 8000）
	@CONTENT_DIR=content DATA_DIR=data \
		$(PY) -m uvicorn backend.app.main:app --reload --port 8000

dev-web: ## 终端 2：起前端（端口 5173，代理 /api 到 8000）
	@cd frontend && $(NPM) run dev

##@ 清理

clean: ## 停服务 + 删镜像和构建产物（★ 进度不动）
	@$(DC) down --rmi local --remove-orphans 2>/dev/null || $(DC) down 2>/dev/null || true
	@$(MK) clean

reset-data: ## ⚠ 清空学习进度（会先自动备份到 data/backups/，需输入 yes 确认）
	@$(MK) reset-data

clean-all: ## ⚠ clean + reset-data，恢复到刚下载的样子
	@$(MAKE) clean
	@$(MAKE) reset-data
