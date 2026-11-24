import { md } from "../lib/markdown"

const inline = (t) => ({ __html: md(t || "").replace(/^<p>|<\/p>\n?$/g, "") })

/**
 * 任务清单。没过的项**必须**给出具体哪里不对（check 的 fail 字段），
 * 只写「测试 3 失败」是最容易让人放弃的做法。
 */
export default function TaskList({ tasks, results, notes, judging }) {
  const byId = new Map((results || []).map((r) => [r.id, r]))
  const total = tasks.length
  const passed = (results || []).filter((r) => r.passed).length

  return (
    <div className="card p-3.5">
      <div className="mb-2.5 flex items-center justify-between">
        <h3 className="flex items-center gap-1.5 text-sm font-bold text-ink">
          <span>✅</span> 今日任务
        </h3>
        <span
          className={`chip ${
            results?.length && passed === total
              ? "bg-mint-100 text-mint-600"
              : "bg-magic-50 text-magic-600"
          }`}
        >
          {results?.length ? `${passed} / ${total}` : `共 ${total} 项`}
        </span>
      </div>

      {/* 残留的清空语句 —— 输出看着全对、判题却红，最难自己发现的一种错 */}
      {!judging && notes?.length > 0 && (
        <div className="animate-pop mb-2.5 rounded-xl border border-amberly-500/40 bg-amberly-100 px-2.5 py-2">
          <div className="text-[13px] font-bold text-ink">🔍 等一下，我发现一件事</div>
          {notes.map((n) => (
            <p key={`${n.name}-${n.line}`} className="mt-1 text-[12.5px] leading-relaxed text-ink-soft">
              第 <strong className="text-amberly-500">{n.line}</strong> 行有一句{" "}
              <code className="rounded bg-white/70 px-1 font-mono">{n.name} = 空的</code>
              ，它在你算完之后又把 <code className="font-mono">{n.name}</code> 清空了，
              而且后面再没用过它。
              <br />
              你的输出是对的（因为打印在前面），但程序跑到最后它已经变回空的了 ——
              <strong>多半是 starter 里的 TODO 没删干净</strong>。把那一行删掉试试 ✨
            </p>
          ))}
        </div>
      )}

      <ul className="space-y-1.5">
        {tasks.map((t, i) => {
          const r = byId.get(t.id)
          const state = judging ? "pending" : !r ? "idle" : r.passed ? "pass" : "fail"
          return (
            <li
              key={t.id || i}
              className={`rounded-xl border px-2.5 py-2 transition ${
                state === "pass"
                  ? "border-mint-500/40 bg-mint-100/70"
                  : state === "fail"
                    ? "border-sakura-200 bg-sakura-50"
                    : "border-magic-100 bg-paper-sunken/60"
              }`}
            >
              <div className="flex items-start gap-2">
                <span className="mt-0.5 w-4 shrink-0 text-center text-[13px]">
                  {state === "pass" ? "✅" : state === "fail" ? "🔸" : state === "pending" ? "⏳" : "☐"}
                </span>
                <span
                  className={`text-[13.5px] leading-snug ${
                    state === "pass" ? "text-mint-600 line-through decoration-mint-600/40" : "text-ink"
                  }`}
                >
                  {t.desc}
                </span>
              </div>
              {state === "fail" && r.fail && (
                <div
                  className="prose-py mt-1.5 rounded-lg bg-white/70 px-2 py-1.5 pl-7 text-[12.5px] text-ink-soft"
                  dangerouslySetInnerHTML={inline(r.fail)}
                />
              )}
            </li>
          )
        })}
      </ul>
    </div>
  )
}
