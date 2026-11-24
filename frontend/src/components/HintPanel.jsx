import { useState } from "react"
import { md } from "../lib/markdown"
import Mascot from "./Mascot"

const TEASE = [
  "要不要……派森酱悄悄告诉你一点点？(◍•ᴗ•◍)",
  "卡住了？我这里有三级提示，一级一级来～",
  "先自己想 5 分钟哦，实在不行我再开口！",
]

/**
 * 分级提示：思路 → 伪代码 → 关键代码。
 * 参考答案单独一档，需要二次确认 —— 让「看答案」有一点心理成本，
 * 但绝不封死，卡太久却看不到答案只会让人放弃。
 */
export default function HintPanel({ hints, onReveal, onWantSolution, solutionSeen }) {
  const [level, setLevel] = useState(0)
  const [confirming, setConfirming] = useState(false)
  const [tease] = useState(() => TEASE[Math.floor(Math.random() * TEASE.length)])

  const reveal = () => {
    const next = level + 1
    setLevel(next)
    onReveal?.(next)
  }

  return (
    <div className="card p-3.5">
      <div className="mb-2 flex items-center justify-between">
        <h3 className="flex items-center gap-1.5 text-sm font-bold text-ink">
          <span>💡</span> 提示
        </h3>
        <span className="chip bg-magic-50 text-magic-600">
          {level} / {hints.length}
        </span>
      </div>

      {level === 0 && (
        <div className="flex items-start gap-2 rounded-xl bg-paper-sunken/70 p-2.5">
          <Mascot mood="wink" size={40} className="shrink-0" />
          <p className="mt-1 text-[13px] leading-relaxed text-ink-soft">{tease}</p>
        </div>
      )}

      <div className="mt-2 space-y-2">
        {hints.slice(0, level).map((h, i) => (
          <div key={i} className="animate-pop rounded-xl border border-magic-100 bg-magic-50/60 p-2.5">
            <div className="mb-1 text-[12.5px] font-bold text-magic-600">
              {i + 1}. {h.title}
            </div>
            <div
              className="prose-py text-[13.5px] [&_pre]:my-2 [&_pre]:py-2.5"
              dangerouslySetInnerHTML={{ __html: md(h.body) }}
            />
          </div>
        ))}
      </div>

      <div className="mt-2.5 flex flex-wrap gap-2">
        {level < hints.length && (
          <button onClick={reveal} className="btn btn-sm border border-magic-200 bg-white text-magic-600">
            {level === 0 ? "给我一点提示" : `再来一点（第 ${level + 1} 级）`}
          </button>
        )}

        {level >= hints.length && !confirming && (
          <button onClick={() => setConfirming(true)} className="btn btn-sm btn-ghost">
            {solutionSeen ? "再看一次参考答案" : "我想看参考答案"}
          </button>
        )}
      </div>

      {confirming && (
        <div className="mt-2.5 animate-pop rounded-xl border border-amberly-500/40 bg-amberly-100 p-2.5">
          <p className="text-[13px] leading-relaxed text-ink">
            答案会直接出现在编辑器旁边哦。
            <br />
            <strong className="text-magic-600">看完之后，还是要自己敲一遍才算通过～</strong>
          </p>
          <div className="mt-2 flex gap-2">
            <button
              onClick={() => {
                setConfirming(false)
                onWantSolution?.()
              }}
              className="btn btn-sm bg-amberly-500 text-white"
            >
              嗯，给我看
            </button>
            <button onClick={() => setConfirming(false)} className="btn btn-sm btn-ghost">
              再想想
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
