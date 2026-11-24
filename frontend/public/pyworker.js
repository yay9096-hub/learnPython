/* eslint-env worker */
/**
 * Pyodide 运行在 Web Worker 里：
 *  - 学生写死循环最多卡住这个 worker，主线程点「停止」直接 terminate 重建
 *  - input() 用 SharedArrayBuffer + Atomics.wait 实现真正的阻塞式输入
 *    （需要 COOP/COEP 响应头，nginx.conf 和 vite.config.js 里都配好了）
 */
importScripts('/pyodide/pyodide.js')

let py = null
let ctrl = null // Int32Array: [0]=信号量, [1]=输入字节数
let inbuf = null // Uint8Array
let outChars = 0
let fsReady = false // 持久化文件系统挂上了没
let plotReady = false // matplotlib 载入了没（第一次用到才载，省启动时间）

// 学生代码读写文件的目录。挂在 IDBFS 上 = 存进浏览器的 IndexedDB，
// 刷新页面、关掉浏览器都还在。第五章「文件」整章都靠它。
const WORK_DIR = '/home/pyodide/files'
const MAX_PREVIEW = 20000

const OUTPUT_CAP = 200000 // 防止死循环 print 把浏览器打爆

const post = (msg) => self.postMessage(msg)

function emit(kind, text) {
  outChars += text.length
  if (outChars > OUTPUT_CAP) {
    post({ type: 'overflow' })
    throw new Error('__OUTPUT_OVERFLOW__')
  }
  post({ type: kind, text })
}

/** 同步阻塞：通知主线程要输入，然后原地等，直到主线程写回数据 */
function blockingInput(prompt) {
  if (!ctrl) throw new Error('这个环境暂时不支持交互输入')
  Atomics.store(ctrl, 0, 0)
  Atomics.store(ctrl, 1, 0)
  post({ type: 'input', prompt: String(prompt ?? '') })
  Atomics.wait(ctrl, 0, 0)
  const len = Atomics.load(ctrl, 1)
  if (len < 0) throw new Error('__INPUT_CANCELLED__')
  return new TextDecoder().decode(inbuf.slice(0, len))
}

async function boot() {
  py = await self.loadPyodide({ indexURL: '/pyodide/' })
  py.setStdout({ batched: (s) => emit('stdout', s) })
  py.setStderr({ batched: (s) => emit('stderr', s) })

  const [runtimeSrc, judgeSrc, turtleSrc] = await Promise.all(
    ['/py/runtime.py', '/py/judge.py', '/py/turtle_shim.py'].map((u) =>
      fetch(u).then((r) => r.text()),
    ),
  )
  py.FS.writeFile('/home/pyodide/runtime.py', runtimeSrc, { encoding: 'utf8' })
  py.FS.writeFile('/home/pyodide/judge.py', judgeSrc, { encoding: 'utf8' })
  py.runPython('import sys; sys.path.insert(0, "/home/pyodide")')
  py.runPython('import runtime, judge')

  py.globals.set('__turtle_src', turtleSrc)
  py.runPython('runtime.install_turtle(__turtle_src)')
  py.globals.set('__js_input', blockingInput)
  py.runPython('runtime.set_js_input(__js_input)')

  await initFS()

  post({ type: 'ready', interactive: !!ctrl, persistent: fsReady })
  post({ type: 'files', data: listFiles() })
}

/** 挂上 IDBFS 并把之前存的文件读回来 */
async function initFS() {
  try {
    py.FS.mkdirTree(WORK_DIR)
    py.FS.mount(py.FS.filesystems.IDBFS, {}, WORK_DIR)
    await new Promise((resolve, reject) => {
      py.FS.syncfs(true, (err) => (err ? reject(err) : resolve()))
    })
    fsReady = true
  } catch (e) {
    // 挂不上也不让整个网站挂掉，只是文件不持久而已
    console.warn('[fs] IDBFS 挂载失败，文件将只存在内存里：', e)
    fsReady = false
  }
  // 把工作目录切过去，这样 open("日记.txt", "w") 直接写在持久化目录里
  py.runPython(`import os
os.chdir(${JSON.stringify(WORK_DIR)})`)
}

/**
 * 按需载入 matplotlib。
 *
 * 12MB 的 wheel 每次启动都载太浪费，所以只在代码里真的出现
 * matplotlib / numpy 时才载，而且只载一次。
 */
async function ensurePlotting(code) {
  if (plotReady) return
  if (!/\b(matplotlib|pyplot|numpy)\b/.test(code)) return

  post({ type: 'stdout', text: '（第一次画图，正在载入绘图库…）\n' })
  await py.loadPackage(['matplotlib'])

  // Agg 后端只画到内存缓冲区，不需要浏览器画布 ——
  // 我们自己把图取成 PNG 发给主线程显示。
  py.runPython([
    'import matplotlib',
    'matplotlib.use("AGG")',
    'import matplotlib.pyplot as plt',
    'plt.rcParams["font.sans-serif"] = ["DejaVu Sans"]',
    'plt.rcParams["axes.unicode_minus"] = False',
  ].join('\n'))
  plotReady = true
}

