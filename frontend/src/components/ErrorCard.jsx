import { useState } from "react"
import { Link } from "react-router-dom"
import { MascotSays } from "./Mascot"
import { md } from "../lib/markdown"

/** 一行里的 `代码` 和 **加粗** 也要能显示 */
const inline = (text) => ({
  __html: md(text).replace(/^<p>|<\/p>\n?$/g, ""),
})

export default function ErrorCard({ error, mascotLine, onJumpToLine }) {
  const [showRaw, setShowRaw] = useState(false)
  if (!error) return null

  return (
    <div className="card animate-pop border-sakura-200 bg-sakura-50/60 p-3.5">
      <MascotSays mood="worried" tone="sakura" size={52}>
        {mascotLine}
      </MascotSays>

      <div className="mt-3 rounded-xl border border-sakura-200 bg-white p-3.5">
        <div className="flex flex-wrap items-center gap-2">
          <h4 className="text-[15px] font-bold text-ink">{error.title}</h4>
          {error.line != null && (
            <button
              onClick={() => onJumpToLine?.(error.line)}
              className="chip bg-sakura-100 text-sakura-500 ring-1 ring-sakura-200 hover:bg-sakura-200"
              title="在编辑器里高亮这一行"
            >
              第 {error.line} 行
            </button>
          )}
        </div>

        <ul className="prose-py mt-2 space-y-1 text-[14px]">
          {error.lines.map((l, i) => (
            <li key={i} className="list-none" dangerouslySetInnerHTML={inline(l)} />
          ))}
        </ul>

        {error.code && (
          <div className="mt-3 grid gap-2 sm:grid-cols-2">
            <div>
              <div className="mb-1 text-xs font-bold text-sakura-500">✗ 会报错的写法</div>
              <pre className="overflow-x-auto rounded-lg border border-sakura-200 bg-sakura-50 p-2.5 font-mono text-[12.5px] leading-relaxed text-ink">
                {error.code.bad}
              </pre>
            </div>
            <div>
              <div className="mb-1 text-xs font-bold text-mint-600">✓ 这样就好了</div>
              <pre className="overflow-x-auto rounded-lg border border-mint-500/30 bg-mint-100 p-2.5 font-mono text-[12.5px] leading-relaxed text-ink">
                {error.code.good}
              </pre>
            </div>
          </div>
        )}

        <div className="mt-3 flex flex-wrap items-center gap-2">
          {error.concept && (
            <Link
              to={`/day/${error.concept.day}`}
              className="btn btn-sm border border-magic-200 bg-magic-50 text-magic-600"
            >
              📖 回去看看「{error.concept.name}」
            </Link>
          )}
          <button onClick={() => setShowRaw((v) => !v)} className="btn btn-sm btn-ghost">
            {showRaw ? "收起" : "看英文原文"}
          </button>
        </div>

        {showRaw && (
          <pre className="mt-2 overflow-x-auto rounded-lg bg-[#241C3B] p-2.5 font-mono text-[12px] leading-relaxed text-[#E8DEFF]">
            {error.raw}
          </pre>
        )}
      </div>
    </div>
  )
}
