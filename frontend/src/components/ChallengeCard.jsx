import { useState } from "react"
import Mascot from "./Mascot"

/**
 * 挑战关。主线全部通过之后才出现，**不计入完成条件**。
 *
 * 存在的理由：她一天能做完四天的内容，说明主线对她偏轻。
 * 与其把主线拔高吓退别人，不如给「还想再玩会儿」的人留一个出口。
 */
export default function ChallengeCard({ challenge, unlocked }) {
  const [open, setOpen] = useState(false)
  if (!challenge?.title) return null

  if (!unlocked) {
    return (
      <div className="card border-dashed border-magic-200 bg-paper-sunken/50 p-3">
        <div className="flex items-center gap-2 text-[13px] text-ink-faint">
          <span>🔒</span>
          <span>
            完成今天的全部任务后，解锁 <strong>挑战关</strong>
          </span>
        </div>
      </div>
    )
  }

  return (
    <div className="card animate-pop border-amberly-500/50 bg-amberly-100/60 p-3.5">
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center gap-2 text-left"
      >
        <span className="chip bg-amberly-500 text-white">🔥 挑战关</span>
        <span className="flex-1 truncate text-[13.5px] font-bold text-ink">
          {challenge.title}
        </span>
        <span className="text-ink-faint">{open ? "▴" : "▾"}</span>
      </button>

      {open && (
        <div className="mt-3 flex items-start gap-2.5">
          <Mascot mood="excited" size={44} className="shrink-0" />
          <div className="flex-1 rounded-xl bg-white/70 p-2.5">
            <p className="text-[13.5px] leading-relaxed text-ink">{challenge.desc}</p>
            <p className="mt-2 text-[12px] text-ink-faint">
              挑战关不影响今天的完成状态 —— 做不做都行，纯粹给还想玩的人 ✨
            </p>
          </div>
        </div>
      )}
    </div>
  )
}
