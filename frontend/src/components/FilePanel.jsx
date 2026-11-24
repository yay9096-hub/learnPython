import { useState } from "react"
import Mascot from "./Mascot"

/**
 * 文件面板。
 *
 * 第五章开始，她的代码会真的往磁盘写文件。
 * 没有这个面板，「文件」对她就是个黑箱 —— 写进去了什么、存住没有，全靠想象。
 * 有了它，`open("日记.txt", "w")` 之后立刻能看见那个文件出现在列表里。
 */
function humanSize(n) {
  if (n < 1024) return `${n} B`
  return `${(n / 1024).toFixed(1)} KB`
}

export default function FilePanel({ files, persistent, onRefresh, onClear }) {
  const [openName, setOpenName] = useState(null)
  const [confirmClear, setConfirmClear] = useState(false)

  const list = files || []
  const opened = list.find((f) => f.name === openName)

  return (
    <div className="flex h-full flex-col">
      <div className="mb-2 flex shrink-0 items-center gap-2">
        <span className="chip bg-magic-50 text-magic-600">
          {list.length} 个文件
        </span>
        {persistent ? (
          <span className="chip bg-mint-100 text-mint-600" title="文件存在浏览器里，刷新和关机都还在">
            💾 会保存
          </span>
        ) : (
          <span className="chip bg-amberly-100 text-amberly-500" title="这个环境下文件只存在内存里">
            ⚠️ 刷新就没
          </span>
        )}
        <div className="flex-1" />
        <button onClick={onRefresh} className="btn btn-sm btn-ghost !px-2 !py-0.5">
          刷新
        </button>
        {list.length > 0 && (
          <button
            onClick={() => setConfirmClear(true)}
            className="btn btn-sm btn-ghost !px-2 !py-0.5 text-sakura-500"
          >
            清空
          </button>
        )}
      </div>

      {confirmClear && (
        <div className="animate-pop mb-2 shrink-0 rounded-xl border border-sakura-200 bg-sakura-50 p-2.5">
          <p className="text-[13px] text-ink">
            确定要删掉这 {list.length} 个文件吗？删了就找不回来了。
          </p>
          <div className="mt-2 flex gap-2">
            <button
              onClick={() => {
                setConfirmClear(false)
                setOpenName(null)
                onClear()
              }}
              className="btn btn-sm bg-sakura-500 text-white"
            >
              删掉
            </button>
            <button onClick={() => setConfirmClear(false)} className="btn btn-sm btn-ghost">
              算了
            </button>
          </div>
        </div>
      )}

      <div className="min-h-0 flex-1 overflow-auto">
        {list.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <Mascot mood="normal" size={56} />
            <p className="mt-2 text-[13px] text-ink-soft">还没有文件</p>
            <p className="mt-1 px-4 text-[12px] leading-relaxed text-ink-faint">
              代码里用 <code className="rounded bg-magic-50 px-1">open("日记.txt", "w")</code>{" "}
              写点东西，文件就会出现在这里
            </p>
          </div>
        ) : (
          <ul className="space-y-1">
            {list.map((f) => {
              const isOpen = openName === f.name
              return (
                <li key={f.name} className="overflow-hidden rounded-xl border border-magic-100">
                  <button
                    onClick={() => setOpenName(isOpen ? null : f.name)}
                    className="flex w-full items-center gap-2 bg-paper-sunken/50 px-2.5 py-1.5 text-left hover:bg-magic-50"
                  >
                    <span>{f.dir ? "📁" : "📄"}</span>
                    <span className="flex-1 truncate font-mono text-[12.5px] text-ink">
                      {f.name}
                    </span>
                    <span className="shrink-0 text-[11px] text-ink-faint">
                      {f.dir ? "" : humanSize(f.size)}
                    </span>
                    {!f.dir && <span className="text-ink-faint">{isOpen ? "▴" : "▾"}</span>}
                  </button>
                  {isOpen && !f.dir && (
                    <pre className="max-h-56 overflow-auto whitespace-pre-wrap break-words border-t border-magic-100 bg-[#241C3B] p-2.5 font-mono text-[12px] leading-relaxed text-[#E8DEFF]">
                      {f.text === null
                        ? "（文件太大了，这里就不显示了）"
                        : f.text || "（空文件）"}
                    </pre>
                  )}
                </li>
              )
            })}
          </ul>
        )}
      </div>

      {opened && !opened.dir && (
        <p className="mt-2 shrink-0 text-[11.5px] text-ink-faint">
          💡 这是文件真正的内容 —— 关掉浏览器再回来，它还在这里。
        </p>
      )}
    </div>
  )
}
