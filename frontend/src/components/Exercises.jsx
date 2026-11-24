import { useState } from "react"
import CodeEditor from "./CodeEditor"
import { md } from "../lib/markdown"
import Mascot from "./Mascot"

const inline = (t) => ({ __html: md(t || "").replace(/^<p>|<\/p>\n?$/g, "") })

const NICE = ["答对啦！(๑˃̵ᴗ˂̵)و", "就是这个！", "漂亮～ ✨", "完全正确！"]
const NUDGE = ["再看看这里？", "差一点点，回去数一数～", "嗯……不是这个哦，换一个试试"]
const pick = (a) => a[Math.floor(Math.random() * a.length)]

/* ------------------------------------------------------- 预测题：先猜再跑 */
function Predict({ ex, done, onDone }) {
  const [chosen, setChosen] = useState(null)
  const ok = chosen === ex.answer

  return (
    <div className="space-y-2">
      <div className="prose-py text-[13.5px]" dangerouslySetInnerHTML={inline(ex.question)} />
      <pre className="overflow-x-auto rounded-xl bg-[#2E2545] p-3 font-mono text-[12.5px] leading-relaxed text-[#EDE4FF]">
        {ex.code}
      </pre>
      <div className="grid gap-1.5">
        {ex.options.map((opt, i) => {
          const picked = chosen === i
          const state = chosen === null ? "idle" : i === ex.answer ? "right" : picked ? "wrong" : "idle"
          return (
            <button
              key={i}
              disabled={ok || done}
              onClick={() => {
                setChosen(i)
                if (i === ex.answer) onDone?.()
              }}
              className={`rounded-xl border px-3 py-2 text-left font-mono text-[13px] transition ${
                state === "right"
                  ? "border-mint-500 bg-mint-100 text-mint-600"
                  : state === "wrong"
                    ? "border-sakura-400 bg-sakura-50 text-sakura-500"
                    : "border-magic-100 bg-white hover:border-magic-200 hover:bg-magic-50"
              }`}
            >
              <span className="mr-2 font-round font-bold text-ink-faint">
                {String.fromCharCode(65 + i)}.
              </span>
              <span className="whitespace-pre-wrap">{opt}</span>
            </button>
          )
        })}
      </div>
      {chosen !== null && (
        <div
          className={`animate-pop flex items-start gap-2 rounded-xl p-2.5 text-[13px] ${
            ok ? "bg-mint-100 text-ink" : "bg-amberly-100 text-ink"
          }`}
        >
          <Mascot mood={ok ? "happy" : "thinking"} size={36} className="shrink-0" />
          <div className="mt-1">
            <strong>{ok ? pick(NICE) : pick(NUDGE)}</strong>
            {ok && ex.explain && (
              <div className="prose-py mt-1 text-[13px]" dangerouslySetInnerHTML={inline(ex.explain)} />
            )}
          </div>
        </div>
      )}
    </div>
  )
}

