import { useEffect, useRef } from "react"
import { EditorState, StateEffect, StateField } from "@codemirror/state"
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter, Decoration } from "@codemirror/view"
import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands"
import { python } from "@codemirror/lang-python"
import { bracketMatching, indentUnit, syntaxHighlighting, defaultHighlightStyle } from "@codemirror/language"
import { closeBrackets, closeBracketsKeymap, autocompletion } from "@codemirror/autocomplete"

/* 出错的那一行整行标红 —— 比让她自己去数行号友好得多 */
const setErrorLine = StateEffect.define()
const errorLineField = StateField.define({
  create: () => Decoration.none,
  update(deco, tr) {
    deco = deco.map(tr.changes)
    for (const e of tr.effects) {
      if (!e.is(setErrorLine)) continue
      if (!e.value) return Decoration.none
      const total = tr.state.doc.lines
      const n = Math.min(Math.max(1, e.value), total)
      const line = tr.state.doc.line(n)
      deco = Decoration.set([Decoration.line({ class: "cm-error-line" }).range(line.from)])
    }
    // 一改代码就把红线撤掉，别一直挂着吓人
    if (tr.docChanged) return Decoration.none
    return deco
  },
  provide: (f) => EditorView.decorations.from(f),
})

export default function CodeEditor({ value, onChange, errorLine = null, readOnly = false, onRunShortcut }) {
  const host = useRef(null)
  const view = useRef(null)
  const onChangeRef = useRef(onChange)
  const onRunRef = useRef(onRunShortcut)
  onChangeRef.current = onChange
  onRunRef.current = onRunShortcut

  useEffect(() => {
    if (!host.current) return

    const runKey = keymap.of([
      {
        key: "Ctrl-Enter",
        mac: "Cmd-Enter",
        run: () => {
          onRunRef.current?.()
          return true
        },
      },
    ])

    const state = EditorState.create({
      doc: value ?? "",
      extensions: [
        lineNumbers(),
        history(),
        highlightActiveLine(),
        highlightActiveLineGutter(),
        bracketMatching(),
        closeBrackets(),
        autocompletion({ activateOnTyping: false }), // 小白阶段不要弹一堆看不懂的提示
        python(),
        syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
        indentUnit.of("    "),
        errorLineField,
        runKey,
        keymap.of([...closeBracketsKeymap, ...defaultKeymap, ...historyKeymap, indentWithTab]),
        EditorView.lineWrapping,
        EditorState.readOnly.of(readOnly),
        EditorView.updateListener.of((u) => {
          if (u.docChanged) onChangeRef.current?.(u.state.doc.toString())
        }),
      ],
    })

    view.current = new EditorView({ state, parent: host.current })
    return () => {
      view.current?.destroy()
      view.current = null
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // 外部改了内容（读档 / 重置 / 载入答案）才覆盖，避免打字被打断
  useEffect(() => {
    const v = view.current
    if (!v) return
    const cur = v.state.doc.toString()
    if (value !== undefined && value !== cur) {
      v.dispatch({ changes: { from: 0, to: cur.length, insert: value ?? "" } })
    }
  }, [value])

  useEffect(() => {
    view.current?.dispatch({ effects: setErrorLine.of(errorLine) })
  }, [errorLine])

  return <div ref={host} className="h-full overflow-hidden" />
}
