import { useCallback, useEffect, useMemo, useRef, useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { api, quietly } from "../lib/api"
import { PyRunner, isolated } from "../lib/pyrunner"
import { translateError, errorMascotLine } from "../errors/translate"
import Mascot, { MascotSays } from "../components/Mascot"
import CodeEditor from "../components/CodeEditor"
import Terminal from "../components/Terminal"
import TurtleCanvas from "../components/TurtleCanvas"
import FilePanel from "../components/FilePanel"
import TaskList from "../components/TaskList"
import HintPanel from "../components/HintPanel"
import LessonPanel from "../components/LessonPanel"
import Exercises from "../components/Exercises"
import ErrorCard from "../components/ErrorCard"
import ChallengeCard from "../components/ChallengeCard"
import Diploma from "../components/Diploma"

const CHEER = [
  "★ 任务完成 ★ 今天的你，又变强了一点点！",
  "全部通过！这一关的经验值已经到账 ✨",
  "完美通关！派森酱都看呆了 (,,•̀ ᴗ •́,,)",
  "叮 —— 技能解锁成功！",
]

/** 从 tests.py 源码里抠出任务清单（判题在 Pyodide 里跑，清单在这里显示） */
function extractTasks(testsSrc) {
  const tasks = []
  const re = /"id"\s*:\s*"([^"]+)"\s*,\s*"desc"\s*:\s*"([^"]+)"/g
  let m
  while ((m = re.exec(testsSrc || ""))) tasks.push({ id: m[1], desc: m[2] })
  return tasks
}

export default function DayPage() {
  const { day } = useParams()
  const dayNum = Number(day)
  const navigate = useNavigate()

  const [bundle, setBundle] = useState(null)
  const [loadError, setLoadError] = useState(null)
  const [code, setCode] = useState("")
  const [chunks, setChunks] = useState([])
  const [waitingPrompt, setWaitingPrompt] = useState(null)
  const [running, setRunning] = useState(false)
  const [booting, setBooting] = useState(true)
  const [turtleData, setTurtleData] = useState(null)
  const [judgeResults, setJudgeResults] = useState(null)
  const [judging, setJudging] = useState(false)
  const [err, setErr] = useState(null)
  const [mascotLine, setMascotLine] = useState("")
  const [solution, setSolution] = useState(null)
  const [celebrate, setCelebrate] = useState(false)
  const [tab, setTab] = useState("lesson")
  const [outTab, setOutTab] = useState("terminal")
  const [files, setFiles] = useState([])
  const [plot, setPlot] = useState(null)
  const [persistent, setPersistent] = useState(false)
  const [slowWarn, setSlowWarn] = useState(false)
  const [totalDays, setTotalDays] = useState(10)
  const [snippetPrompt, setSnippetPrompt] = useState(null)
  const [doneToday, setDoneToday] = useState(0)
  const [gradStats, setGradStats] = useState(null)

  const runner = useRef(null)
  const capture = useRef(null)
  const canvasRef = useRef(null)
  const lastOutput = useRef("")
  const saveTimer = useRef(null)

  const meta = bundle?.meta
  const tasks = useMemo(() => extractTasks(bundle?.tests), [bundle?.tests])

  /* ------------------------------------------------------------ 引擎 */
  useEffect(() => {
    const push = (kind) => (text) => {
      if (capture.current) {
        capture.current.push(text)
        return
      }
      lastOutput.current += text
      setChunks((c) => [...c, { kind, text }])
    }

    const r = new PyRunner({
      onStdout: push("stdout"),
      onStderr: push("stderr"),
      onPlot: (dataUrl) => {
        if (capture.current) return
        setPlot(dataUrl)
        setOutTab("plot")
      },
      onFiles: (list) => {
        setFiles(list || [])
        // 第一次写出文件时自动切过去，让她立刻看见「文件真的产生了」
        if ((list || []).length > 0) {
          setOutTab((cur) => (cur === "terminal" ? "files" : cur))
        }
      },
      onTurtle: (data) => {
        if (capture.current) return
        setTurtleData(data)
        if (data?.cmds?.length) setOutTab("canvas")
      },
      onInputRequest: (p) => {
        // 知识卡 / 练习题跑的时候，输入框以浮层形式出现，不去抢主终端
        setSlowWarn(false)
        if (capture.current) setSnippetPrompt(p)
        else setWaitingPrompt(p)
      },
    })
    runner.current = r
    r.start()
      .then((info) => {
        setBooting(false)
        setPersistent(!!(info && info.persistent))
      })
      .catch((e) => {
        setBooting(false)
        setChunks([{ kind: "stderr", text: e.message }])
      })
    return () => r.dispose()
  }, [])

  /* ------------------------------------------------------------ 内容 */
  useEffect(() => {
    let alive = true
    setBundle(null)
    setLoadError(null)
    api
      .getDay(dayNum)
      .then((b) => {
        if (!alive) return
        setBundle(b)
        const saved = b.progress?.code || localStorage.getItem(`code:${dayNum}`)
        setCode(saved && saved.trim() ? saved : b.starter)
        setChunks([])
        setTurtleData(null)
        setPlot(null)
        setJudgeResults(null)
        setErr(null)
        setSolution(null)
        setTab("lesson")
        setOutTab("terminal")
      })
      .catch((e) => alive && setLoadError(e.message))
    api.listDays().then((d) => alive && setTotalDays(d.total || 10)).catch(() => {})
    return () => {
      alive = false
    }
  }, [dayNum])

  /* ------------------------- 把她自己的学习记录注入 Pyodide（Day 65 用）*/
  useEffect(() => {
    if (!bundle?.meta?.uses_my_data || booting || !runner.current) return
    let alive = true
    quietly(api.myData()).then((d) => {
      if (!alive || !d) return
      runner.current
        ?.writeFile("我的学习记录.json", JSON.stringify(d.records, null, 2))
        .catch(() => {})
    })
    return () => {
      alive = false
    }
  }, [bundle, booting])

  /* --------------------------------------------- 自动保存 + 学习时长埋点 */
  useEffect(() => {
    if (!bundle) return
    localStorage.setItem(`code:${dayNum}`, code)
    clearTimeout(saveTimer.current)
    saveTimer.current = setTimeout(() => quietly(api.saveCode(dayNum, code)), 1500)
    return () => clearTimeout(saveTimer.current)
  }, [code, dayNum, bundle])

  useEffect(() => {
    const t = setInterval(() => quietly(api.recordTime(dayNum, 60)), 60000)
    return () => clearInterval(t)
  }, [dayNum])

  /* ------------------------------------------------------------ 运行 */
  const resetOutput = () => {
    setChunks([])
    setPlot(null)
    setErr(null)
    setWaitingPrompt(null)
    lastOutput.current = ""
  }

  const doRun = useCallback(async () => {
    if (!runner.current || running || booting) return
    resetOutput()
    setRunning(true)
    setSlowWarn(false)
    // 8 秒还没结束就提醒一下，但「停下来等她打字」不算卡住
    const slow = setTimeout(() => {
      if (!runner.current?.awaitingInput) setSlowWarn(true)
    }, 8000)
    try {
      const { error, cancelled } = await runner.current.run(code, null)
      if (cancelled) {
        setChunks((c) => [...c, { kind: "stderr", text: "\n（已停止）" }])
      } else if (error) {
        setErr(translateError(error))
        setMascotLine(errorMascotLine())
      }
      quietly(api.recordRun(dayNum, error ? "error" : "ok", error ? { type: error.type } : {}))
    } catch (e) {
      setChunks((c) => [...c, { kind: "stderr", text: String(e.message || e) }])
    } finally {
      clearTimeout(slow)
      setSlowWarn(false)
      setRunning(false)
      setWaitingPrompt(null)
    }
  }, [code, running, booting, dayNum])

  const stop = async () => {
    setWaitingPrompt(null)
    setSlowWarn(false)
    await runner.current?.stop()
    setRunning(false)
  }

  const submitInput = (text) => {
    setWaitingPrompt(null)
    runner.current?.provideInput(text)
  }

  /** 知识卡 / 练习题用的小运行器：输出单独收集，不污染主终端 */
  const runSnippet = useCallback(
    async (src) => {
      if (!runner.current || booting) return { text: "Python 还在启动中…", error: true }
      capture.current = []
      try {
        // 用交互模式跑，这样知识卡里的 input() 也能真的停下来等她打字
        const { error } = await runner.current.run(src, null)
        const text = capture.current.join("")
        const t = error ? translateError(error) : null
        return {
          text: t ? `${text}\n⚠ ${t.title}\n${t.lines[0] || ""}` : text,
          error: !!error,
        }
      } finally {
        capture.current = null
        setSnippetPrompt(null)
      }
    },
    [booting],
  )

  /* ------------------------------------------------------------ 判题 */
  const doJudge = async () => {
    if (!runner.current || judging || running) return
    setJudging(true)
    setErr(null)
    try {
      const res = await runner.current.judge(code, bundle.tests)
      setJudgeResults(res)
      if (res.error && res.syntax) {
        setErr(translateError(res.syntax))
        setMascotLine(errorMascotLine())
      } else if (res.run_error) {
        setErr(translateError(res.run_error))
        setMascotLine(errorMascotLine())
      }
      if (res.all_passed && meta?.graduation) {
        // 毕业证书上要写完成天数和总时长，去后端取一份
        quietly(api.myData()).then((d) => {
          if (!d) return
          const done = d.records.filter((r) => r.status === "done")
          setGradStats({
            done: done.length,
            minutes: done.reduce((sum, r) => sum + (r.minutes || 0), 0),
            longest: d.streak?.longest ?? 0,
          })
        })
      }
      if (res.all_passed) {
        const image = meta?.uses_turtle ? canvasRef.current?.toDataURL() : null
        const done = await quietly(
          api.complete(dayNum, {
            code,
            checks_passed: res.results.map((r) => r.id),
            title: meta?.title || `Day ${dayNum}`,
            snippet: lastOutput.current.slice(0, 600),
            image,
          }),
        )
        setDoneToday(done?.done_today || 0)
        setCelebrate(true)
      }
    } catch (e) {
      setChunks((c) => [...c, { kind: "stderr", text: String(e.message || e) }])
    } finally {
      setJudging(false)
    }
  }

  /* ------------------------------------------------------------ 渲染 */
  if (loadError) {
    return (
      <Centered>
        <Mascot mood="worried" size={96} />
        <p className="mt-3 text-ink-soft">{loadError}</p>
        <Link to="/" className="btn-primary mt-4">
          回首页
        </Link>
      </Centered>
    )
  }

  if (!bundle) {
    return (
      <Centered>
        <Mascot mood="sleepy" size={96} float />
        <p className="mt-3 text-ink-soft">派森酱正在翻今天的教案…</p>
      </Centered>
    )
  }

  const doneExercises = bundle.progress?.exercises_done || []
  const showCanvas = meta.uses_turtle
  // 这一天要用文件，或者目录里本来就有东西，就把文件页显示出来
  const showFiles = meta.uses_files || files.length > 0
  const showPlot = meta.uses_plot || plot !== null

  return (
    <div className="min-h-screen pb-10">
      {/* ---------------------------------------------------------- 顶栏 */}
      <header className="sticky top-0 z-20 border-b border-magic-100 bg-paper/85 backdrop-blur">
        <div className="mx-auto flex max-w-[1700px] flex-wrap items-center gap-3 px-4 py-2.5">
          <Link to="/" className="btn btn-sm btn-ghost">
            ← 首页
          </Link>
          <div className="min-w-0 flex-1">
            <div className="flex items-baseline gap-2">
              <span className="chip bg-magic-500 text-white">Day {dayNum}</span>
              <h1 className="truncate text-[15px] font-bold text-ink">{meta.title}</h1>
            </div>
            {meta.hook && <p className="truncate text-[12.5px] text-ink-soft">{meta.hook}</p>}
          </div>

          <div className="hidden items-center gap-1.5 md:flex">
            {meta.concepts.map((c) => (
              <span key={c} className="chip bg-magic-50 text-magic-600">
                {c}
              </span>
            ))}
          </div>

          <div className="flex items-center gap-2">
            <div className="hidden h-2 w-28 overflow-hidden rounded-full bg-magic-100 sm:block">
              <div
                className="h-full rounded-full bg-gradient-to-r from-magic-400 to-sakura-400 transition-all"
                style={{ width: `${(dayNum / totalDays) * 100}%` }}
              />
            </div>
            <span className="chip bg-paper-sunken text-ink-soft">
              {dayNum} / {totalDays}
            </span>
          </div>
        </div>
      </header>

      {!isolated() && (
        <div className="mx-auto max-w-[1700px] px-4 pt-2">
          <div className="rounded-xl border border-amberly-500/40 bg-amberly-100 px-3 py-2 text-[13px]">
            ⚠️ 当前页面没有开启跨域隔离，<code>input()</code> 用不了。请通过 docker compose
            起的地址访问，或者用 <code>npm run dev</code>。
          </div>
        </div>
      )}

      <div className="mx-auto grid max-w-[1700px] gap-3 px-4 pt-3 xl:grid-cols-[minmax(0,30fr)_minmax(0,38fr)_minmax(0,32fr)]">
        {/* ------------------------------------------------------ 左：讲解 */}
        <section className="card flex max-h-[calc(100vh-7rem)] flex-col overflow-hidden xl:sticky xl:top-[4.2rem]">
          <div className="flex shrink-0 gap-1 border-b border-magic-100 p-1.5">
            <TabBtn active={tab === "lesson"} onClick={() => setTab("lesson")}>
              📖 今日剧情
            </TabBtn>
            {bundle.exercises?.length > 0 && (
              <TabBtn active={tab === "ex"} onClick={() => setTab("ex")}>
                🎯 练习 {doneExercises.length}/{bundle.exercises.length}
              </TabBtn>
            )}
          </div>
          <div className="min-h-0 flex-1 overflow-auto px-4 py-3">
            {tab === "lesson" ? (
              <LessonPanel source={bundle.lesson} runSnippet={runSnippet} busy={running || judging} />
            ) : (
              <Exercises
                exercises={bundle.exercises}
                doneIds={doneExercises}
                runSnippet={runSnippet}
                busy={running || judging}
                onDone={(id) => {
                  quietly(api.recordExercise(dayNum, id)).then(() =>
                    setBundle((b) => ({
                      ...b,
                      progress: {
                        ...b.progress,
                        exercises_done: [...new Set([...(b.progress.exercises_done || []), id])],
                      },
                    })),
                  )
                }}
              />
            )}
          </div>
        </section>

        {/* ------------------------------------------------------ 中：编辑器 */}
        <section className="flex flex-col gap-3">
          <div className="card flex flex-col overflow-hidden">
            <div className="flex flex-wrap items-center gap-2 border-b border-magic-100 bg-paper-sunken/60 px-3 py-2">
              <span className="font-mono text-[12.5px] text-ink-soft">我的代码.py</span>
              <div className="flex-1" />
              <button
                onClick={() => {
                  setCode(bundle.starter)
                  resetOutput()
                  setTurtleData(null)
        setPlot(null)
                }}
                className="btn btn-sm btn-ghost"
              >
                重置
              </button>
              {running ? (
                <button onClick={stop} className="btn btn-sm bg-sakura-500 text-white">
                  ■ 停止
                </button>
              ) : (
                <button onClick={doRun} disabled={booting} className="btn btn-sm btn-primary">
                  {booting ? "启动中…" : "▶ 运行"}
                </button>
              )}
              <button
                onClick={doJudge}
                disabled={booting || running || judging}
                className="btn btn-sm btn-check"
              >
                {judging ? "检查中…" : "✓ 检查任务"}
              </button>
            </div>
            <div className="h-[46vh] min-h-[300px]">
              <CodeEditor value={code} onChange={setCode} errorLine={err?.line} onRunShortcut={doRun} />
            </div>
          </div>

          {slowWarn && (
            <div className="card animate-pop border-amberly-500/40 bg-amberly-100 p-3">
              <MascotSays mood="thinking" tone="amber" size={48}>
                程序跑了 8 秒还没结束…… 是不是循环停不下来了？
                <button onClick={stop} className="btn btn-sm mt-2 bg-sakura-500 text-white">
                  帮我停下来
                </button>
              </MascotSays>
            </div>
          )}

          {err && <ErrorCard error={err} mascotLine={mascotLine} onJumpToLine={() => {}} />}

          {solution && (
            <div className="card animate-pop border-amberly-500/40 p-3.5">
              <div className="mb-2 flex items-center justify-between">
                <h3 className="text-sm font-bold text-ink">📜 参考答案</h3>
                <button onClick={() => setSolution(null)} className="btn btn-sm btn-ghost">
                  收起
                </button>
              </div>
              <pre className="overflow-x-auto rounded-xl bg-[#2E2545] p-3 font-mono text-[12.5px] leading-relaxed text-[#EDE4FF]">
                {solution}
              </pre>
              <p className="mt-2 text-[12.5px] text-ink-soft">
                看完记得回去<strong className="text-magic-600">自己敲一遍</strong>，
                光看会以为自己懂了，手会告诉你真相 (๑•̀ㅂ•́)و
              </p>
            </div>
          )}
        </section>

        {/* ------------------------------------------------------ 右：输出 */}
        <section className="flex flex-col gap-3">
          <div className="card flex flex-col overflow-hidden">
            <div className="flex shrink-0 gap-1 border-b border-magic-100 p-1.5">
              <TabBtn active={outTab === "terminal"} onClick={() => setOutTab("terminal")}>
                🖥 输出
              </TabBtn>
              {showCanvas && (
                <TabBtn active={outTab === "canvas"} onClick={() => setOutTab("canvas")}>
                  🐢 画布
                </TabBtn>
              )}
              {showPlot && (
                <TabBtn active={outTab === "plot"} onClick={() => setOutTab("plot")}>
                  📊 图表
                </TabBtn>
              )}
              {showFiles && (
                <TabBtn active={outTab === "files"} onClick={() => setOutTab("files")}>
                  📁 文件 {files.length > 0 ? files.length : ""}
                </TabBtn>
              )}
            </div>
            <div className={
                (showCanvas && outTab === "canvas") || outTab === "plot"
                  ? "p-2.5"
                  : "h-[34vh] min-h-[220px] p-2.5"
              }>
              {showCanvas && outTab === "canvas" ? (
                <TurtleCanvas ref={canvasRef} data={turtleData} />
              ) : outTab === "plot" ? (
                <PlotPanel src={plot} />
              ) : outTab === "files" ? (
                <FilePanel
                  files={files}
                  persistent={persistent}
                  onRefresh={() => runner.current?.listFiles()}
                  onClear={() => runner.current?.clearFiles()}
                />
              ) : (
                <Terminal
                  chunks={chunks}
                  waitingPrompt={waitingPrompt}
                  onSubmitInput={submitInput}
                  running={running}
                />
              )}
            </div>
          </div>

          <TaskList
            tasks={tasks}
            results={judgeResults?.results}
            notes={judgeResults?.notes}
            judging={judging}
          />

          {meta.challenge && (
            <ChallengeCard
              challenge={meta.challenge}
              unlocked={!!judgeResults?.all_passed || bundle.progress?.status === "done"}
            />
          )}

          {bundle.hints?.length > 0 && (
            <HintPanel
              hints={bundle.hints}
              solutionSeen={!!bundle.progress?.solution_seen}
              onReveal={(lv) => quietly(api.recordHint(dayNum, lv))}
              onWantSolution={async () => {
                const r = await quietly(api.getSolution(dayNum))
                if (r) setSolution(r.solution)
              }}
            />
          )}
        </section>
      </div>

      {/* ------------------------------ 知识卡 / 练习题里的 input() 浮层 */}
      {snippetPrompt !== null && (
        <SnippetInput
          prompt={snippetPrompt}
          onSubmit={(t) => {
            setSnippetPrompt(null)
            runner.current?.provideInput(t)
          }}
          onCancel={async () => {
            setSnippetPrompt(null)
            await runner.current?.stop()
          }}
        />
      )}

      {/* ------------------------------------------------------- 通关庆祝 */}
      {celebrate && meta.graduation && (
        <Diploma
          stats={gradStats}
          onClose={() => setCelebrate(false)}
          onGallery={() => navigate("/gallery")}
        />
      )}

      {celebrate && !meta.graduation && (
        <div className="fixed inset-0 z-40 flex items-center justify-center bg-ink/40 p-4 backdrop-blur-sm">
          <div className="card animate-pop w-full max-w-md p-6 text-center">
            <Mascot mood="excited" size={120} className="mx-auto" float />
            <h2 className="mt-3 text-xl font-bold text-magic-600">
              {CHEER[dayNum % CHEER.length]}
            </h2>
            <p className="mt-1.5 text-[14px] text-ink-soft">
              Day {dayNum}「{meta.title}」已收进你的作品陈列馆 ✨
            </p>
            <div className="mt-3 flex flex-wrap justify-center gap-1.5">
              {meta.concepts.map((c) => (
                <span key={c} className="chip bg-mint-100 text-mint-600">
                  ✓ {c}
                </span>
              ))}
            </div>
            {doneToday >= 3 && (
              <div className="mt-4 rounded-xl border border-amberly-500/40 bg-amberly-100 p-2.5 text-left text-[13px] leading-relaxed">
                <strong className="text-amberly-500">
                  今天已经是第 {doneToday} 关啦，你也太猛了 (๑•̀ㅂ•́)ｼ✧
                </strong>
                <br />
                不过明天再来的话，今天学的会记得更牢哦 —— 当然你想继续我也拦不住！
              </div>
            )}
            {meta.next_teaser && (
              <p className="mt-4 rounded-xl bg-magic-50 p-2.5 text-[13.5px] text-ink">
                <strong className="text-magic-600">明天预告：</strong>
                {meta.next_teaser}
              </p>
            )}
            <div className="mt-5 flex justify-center gap-2">
              <button onClick={() => setCelebrate(false)} className="btn btn-ghost">
                再改改
              </button>
              <Link to="/gallery" className="btn-ghost">
                看陈列馆
              </Link>
              <button
                onClick={() => {
                  setCelebrate(false)
                  navigate(dayNum < totalDays ? `/day/${dayNum + 1}` : "/")
                }}
                className="btn-primary"
              >
                {dayNum < totalDays ? "去第 " + (dayNum + 1) + " 天 →" : "回首页"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

/** 知识卡里的程序在问问题 —— 用浮层收一次输入，避免和主终端抢地盘 */
function SnippetInput({ prompt, onSubmit, onCancel }) {
  const [v, setV] = useState("")
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-ink/30 p-4 backdrop-blur-sm">
      <form
        onSubmit={(e) => {
          e.preventDefault()
          onSubmit(v)
        }}
        className="card animate-pop w-full max-w-sm p-4"
      >
        <div className="flex items-start gap-2.5">
          <Mascot mood="thinking" size={48} className="shrink-0" />
          <div className="min-w-0 flex-1">
            <p className="text-[12px] text-ink-faint">程序在问你：</p>
            <p className="whitespace-pre-wrap break-words font-mono text-[14px] font-bold text-ink">
              {prompt || "（请输入）"}
            </p>
          </div>
        </div>
        <input
          autoFocus
          value={v}
          onChange={(e) => setV(e.target.value)}
          className="mt-3 w-full rounded-xl border border-magic-200 bg-white px-3 py-2 font-mono text-[14px] outline-none focus:border-magic-400"
          placeholder="打完按回车"
          spellCheck={false}
        />
        <div className="mt-3 flex justify-end gap-2">
          <button type="button" onClick={onCancel} className="btn btn-sm btn-ghost">
            算了，停掉
          </button>
          <button type="submit" className="btn btn-sm btn-primary">
            回车 ↵
          </button>
        </div>
      </form>
    </div>
  )
}

/** matplotlib 画出来的图，worker 那边已经转成了 PNG dataURL */
function PlotPanel({ src }) {
  if (!src) {
    return (
      <div className="flex h-[30vh] flex-col items-center justify-center text-center">
        <Mascot mood="normal" size={56} />
        <p className="mt-2 text-[13px] text-ink-soft">还没有图表</p>
        <p className="mt-1 px-4 text-[12px] leading-relaxed text-ink-faint">
          用 <code className="rounded bg-magic-50 px-1">plt.bar(...)</code> 之类画一张，
          图会出现在这里
        </p>
      </div>
    )
  }
  return (
    <div>
      <img
        src={src}
        alt="你画的图表"
        className="w-full rounded-xl border border-magic-100 bg-white shadow-card"
      />
      <p className="mt-2 text-[11.5px] text-ink-faint">
        💡 这是 matplotlib 真正画出来的图 —— 跟专业的数据分析用的是同一个库
      </p>
    </div>
  )
}

function TabBtn({ active, children, onClick }) {
  return (
    <button
      onClick={onClick}
      className={`rounded-lg px-3 py-1.5 text-[13px] font-semibold transition ${
        active ? "bg-magic-500 text-white shadow-pop" : "text-ink-soft hover:bg-magic-50"
      }`}
    >
      {children}
    </button>
  )
}

function Centered({ children }) {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center px-4 text-center">
      {children}
    </div>
  )
}
