import { useMemo } from "react"
import { md, parseLesson } from "../lib/markdown"
import RunnableCard from "./RunnableCard"

export default function LessonPanel({ source, runSnippet, busy }) {
  const blocks = useMemo(() => parseLesson(source), [source])

  return (
    <div className="prose-py">
      {blocks.map((b, i) =>
        b.kind === "runnable" ? (
          <RunnableCard key={i} caption={b.caption} code={b.code} runSnippet={runSnippet} busy={busy} />
        ) : (
          <div key={i} dangerouslySetInnerHTML={{ __html: md(b.text) }} />
        ),
      )}
    </div>
  )
}
