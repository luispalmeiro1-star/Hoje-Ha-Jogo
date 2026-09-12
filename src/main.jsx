import React from 'react'
import ReactDOM from 'react-dom/client'
// O import é de "/react" e não de "/next": esta app é React com Vite. O exemplo
// que o painel do Vercel mostra por omissão é o de Next.js e não compila aqui.
import { Analytics } from '@vercel/analytics/react'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
    <Analytics />
  </React.StrictMode>
)
