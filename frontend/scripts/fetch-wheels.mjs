// 把 matplotlib 需要的 wheel 下载到 public/pyodide/，让第七章能离线画图。
//
// 为什么要单独一个脚本：npm 的 pyodide 包**不含** wheel 文件 ——
// Pyodide 默认运行时去 CDN 现取。那样一断网第七章就废了，
// 所以构建时先抓下来放本地，跟 Pyodide 核心放在一起。
//
// 依赖关系从 pyodide-lock.json 里递归解析，不用手写清单：
// 官方哪天调整了依赖，这个脚本自动跟上。
import { existsSync, mkdirSync, readFileSync, writeFileSync, statSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const pkgDir = resolve(here, '..', 'node_modules', 'pyodide')
const destDir = resolve(here, '..', 'public', 'pyodide')

// 第七章要用的顶层包。依赖会自动带上。
const WANTED = ['matplotlib']

if (!existsSync(pkgDir)) {
  console.warn('[fetch-wheels] 还没 npm install，跳过')
  process.exit(0)
}

const lockPath = join(pkgDir, 'pyodide-lock.json')
const lock = JSON.parse(readFileSync(lockPath, 'utf8'))
const packages = lock.packages || {}
const version = lock.info?.version
if (!version) {
  console.error('[fetch-wheels] lock 文件里没有版本号，装不了')
  process.exit(1)
}

/** 递归收集一个包及其全部依赖 */
function collect(name, seen = new Set()) {
  if (seen.has(name)) return seen
  const pkg = packages[name]
  if (!pkg) {
    console.warn(`[fetch-wheels] lock 里没有 ${name}，跳过`)
    return seen
  }
  seen.add(name)
  for (const dep of pkg.depends || []) collect(dep, seen)
  return seen
}

const needed = new Set()
for (const name of WANTED) for (const n of collect(name)) needed.add(n)

mkdirSync(destDir, { recursive: true })

const base = `https://cdn.jsdelivr.net/pyodide/v${version}/full/`
let downloaded = 0
let skipped = 0
let bytes = 0

for (const name of [...needed].sort()) {
  const file = packages[name].file_name
  if (!file) continue
  const out = join(destDir, file)

  if (existsSync(out) && statSync(out).size > 0) {
    skipped++
    bytes += statSync(out).size
    continue
  }

  const url = base + file
  process.stdout.write(`[fetch-wheels] ${name} … `)
  const res = await fetch(url)
  if (!res.ok) {
    console.log(`失败 (${res.status})`)
    console.error(`[fetch-wheels] 下载不了 ${url}`)
    process.exit(1)
  }
  const buf = Buffer.from(await res.arrayBuffer())
  writeFileSync(out, buf)
  downloaded++
  bytes += buf.length
  console.log(`${(buf.length / 1048576).toFixed(1)} MB`)
}

console.log(
  `[fetch-wheels] ${needed.size} 个包就绪`
  + `（新下载 ${downloaded}，已有 ${skipped}），`
  + `共 ${(bytes / 1048576).toFixed(1)} MB → public/pyodide/`,
)
