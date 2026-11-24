import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { api } from "../lib/api"
import Mascot, { MascotSays } from "../components/Mascot"

const GREETING = [
  { hi: "今天也一起加油吧！(๑•̀ㅂ•́)و✧", mood: "happy" },
  { hi: "派森酱已经准备好今天的课啦～", mood: "excited" },
  { hi: "欢迎回来！上次的代码我帮你存着呢 ✨", mood: "wink" },
  { hi: "要不要来解锁新技能？", mood: "normal" },
]

const STAGE_NAME = { 1: "第一章 · 会说话" }

export default function Home() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [greet] = useState(() => GREETING[Math.floor(Math.random() * GREETING.length)])

  useEffect(() => {
    api.listDays().then(setData).catch((e) => setError(e.message))
  }, [])

  if (error) {
    return (
      <Wrap>
        <div className="card p-6 text-center">
          <Mascot mood="worried" size={96} className="mx-auto" />
          <p className="mt-3 font-bold">连不上后端 (｡•́︿•̀｡)</p>
          <p className="mt-1 text-[13.5px] text-ink-soft">{error}</p>
          <p className="mt-3 text-[13px] text-ink-faint">
            确认一下 <code className="rounded bg-magic-50 px-1">docker compose up</code> 起来了没？
          </p>
        </div>
      </Wrap>
    )
  }

  if (!data) {
    return (
      <Wrap>
        <div className="flex flex-col items-center py-24">
          <Mascot mood="sleepy" size={110} float />
          <p className="mt-3 text-ink-soft">正在整理课程表…</p>
        </div>
      </Wrap>
    )
  }

  const done = data.days.filter((d) => d.status === "done")
  const nextDay = data.days.find((d) => d.status !== "done") || data.days[data.days.length - 1]
  const pct = data.days.length ? Math.round((done.length / data.days.length) * 100) : 0

  return (
    <Wrap>
      {/* -------------------------------------------------------- 欢迎区 */}
      <header className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-magic-600">派森酱学院 ✨</h1>
          <p className="text-[13.5px] text-ink-soft">每天一个小项目，把 Python 一点点变成你的</p>
        </div>
        <Link to="/gallery" className="btn-ghost">
          🏆 作品陈列馆
        </Link>
      </header>

      <div className="card mb-5 p-5">
        <MascotSays mood={greet.mood} size={72}>
          <p className="text-[15px] font-semibold">{greet.hi}</p>
          <p className="mt-1 text-[13.5px] text-ink-soft">
            {done.length === 0
              ? "从第 1 天开始，今天只要 40 分钟就够了。"
              : `你已经完成 ${done.length} 天啦，下一站是 Day ${nextDay?.day}「${nextDay?.title}」。`}
          </p>
          {data.streak.current >= 2 && (
            <p className="mt-1 text-[13.5px] text-sakura-500">
              🔥 连续第 {data.streak.current} 天 —— 这个坚持度已经是 SSR 级别了！
            </p>
          )}
        </MascotSays>

        <div className="mt-4 grid grid-cols-2 gap-2.5 sm:grid-cols-4">
          <Stat label="已完成" value={`${done.length} 天`} tone="mint" />
          <Stat label="当前连击" value={`${data.streak.current} 天`} tone="sakura" />
          <Stat label="最长连击" value={`${data.streak.longest} 天`} tone="amber" />
          <Stat label="总进度" value={`${pct}%`} tone="magic" />
        </div>

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <Link to={`/day/${nextDay?.day || 1}`} className="btn-primary !px-5 !py-2.5 !text-[15px]">
            {done.length === 0 ? "开始第 1 天 →" : `继续 Day ${nextDay?.day} →`}
          </Link>
          <div className="h-2.5 min-w-[10rem] flex-1 overflow-hidden rounded-full bg-magic-100">
            <div
              className="h-full rounded-full bg-gradient-to-r from-magic-400 via-sakura-400 to-amberly-500 transition-all duration-700"
              style={{ width: `${pct}%` }}
            />
          </div>
        </div>
      </div>

      {/* -------------------------------------------------------- 日历格 */}
      <h2 className="mb-2.5 flex items-center gap-2 text-sm font-bold text-ink">
        <span>🗓</span>
        {STAGE_NAME[1]}
        <span className="chip bg-magic-50 text-magic-600">{data.days.length} 天</span>
      </h2>

      <div className="grid grid-cols-2 gap-2.5 sm:grid-cols-3 lg:grid-cols-5">
        {data.days.map((d) => (
          <DayCard key={d.day} d={d} />
        ))}
      </div>

      <p className="mt-8 text-center text-[12.5px] text-ink-faint">
        第一章之后还有六章在路上 —— 循环、列表、函数、文件、类、数据可视化。
        <br />
        先把这 10 天玩透，剩下的边学边加 🌱
      </p>
    </Wrap>
  )
}

function DayCard({ d }) {
  const doneState = d.status === "done"
  const opened = d.status === "opened"
  return (
    <Link
      to={`/day/${d.day}`}
      className={`group relative overflow-hidden rounded-2xl border p-3 transition hover:-translate-y-0.5 hover:shadow-card ${
        doneState
          ? "border-mint-500/40 bg-mint-100/70"
          : opened
            ? "border-amberly-500/40 bg-amberly-100/60"
            : "border-magic-100 bg-paper-card"
      }`}
    >
      <div className="flex items-start justify-between">
        <span
          className={`chip ${
            doneState ? "bg-mint-600 text-white" : opened ? "bg-amberly-500 text-white" : "bg-magic-50 text-magic-600"
          }`}
        >
          Day {d.day}
        </span>
        <span className="text-lg">{doneState ? "✅" : opened ? "✏️" : d.uses_turtle ? "🐢" : "🔒"}</span>
      </div>
      <h3 className="mt-2 text-[14px] font-bold leading-snug text-ink">{d.title}</h3>
      <p className="mt-0.5 line-clamp-2 text-[12px] leading-snug text-ink-soft">{d.hook}</p>
      <div className="mt-2 flex flex-wrap gap-1">
        {d.concepts.slice(0, 2).map((c) => (
          <span key={c} className="chip bg-white/70 text-[11px] text-ink-faint ring-1 ring-magic-100">
            {c}
          </span>
        ))}
      </div>
    </Link>
  )
}

function Stat({ label, value, tone }) {
  const tones = {
    mint: "bg-mint-100 text-mint-600",
    sakura: "bg-sakura-50 text-sakura-500",
    amber: "bg-amberly-100 text-amberly-500",
    magic: "bg-magic-50 text-magic-600",
  }
  return (
    <div className={`rounded-xl px-3 py-2 ${tones[tone]}`}>
      <div className="text-[11.5px] opacity-80">{label}</div>
      <div className="text-lg font-bold leading-tight">{value}</div>
    </div>
  )
}

function Wrap({ children }) {
  return <div className="mx-auto max-w-5xl px-4 py-8">{children}</div>
}
