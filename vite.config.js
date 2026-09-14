import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      filename: 'sw.js',
      manifest: {
        name: 'Hoje Há Jogo',
        short_name: 'Hoje Há Jogo',
        description: 'Gestão do jogo semanal',
        theme_color: '#0a0a0a',
        background_color: '#0a0a0a',
        display: 'standalone',
        orientation: 'portrait',
        icons: [
          { src: '/icon-192.png', sizes: '192x192', type: 'image/png' },
          { src: '/icon-512.png', sizes: '512x512', type: 'image/png' }
        ]
      },
      workbox: {
        importScripts: ['OneSignalSDKWorker.js'],
        // A /privacidade é uma página à parte, em HTML simples. Sem esta
        // exceção o service worker responderia com a app a qualquer navegação,
        // e quem já tem a app instalada nunca veria a página — veria o ecrã de
        // entrada. Vale para quem partilha o link e para quem o vai buscar de
        // fora (a Play Store, por exemplo).
        navigateFallbackDenylist: [/^\/privacidade/]
      }
    })
  ]
})
