import { useEffect, useImperativeHandle, useRef, forwardRef, useState } from "react"

const W = 520
const H = 420

/**
 * 把 turtle_shim 记录下来的指令一条条画到 Canvas 上（带动画，看得见笔在走）。
 * 动画速度跟 turtle 的 speed() 挂钩，speed(0) 直接瞬间画完。
 */
function drawAll(ctx, data, upto) {
  ctx.clearRect(0, 0, W, H)
  ctx.fillStyle = data.bg || "#FFFFFF"
  ctx.fillRect(0, 0, W, H)

  const cx = W / 2
  const cy = H / 2
  const X = (x) => cx + x
  const Y = (y) => cy - y // turtle 的 y 轴朝上

  ctx.lineCap = "round"
  ctx.lineJoin = "round"

  for (let i = 0; i < upto && i < data.cmds.length; i++) {
    const c = data.cmds[i]
    if (c.op === "line") {
      ctx.beginPath()
      ctx.strokeStyle = c.color
      ctx.lineWidth = c.w
      ctx.moveTo(X(c.x1), Y(c.y1))
      ctx.lineTo(X(c.x2), Y(c.y2))
      ctx.stroke()
    } else if (c.op === "dot") {
      ctx.beginPath()
      ctx.fillStyle = c.color
      ctx.arc(X(c.x), Y(c.y), Math.max(1.5, c.r), 0, Math.PI * 2)
      ctx.fill()
    } else if (c.op === "fill") {
      ctx.beginPath()
      ctx.fillStyle = c.color
      c.points.forEach(([x, y], k) => (k ? ctx.lineTo(X(x), Y(y)) : ctx.moveTo(X(x), Y(y))))
      ctx.closePath()
      ctx.fill()
    } else if (c.op === "write") {
      ctx.fillStyle = c.color
      ctx.font = `${c.size}px "PingFang SC", "Microsoft YaHei", sans-serif`
      ctx.textAlign = c.align === "center" ? "center" : c.align === "right" ? "right" : "left"
      ctx.fillText(c.text, X(c.x), Y(c.y))
    }
  }
}

const TurtleCanvas = forwardRef(function TurtleCanvas({ data }, ref) {
  const canvasRef = useRef(null)
  const timer = useRef(null)
  const [done, setDone] = useState(true)

  useImperativeHandle(ref, () => ({
    /** 完成当天任务时，把画好的图存进作品陈列馆 */
    toDataURL: () => {
      try {
        return canvasRef.current?.toDataURL("image/png")
      } catch {
        return null
      }
    },
  }))

  useEffect(() => {
    const ctx = canvasRef.current?.getContext("2d")
    if (!ctx) return
    clearInterval(timer.current)

    if (!data || !data.cmds?.length) {
      drawAll(ctx, data || { bg: null, cmds: [] }, 0)
      setDone(true)
      return
    }

    const speed = data.cmds[0]?.speed ?? 5
    if (speed === 0 || data.cmds.length > 600) {
      drawAll(ctx, data, data.cmds.length)
      setDone(true)
      return
    }

    setDone(false)
    let i = 0
    const step = Math.max(1, Math.round(speed / 2))
    const interval = Math.max(8, 90 - speed * 8)
    timer.current = setInterval(() => {
      i += step
      drawAll(ctx, data, i)
      if (i >= data.cmds.length) {
        clearInterval(timer.current)
        setDone(true)
      }
    }, interval)

    return () => clearInterval(timer.current)
  }, [data])

  const empty = !data || !data.cmds?.length

  return (
    <div className="relative">
      <canvas
        ref={canvasRef}
        width={W}
        height={H}
        className="w-full rounded-xl border border-magic-100 bg-white shadow-card"
      />
      {empty && (
        <div className="pointer-events-none absolute inset-0 flex items-center justify-center text-sm text-ink-faint">
          小海龟还在等你下指令 🐢
        </div>
      )}
      {!done && (
        <div className="absolute right-2.5 top-2.5 chip bg-magic-500/90 text-white">绘制中…</div>
      )}
    </div>
  )
})

export default TurtleCanvas
