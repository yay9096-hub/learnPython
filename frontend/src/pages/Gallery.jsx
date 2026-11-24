import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import { api } from "../lib/api"
import Mascot, { MascotSays } from "../components/Mascot"

/**
 * 作品陈列馆。
 * 「能把做出来的东西给爸爸看」这件事，对动力的贡献比任何徽章都大。
 */
export default function Gallery() {
  const [data, setData] = useState(null)

  useEffect(() => {
    api.gallery().then(setData).catch(() => setData({ works: [], streak: {} }))
  }, [])

  const works = data?.works || []

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <header className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-bold text-magic-600">🏆 作品陈列馆</h1>
          <p className="text-[13.5px] text-ink-soft">你亲手写出来的每一个程序，都在这里</p>
        </div>
        <Link to="/" className="btn-ghost">
          ← 回首页
        </Link>
      </header>

      {!data ? (
        <div className="flex flex-col items-center py-20">
          <Mascot mood="sleepy" size={96} float />
          <p className="mt-3 text-ink-soft">正在把作品搬出来…</p>
        </div>
      ) : works.length === 0 ? (
        <div className="card p-6">
          <MascotSays mood="normal" size={72}>
            <p className="font-semibold">这里还空着呢～</p>
            <p className="mt-1 text-[13.5px] text-ink-soft">
              完成任意一天的全部任务，作品就会自动挂到墙上。
            </p>
            <Link to="/day/1" className="btn-primary mt-3">
              去做第 1 天 →
            </Link>
          </MascotSays>
        </div>
      ) : (
        <>
          <div className="card mb-5 p-4">
            <MascotSays mood="excited" size={64} tone="mint">
              <p className="font-semibold">已经有 {works.length} 件作品了！</p>
              <p className="mt-1 text-[13.5px] text-ink-soft">
                每一件都是从空白文件开始，一行一行敲出来的 ✨
              </p>
            </MascotSays>
          </div>

          <div className="grid gap-3 sm:grid-cols-2">
            {works.map((w) => (
              <article key={w.day} className="card overflow-hidden">
                <div className="flex items-center gap-2 border-b border-magic-100 bg-magic-50/60 px-3.5 py-2">
                  <span className="chip bg-magic-500 text-white">Day {w.day}</span>
                  <h3 className="truncate text-[14px] font-bold text-ink">{w.title}</h3>
                  <div className="flex-1" />
                  <span className="text-[11.5px] text-ink-faint">
                    {(w.created_at || "").slice(0, 10)}
                  </span>
                </div>

                {w.image ? (
                  <img
                    src={w.image}
                    alt={w.title}
                    className="max-h-64 w-full bg-white object-contain"
                  />
                ) : (
                  <pre className="max-h-64 overflow-auto whitespace-pre-wrap break-words bg-[#241C3B] p-3.5 font-mono text-[12.5px] leading-relaxed text-[#E8DEFF]">
                    {w.snippet?.trim() || "（这一天的作品没有文字输出）"}
                  </pre>
                )}

                <div className="flex items-center justify-between px-3.5 py-2">
                  <p className="truncate text-[12.5px] text-ink-soft">{w.hook}</p>
                  <Link to={`/day/${w.day}`} className="btn btn-sm btn-ghost shrink-0">
                    再看看
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
