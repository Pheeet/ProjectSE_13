import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    server: {
        host: true,
        port: parseInt(process.env.VITE_PORT || '5173', 10),
        strictPort: true,
        proxy: {
            '/api': {
                target: 'http://flask:8000',
                changeOrigin: true
            }
        }
    }
})
