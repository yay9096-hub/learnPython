/**
 * 主线程这一侧的 Pyodide 客户端。
 *
 * 职责：
 *  - 起 worker、准备 SharedArrayBuffer（input() 的阻塞通道）
 *  - 把 stdout / turtle 指令 / 输入请求转成回调
 *  - 「停止」= 直接 terminate worker 再重建，死循环也拦得住
 */

const CTRL_LEN = 2 // [0] 信号量, [1] 输入字节数
const BUF_BYTES = 64 * 1024

export const isolated = () =>
  typeof SharedArrayBuffer !== "undefined" && globalThis.crossOriginIsolated === true

export class PyRunner {
  constructor(handlers = {}) {
    this.h = handlers
    this.worker = null
    this.ready = null
    this.ctrl = null
    this.inbuf = null
    this.busy = false
    this.pending = null // { resolve, reject, kind }
    this.awaitingInput = false
    this.bootTimer = null
    this.disposed = false
    this.persistent = false // 文件能不能存住（IDBFS 挂上了没）
  }

  /** 往学生的工作目录里塞一个文件（比如她自己的学习记录） */
  async writeFile(name, text) {
    await this.start()
    this.worker?.postMessage({ type: "writeFile", name, text })
  }

  /** 让 worker 重新报一遍文件列表 */
  listFiles() {
    this.worker?.postMessage({ type: "listFiles" })
  }

  /** 清空她的文件目录 */
  clearFiles() {
    this.worker?.postMessage({ type: "clearFiles" })
  }

  _makeBuffers() {
    if (!isolated()) return { ctrl: null, inbuf: null }
    const ctrl = new Int32Array(new SharedArrayBuffer(CTRL_LEN * 4))
    const inbuf = new Uint8Array(new SharedArrayBuffer(BUF_BYTES))
    return { ctrl, inbuf }
  }

  start() {
    if (this.ready) return this.ready
    this.ready = new Promise((resolve, reject) => {
      const worker = new Worker("/pyworker.js")
      const { ctrl, inbuf } = this._makeBuffers()
      this.worker = worker
      this.ctrl = ctrl
      this.inbuf = inbuf

      // 定时器存在实例上：worker 被销毁时要一并清掉，
      // 否则一个早已丢弃的 runner 会在 90 秒后往界面上扔一条假的超时提示
      this.bootTimer = setTimeout(() => {
        if (!this.disposed) reject(new Error("Python 加载超时了，刷新页面再试一次？"))
      }, 90000)

      worker.onmessage = (e) => {
        const m = e.data
        switch (m.type) {
          case "ready":
            clearTimeout(this.bootTimer)
            this.persistent = !!m.persistent
            resolve({ interactive: m.interactive, persistent: m.persistent })
            break
          case "files":
            this.h.onFiles?.(m.data)
            break
          case "plot":
            this.h.onPlot?.(m.data)
            break
          case "stdout":
            this.h.onStdout?.(m.text)
            break
          case "stderr":
            this.h.onStderr?.(m.text)
            break
          case "turtle":
            this.h.onTurtle?.(m.data)
            break
          case "overflow":
            this.h.onOverflow?.()
            break
          case "input":
            this.awaitingInput = true
            this.h.onInputRequest?.(m.prompt)
            break
          case "done": {
            this.busy = false
            this.awaitingInput = false
            const p = this.pending
            this.pending = null
            p?.resolve({ error: m.error ?? null, cancelled: !!m.cancelled })
            break
          }
          case "judged": {
            this.busy = false
            const p = this.pending
            this.pending = null
            p?.resolve(m.data)
            break
          }
          default:
            break
        }
      }

      worker.onerror = (e) => {
        clearTimeout(this.bootTimer)
        if (this.disposed) return
        this.busy = false
        const p = this.pending
        this.pending = null
        const err = new Error(e.message || "Python 引擎出错了")
        p ? p.reject(err) : reject(err)
      }

      worker.postMessage({ type: "init", ctrl, inbuf })
    })
    return this.ready
  }

  /** 她在输入框里按了回车 */
  provideInput(text) {
    if (!this.ctrl || !this.awaitingInput) return
    const bytes = new TextEncoder().encode(String(text))
    const n = Math.min(bytes.length, BUF_BYTES)
    this.inbuf.set(bytes.subarray(0, n), 0)
    Atomics.store(this.ctrl, 1, n)
    Atomics.store(this.ctrl, 0, 1)
    Atomics.notify(this.ctrl, 0)
    this.awaitingInput = false
  }

  async run(code, stdin = null) {
    await this.start()
    if (this.busy) throw new Error("上一段代码还在跑呢～")
    this.busy = true
    return new Promise((resolve, reject) => {
      this.pending = { resolve, reject }
      this.worker.postMessage({ type: "run", code, stdin, id: Date.now() })
    })
  }

  async judge(code, tests) {
    await this.start()
    if (this.busy) throw new Error("上一段代码还在跑呢～")
    this.busy = true
    return new Promise((resolve, reject) => {
      this.pending = { resolve, reject }
      this.worker.postMessage({ type: "judge", code, tests, id: Date.now() })
    })
  }

  /** 强制停止：worker 直接杀掉重建，比任何超时机制都可靠 */
  stop() {
    if (!this.worker) return
    clearTimeout(this.bootTimer)
    this.worker.terminate()
    this.worker = null
    this.ready = null
    this.busy = false
    this.awaitingInput = false
    const p = this.pending
    this.pending = null
    p?.resolve({ error: null, cancelled: true })
    return this.start()
  }

  dispose() {
    this.disposed = true
    clearTimeout(this.bootTimer)
    this.worker?.terminate()
    this.worker = null
    this.ready = null
    this.pending = null
  }
}