/* ---------------------------------------- 修 bug / 补全：小编辑器 + 跑一下 */
function CodeTask({ ex, runSnippet, busy, done, onDone }) {
  const [src, setSrc] = useState(ex.code)
  const [state, setState] = useState(null) // {ok, text}
  const [running, setRunning] = useState(false)

  const check = async () => {
    setRunning(true)
    try {
      const r = await runSnippet(src)
      const out = (r.text || "").replace(/\s+/g, " ").trim()
      let ok = !r.error
      if (ok && ex.expect_contains) {
        const wants = Array.isArray(ex.expect_contains) ? ex.expect_contains : [ex.expect_contains]
        ok = wants.every((w) => out.includes(String(w).replace(/\s+/g, " ").trim()))
      }
      setState({ ok, text: r.text, error: r.error })
      if (ok) onDone?.()
    } finally {
      setRunning(false)
    }
  }

  const lines = src.split("\n").length

  return (
    <div className="space-y-2">
      <div className="prose-py text-[13.5px]" dangerouslySetInnerHTML={inline(ex.question)} />
      <div
        className="overflow-hidden rounded-xl border border-magic-100"
        style={{ height: Math.min(Math.max(lines, 3), 12) * 26 + 14 }}
      >
        <CodeEditor value={src} onChange={setSrc} onRunShortcut={check} />
      </div>
      <div className="flex items-center gap-2">
        <button onClick={check} disabled={running || busy} className="btn btn-sm bg-magic-500 text-white">
          {running ? "跑一下…" : "▶ 跑跑看"}
        </button>
        {src !== ex.code && (
          <button onClick={() => setSrc(ex.code)} className="btn btn-sm btn-ghost">
            还原
          </button>
        )}
        {done && <span className="chip bg-mint-100 text-mint-600">已完成 ✓</span>}
      </div>
      {state && (
        <div className="animate-pop space-y-1.5">
          <pre
            className={`overflow-x-auto whitespace-pre-wrap rounded-xl p-2.5 font-mono text-[12.5px] ${
              state.error ? "bg-sakura-50 text-sakura-500" : "bg-[#241C3B] text-[#E8DEFF]"
            }`}
          >
            {state.text || "（没有输出）"}
          </pre>
          <div
            className={`flex items-start gap-2 rounded-xl p-2.5 text-[13px] ${
              state.ok ? "bg-mint-100" : "bg-amberly-100"
            }`}
          >
            <Mascot mood={state.ok ? "happy" : "thinking"} size={36} className="shrink-0" />
            <div className="mt-1">
              <strong>{state.ok ? pick(NICE) : "还没好哦"}</strong>
              {!state.ok && ex.nudge && (
                <div className="prose-py mt-1 text-[13px]" dangerouslySetInnerHTML={inline(ex.nudge)} />
              )}
              {state.ok && ex.explain && (
                <div className="prose-py mt-1 text-[13px]" dangerouslySetInnerHTML={inline(ex.explain)} />
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

/* ------------------------------------------------------------------ 外壳 */
const KIND_LABEL = {
  predict: { icon: "🔮", name: "先猜一猜", tone: "bg-magic-50 text-magic-600" },
  fixbug: { icon: "🔧", name: "找找 bug", tone: "bg-sakura-50 text-sakura-500" },
  fill: { icon: "✏️", name: "补全它", tone: "bg-amberly-100 text-amberly-500" },
}

export default function Exercises({ exercises, doneIds, runSnippet, busy, onDone }) {
  const [open, setOpen] = useState(0)
  if (!exercises?.length) return null

  return (
    <div className="space-y-2">
      {exercises.map((ex, i) => {
        const label = KIND_LABEL[ex.type] || KIND_LABEL.predict
        const done = doneIds.includes(ex.id)
        const isOpen = open === i
        return (
          <div key={ex.id} className="card overflow-hidden">
            <button
              onClick={() => setOpen(isOpen ? -1 : i)}
              className="flex w-full items-center gap-2 px-3.5 py-2.5 text-left hover:bg-magic-50/60"
            >
              <span className={`chip ${label.tone}`}>
                {label.icon} {label.name}
              </span>
              {/* 回响题：来自前几天的知识点，间隔重复用 */}
              {ex.echo && (
                <span className="chip bg-magic-50 text-magic-600 ring-1 ring-magic-200">
                  🔁 回响 · Day {ex.echo}
                </span>
              )}
              <span className="flex-1 truncate text-[13px] text-ink-soft">{ex.title || ex.question}</span>
              {done && <span className="text-mint-600">✓</span>}
              <span className="text-ink-faint">{isOpen ? "▴" : "▾"}</span>
            </button>
            {isOpen && (
              <div className="border-t border-magic-100 p-3.5">
                {ex.type === "predict" ? (
                  <Predict ex={ex} done={done} onDone={() => onDone(ex.id)} />
                ) : (
                  <CodeTask
                    ex={ex}
                    runSnippet={runSnippet}
                    busy={busy}
                    done={done}
                    onDone={() => onDone(ex.id)}
                  />
                )}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
