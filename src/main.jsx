import React from 'react'
import ReactDOM from 'react-dom/client'
// O import é de "/react" e não de "/next": esta app é React com Vite. O exemplo
// que o painel do Vercel mostra por omissão é o de Next.js e não compila aqui.
import { Analytics } from '@vercel/analytics/react'
import App from './App.jsx'

// As visitas de quem faz a app falseiam as contagens: com este volume de
// tráfego, abrir a app três vezes para testar chega para triplicar os
// "visitantes" do dia. Abrir hojehajogo.pt/?analytics=off marca este
// dispositivo como excluído, e ?analytics=on volta a incluí-lo. A marca fica
// no dispositivo, por isso é preciso fazê-lo uma vez em cada telefone ou
// computador.
const OPTOUT_KEY = "hhj_analytics_optout"

function isExcludedFromAnalytics() {
  try {
    const url = new URL(window.location.href)
    const escolha = url.searchParams.get("analytics")
    if (escolha === "off") localStorage.setItem(OPTOUT_KEY, "1")
    if (escolha === "on") localStorage.removeItem(OPTOUT_KEY)
    if (escolha) {
      // Remove só este parâmetro e deixa os outros (?reset, ?vaga) intactos,
      // para a escolha não viajar num link partilhado com outra pessoa.
      url.searchParams.delete("analytics")
      window.history.replaceState({}, "", url.pathname + url.search + url.hash)
    }
    return localStorage.getItem(OPTOUT_KEY) === "1"
  } catch (e) {
    // Janela privada ou armazenamento bloqueado: nesse caso contar a visita é
    // o comportamento certo — mais vale uma visita a mais do que perder tráfego
    // real por não conseguirmos ler uma preferência.
    return false
  }
}

const excluido = isExcludedFromAnalytics()

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
    <Analytics beforeSend={(evento) => (excluido ? null : evento)} />
  </React.StrictMode>
)
