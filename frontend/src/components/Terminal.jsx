import { useEffect, useRef, useState } from "react"

/**
 * 输出终端。等待 input() 时会在最后一行长出一个输入框，
 * 提交之后这一行由 Python 那边写回 stdout，所以这里的临时提示要撤掉。
 */
export default function Terminal({ chunks, waitingPrompt, onSubmitInput, running }) {
  const [draft, setDraft] = useState("")
  const boxRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    boxRef.current?.scrollTo({ top: boxRef.current.scrollHeight, behavior: "smooth" })
  }, [chunks, waitingPrompt])

  useEffect(() => {
    if (waitingPrompt !== null) inputRef.current?.focus()
  }, [waitingPrompt])

  const submit = (e) => {
    e?.preventDefault()
    onSubmitInput(draft)
    setDraft("")
  }

  const empty = chunks.length === 0 && waitingPrompt === null && !running

  return (
    <div
      ref={boxRef}
      className="h-full overflow-auto rounded-xl bg-[#241C3B] px-3.5 py-3 font-mono text-[13.5px] leading-[1.7] text-[#E8DEFF]"
    >
      {empty && (
        <div className="select-none text-[#7A6BA8]">
          点上面的 <span className="text-magic-400">▶ 运行</span> 看看会发生什么～
          <div className="mt-1 text-[12px]">（快捷键 Ctrl + Enter）</div>
        </div>
      )}

      {chunks.map((c, i) => (
        <pre
          key={i}
          className={`whitespace-pre-wrap break-words ${
            c.kind === "stderr" ? "text-sakura-400" : ""
          }`}
        >
          {c.text}
        </pre>
      ))}

      {waitingPrompt !== null && (
        <form onSubmit={submit} className="flex flex-wrap items-center gap-1">
          <span className="whitespace-pre-wrap text-amberly-500">{waitingPrompt}</span>
          <input
            ref={inputRef}
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            // 表单的隐式提交在某些场景下不触发，这里显式接一下回车
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault()
                submit()
              }
            }}
            className="min-w-[8rem] flex-1 border-b border-magic-400 bg-transparent font-mono text-[#FFE9A8] caret-magic-400 outline-none"
            placeholder="在这里打字，按回车"
            autoComplete="off"
            spellCheck={false}
          />
          <button type="submit" className="btn btn-sm bg-magic-500 text-white">
            回车 ↵
          </button>
        </form>
      )}

      {running && waitingPrompt === null && (
        <div className="mt-1 flex items-center gap-2 text-[#9B87D4]">
          <span className="inline-block h-2 w-2 animate-ping rounded-full bg-magic-400" />
          运行中…
        </div>
      )}
    </div>
  )
}
