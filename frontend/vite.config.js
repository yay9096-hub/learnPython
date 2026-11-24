import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// SharedArrayBuffer 需要跨域隔离，input() 的阻塞式实现依赖它。
// nginx.conf 里也配了同样两个头，保证 dev 和 prod 行为一致。
const crossOriginIsolation = {
  name: 'cross-origin-isolation',
  configureServer(server) {
    server.middlewares.use((_req, res, next) => {
      res.setHeader('Cross-Origin-Opener-Policy', 'same-origin')
      res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp')
      next()
    })
  },
}

export default defineConfig({
  plugins: [react(), crossOriginIsolation],
  server: {
    port: 5173,
    proxy: { '/api': 'http://localhost:8000' },
  },
  build: { chunkSizeWarningLimit: 2000 },
})
