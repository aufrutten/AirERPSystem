import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'
import vitePluginFaviconsInject from 'vite-plugin-favicons-inject'

const projectName = "ProjectName"

const faviconConfig = {
  appName: projectName,
  appShortName: projectName, // Your application's short_name. `string`. Optional. If not set, appName will be used
  appDescription: projectName,
}

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueJsx(),
    vitePluginFaviconsInject('./public/favicon.svg', faviconConfig),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
