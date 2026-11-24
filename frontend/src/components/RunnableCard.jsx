import { useState } from "react"
import CodeEditor from "./CodeEditor"

/**
 * 讲解里的「可运行知识卡」。
 * 读到的每一句都能立刻验证 —— 这是整个讲解区最有效的设计。
 * 代码可以随手改，改坏了一键还原。
 */
export default function RunnableCard({ caption, code, runSnippet, busy }) {
  const [src, setSrc] = useState(code)
  const [out, setOut] = useState(null)
  const [running, setRunning] = useState(false)

  const lines = src.split("\n").length
  const dirty = src !== code

  const go = async () => {
    setRunning(true)
    setOut(null)
    try {
      const r = await runSnippet(src)
      setOut(r)
    } catch (e) {
      setOut({ text: String(e.message || e), error: true })
    } finally {
      setRunning(false)
    }
  }

  return (
    <div className="my-3 overflow-hidden rounded-2xl border border-magic-200 bg-white shadow-card">
      <div className="flex items-center justify-between gap-2 border-b border-magic-100 bg-magic-50 px-3 py-1.5">
        <span className="flex items-center gap-1.5 text-[12.5px] font-bold text-magic-600">
          <span>🧪</span>
          {caption || "试一下"}
        </span>
        <div className="flex items-center gap-1.5">
          {dirty && (
            <button onClick={() => setSrc(code)} className="btn btn-sm btn-ghost !px-2 !py-0.5">
              还原
            </button>
          )}
          <button
            onClick={go}
            disabled={running || busy}
            className="btn btn-sm bg-magic-500 !px-2.5 !py-0.5 text-white"
          >
            {running ? "…" : "▶ 试一下"}
          </button>
        </div>
      </div>

      <div style={{ height: Math.min(Math.max(lines, 2), 12) * 26 + 14 }}>
        <CodeEditor value={src} onChange={setSrc} onRunShortcut={go} />
      </div>

      {out && (
        <div
          className={`animate-pop border-t border-magic-100 px-3 py-2 font-mono text-[12.5px] leading-relaxed ${
            out.error ? "bg-sakura-50 text-sakura-500" : "bg-[#241C3B] text-[#E8DEFF]"
          }`}
        >
          <div className="mb-0.5 select-none text-[11px] opacity-60">输出</div>
          <pre className="whitespace-pre-wrap break-words">{out.text || "（这段代码没有输出）"}</pre>
        </div>
      )}
    </div>
  )
}
