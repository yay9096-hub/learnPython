// 把 Pyodide 运行时从 node_modules 拷进 public/pyodide/，让网站完全离线可用。
// 只拷核心文件（约 25MB），不拷 numpy/matplotlib 等 wheel —— 前 10 天用不到。
// 以后要用 matplotlib，把 node_modules/pyodide 下对应的 .whl 一并拷过来即可。
import { existsSync, mkdirSync, copyFileSync, readdirSync, statSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const src = resolve(here, '..', 'node_modules', 'pyodide')
const dest = resolve(here, '..', 'public', 'pyodide')

if (!existsSync(src)) {
  console.warn('[copy-pyodide] node_modules/pyodide 不存在，跳过（先 npm install）')
  process.exit(0)
}

const KEEP = /^(pyodide\.(js|mjs|asm\.js|asm\.wasm)|python_stdlib\.zip|pyodide-lock\.json)$/

mkdirSync(dest, { recursive: true })
let n = 0
let bytes = 0
for (const name of readdirSync(src)) {
  if (!KEEP.test(name)) continue
  const from = join(src, name)
  if (!statSync(from).isFile()) continue
  copyFileSync(from, join(dest, name))
  bytes += statSync(from).size
  n++
}
console.log(`[copy-pyodide] 已拷贝 ${n} 个文件 (${(bytes / 1048576).toFixed(1)} MB) → public/pyodide/`)