/** 如果学生代码画了图，把它取出来变成 PNG dataURL */
function grabPlot() {
  if (!plotReady) return null
  try {
    return py.runPython(`
import base64, io as _io
import matplotlib.pyplot as _plt
_figs = _plt.get_fignums()
if not _figs:
    _out = None
else:
    _buf = _io.BytesIO()
    _plt.savefig(_buf, format="png", dpi=110, bbox_inches="tight")
    _plt.close("all")
    _out = "data:image/png;base64," + base64.b64encode(_buf.getvalue()).decode()
_out
`)
  } catch (e) {
    console.warn('[plot] 取图失败：', e)
    return null
  }
}

/** 把内存里的改动写回 IndexedDB。每次运行结束都要调。 */
async function saveFS() {
  if (!fsReady) return
  await new Promise((resolve) => py.FS.syncfs(false, () => resolve()))
}

/** 列出工作目录里的文件，附带小文件的内容预览 */
function listFiles() {
  const out = []
  let names = []
  try {
    names = py.FS.readdir(WORK_DIR)
  } catch {
    return out
  }
  for (const name of names) {
    if (name === '.' || name === '..') continue
    const path = WORK_DIR + '/' + name
    let stat
    try {
      stat = py.FS.stat(path)
    } catch {
      continue
    }
    if (py.FS.isDir(stat.mode)) {
      out.push({ name, dir: true, size: 0, text: null })
      continue
    }
    let text = null
    if (stat.size <= MAX_PREVIEW) {
      try {
        text = new TextDecoder().decode(py.FS.readFile(path))
      } catch {
        text = '（这个文件不是文本，没法预览）'
      }
    }
    out.push({ name, dir: false, size: stat.size, text })
  }
  out.sort((a, b) => a.name.localeCompare(b.name))
  return out
}

function runUser(code, presetStdin) {
  outChars = 0
  py.globals.set('__code', code)
  py.globals.set('__stdin', presetStdin ? py.toPy(presetStdin) : null)
  const raw = py.runPython(`
import json, runtime
__ns, __err = runtime.run_user_code(__code, preset_stdin=__stdin)
json.dumps({"error": __err, "turtle": runtime.turtle_dump()}, ensure_ascii=False, default=str)
`)
  return JSON.parse(raw)
}

self.onmessage = async (e) => {
  const msg = e.data
  try {
    if (msg.type === 'init') {
      ctrl = msg.ctrl || null
      inbuf = msg.inbuf || null
      await boot()
      return
    }

    if (msg.type === 'run') {
      await ensurePlotting(msg.code)
      const { error, turtle } = runUser(msg.code, msg.stdin ?? null)
      post({ type: 'turtle', data: turtle })
      const plot = grabPlot()
      if (plot) post({ type: 'plot', data: plot })
      await saveFS()
      post({ type: 'files', data: listFiles() })
      post({ type: 'done', id: msg.id, error })
      return
    }

    if (msg.type === 'writeFile') {
      // 主线程往学生的工作目录里塞一个文件（Day 65 用它注入真实学习记录）
      py.FS.writeFile(WORK_DIR + '/' + msg.name, msg.text, { encoding: 'utf8' })
      await saveFS()
      post({ type: 'files', data: listFiles() })
      return
    }

    if (msg.type === 'listFiles') {
      post({ type: 'files', data: listFiles() })
      return
    }

    if (msg.type === 'clearFiles') {
      for (const f of listFiles()) {
        try {
          py.FS.unlink(WORK_DIR + '/' + f.name)
        } catch { /* 目录之类删不掉就算了 */ }
      }
      await saveFS()
      post({ type: 'files', data: listFiles() })
      return
    }

    if (msg.type === 'judge') {
      await ensurePlotting(msg.code)
      py.globals.set('__code', msg.code)
      py.globals.set('__tests', msg.tests || '')
      const raw = py.runPython('import judge; judge.judge(__code, __tests)')
      await saveFS()
      post({ type: 'files', data: listFiles() })
      post({ type: 'judged', id: msg.id, data: JSON.parse(raw) })
      return
    }
  } catch (err) {
    const text = String(err && err.message ? err.message : err)
    if (text.includes('__OUTPUT_OVERFLOW__')) {
      post({ type: 'done', id: msg.id, error: { type: 'OutputOverflow', message: '输出太多了', line: null } })
    } else if (text.includes('__INPUT_CANCELLED__')) {
      post({ type: 'done', id: msg.id, error: null, cancelled: true })
    } else {
      post({ type: 'done', id: msg.id, error: { type: 'WorkerError', message: text, line: null } })
    }
  }
}
