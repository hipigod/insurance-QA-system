import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

// Vite 配置参考：https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const devPort = Number(env.VITE_DEV_PORT || 5173)
  const hmrPort = Number(env.VITE_HMR_PORT || devPort)
  const hmrHost = env.VITE_HMR_HOST || 'localhost'

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      host: true,
      port: devPort,
      strictPort: true,
      hmr: {
        host: hmrHost,
        clientPort: hmrPort
      },
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:8000',
          changeOrigin: true
        },
        '/ws': {
          target: 'ws://127.0.0.1:8000',
          ws: true
        }
      }
    }
  }
})
