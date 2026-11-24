import { marked } from "marked"

marked.setOptions({ breaks: true, gfm: true })

export const md = (text) => marked.parse(text || "")

/**
 * 把 lesson.md 拆成「普通 markdown」和「可运行知识卡」两种片段。
 *
 * 知识卡写法（三个反引号）：
 *   python runnable 变量就是一个盒子
 *   name = "小樱"
 *   print(name)
 *
 * 渲染成一张带 [▶ 试一下] 按钮的卡片 —— 读到的每一句都能立刻验证，
 * 这是整个讲解区最有效的设计。
 */
const FENCE = /^```python\s+runnable[ \t]*(.*)$/

export function parseLesson(source) {
  const lines = (source || "").split("\n")
  const blocks = []
  let buf = []
  let i = 0

  const flush = () => {
    const text = buf.join("\n")
    if (text.trim()) blocks.push({ kind: "md", text })
    buf = []
  }

  while (i < lines.length) {
    const m = lines[i].match(FENCE)
    if (m) {
      flush()
      const caption = m[1].trim()
      const code = []
      i++
      while (i < lines.length && !lines[i].startsWith("```")) {
        code.push(lines[i])
        i++
      }
      i++ // 吃掉结尾的 ```
      blocks.push({ kind: "runnable", caption, code: code.join("\n") })
      continue
    }
    buf.push(lines[i])
    i++
  }
  flush()
  return blocks
}
