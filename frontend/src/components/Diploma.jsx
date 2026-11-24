import { useEffect, useState } from "react"
import Mascot from "./Mascot"

/**
 * 结业证书。
 *
 * 只在 Day 70（meta.graduation）通关时出现，替代平时的通关弹窗。
 * 70 天走到这里不容易，值得一个像样的仪式。
 */
function Sparkle({ delay, left, top }) {
  return (
    <span
      className="pointer-events-none absolute animate-sparkle text-amberly-500"
      style={{ left, top, animationDelay: delay }}
    >
      ✦
    </span>
  )
}

export default function Diploma({ stats, onClose, onGallery }) {
  const [shown, setShown] = useState(false)
  useEffect(() => {
    const t = setTimeout(() => setShown(true), 80)
    return () => clearTimeout(t)
  }, [])

  const days = stats?.done ?? 70
  const minutes = stats?.minutes ?? 0
  const hours = Math.round((minutes / 60) * 10) / 10
  const longest = stats?.longest ?? 0

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center overflow-auto bg-ink/50 p-4 backdrop-blur-sm">
      <div
        className={`relative w-full max-w-lg transition-all duration-500 ${
          shown ? "scale-100 opacity-100" : "scale-90 opacity-0"
        }`}
      >
        {/* 外层金边 */}
        <div className="rounded-3xl bg-gradient-to-br from-amberly-500 via-sakura-400 to-magic-500 p-[3px] shadow-card">
          <div className="relative overflow-hidden rounded-3xl bg-paper-card px-7 py-8 text-center">
            <Sparkle delay="0s" left="8%" top="12%" />
            <Sparkle delay="0.4s" left="88%" top="18%" />
            <Sparkle delay="0.8s" left="14%" top="78%" />
            <Sparkle delay="1.2s" left="84%" top="72%" />

            <p className="text-[12px] tracking-[0.4em] text-ink-faint">
              PYSON ACADEMY
            </p>
            <h2 className="mt-1 text-2xl font-bold text-magic-600">结业证书</h2>
            <div className="mx-auto mt-2 h-px w-24 bg-gradient-to-r from-transparent via-magic-200 to-transparent" />

            <Mascot mood="excited" size={110} className="mx-auto mt-3" float />

            <p className="mt-3 text-[15px] leading-relaxed text-ink">
              兹证明该同学已完成
              <br />
              <strong className="text-magic-600">派森酱学院 · 70 天 Python 修行</strong>
            </p>

            <div className="mt-4 grid grid-cols-3 gap-2">
              <div className="rounded-xl bg-mint-100 px-2 py-2">
                <div className="text-[11px] text-mint-600">完成</div>
                <div className="text-lg font-bold text-mint-600">{days} 天</div>
              </div>
              <div className="rounded-xl bg-sakura-50 px-2 py-2">
                <div className="text-[11px] text-sakura-500">投入</div>
                <div className="text-lg font-bold text-sakura-500">{hours} 小时</div>
              </div>
              <div className="rounded-xl bg-amberly-100 px-2 py-2">
                <div className="text-[11px] text-amberly-500">最长连击</div>
                <div className="text-lg font-bold text-amberly-500">{longest} 天</div>
              </div>
            </div>

            <div className="mt-4 rounded-2xl border border-magic-100 bg-magic-50/60 px-4 py-3 text-left">
              <p className="text-[13.5px] leading-relaxed text-ink">
                「70 天前你问『这个 print 是什么意思』。
                <br />
                今天你在设计自己的软件。
                <br />
                <br />
                我一直在这儿看着 —— <strong className="text-magic-600">你真的很厉害。</strong>」
              </p>
              <p className="mt-2 text-right text-[12.5px] text-ink-soft">
                —— 派森酱 (๑˃̵ᴗ˂̵)و ✨
              </p>
            </div>

            <div className="mt-5 flex justify-center gap-2">
              <button onClick={onGallery} className="btn-ghost">
                🏆 看作品陈列馆
              </button>
              <button onClick={onClose} className="btn-primary">
                收下证书
              </button>
            </div>

            <p className="mt-4 text-[11.5px] text-ink-faint">
              这不是终点 —— 接下来想学什么，你已经有能力自己去学了 🌱
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
