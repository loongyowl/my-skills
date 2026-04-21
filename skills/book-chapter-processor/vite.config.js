import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// GitHub Pages 部署：将 'book-chapter-processor' 替换为你的仓库名
export default defineConfig({
  plugins: [react()],
  base: '/book-chapter-processor/',
})
