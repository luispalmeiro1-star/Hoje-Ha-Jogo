#!/usr/bin/env python3
"""Gera as páginas de /guias a partir do texto abaixo.

São páginas HTML simples, à parte da app, para o Google as conseguir ler:
a app em si é JavaScript e quase não aparece em pesquisas. Para juntar uma
página nova: acrescentar uma entrada a PAGINAS e correr
    python3 scripts/gerar-guias.py
O sitemap é atualizado na mesma corrida.
"""
import html, json, os, datetime

RAIZ = os.path.join(os.path.dirname(__file__), "..", "public")
SITE = "https://hojehajogo.pt"
HOJE = datetime.date.today().isoformat()

CSS = """
:root{--fundo:#0a0b08;--caixa:#14160f;--borda:#23271b;--texto:#d8dbd2;--suave:#8a9080;--ouro:#d4af37;--verde:#4ade80}
*{box-sizing:border-box}
body{margin:0;background:var(--fundo);color:var(--texto);font-family:'DM Sans',system-ui,-apple-system,'Segoe UI',sans-serif;font-size:16.5px;line-height:1.7;-webkit-text-size-adjust:100%}
a{color:var(--ouro)}
.topo{border-bottom:1px solid var(--borda)}
.topo div{max-width:720px;margin:0 auto;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.marca{display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;font-family:'Bebas Neue',sans-serif;font-size:22px;letter-spacing:.08em}
.marca img{width:28px;height:28px}
.marca b{color:var(--ouro);font-weight:400}
.topo .guias{font-size:14px;font-weight:700;text-decoration:none}
main{max-width:720px;margin:0 auto;padding:34px 20px 20px}
.migalha{font-size:13px;color:var(--suave);margin:0 0 14px}
.migalha a{color:var(--suave)}
h1{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:clamp(38px,9vw,56px);line-height:1;color:#fff;margin:0 0 14px;text-wrap:balance}
.entrada{font-size:19px;color:#e9eadf;margin:0 0 26px}
h2{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:30px;line-height:1.1;color:var(--ouro);margin:38px 0 10px;letter-spacing:.02em}
h3{font-size:17px;color:#fff;margin:22px 0 4px}
p{margin:0 0 14px}
ul,ol{margin:0 0 16px;padding-left:22px}
li{margin-bottom:6px}
strong{color:#fff}
.cta{background:var(--caixa);border:1px solid var(--borda);border-radius:18px;padding:24px 22px;margin:34px 0;text-align:center}
.cta p{margin:0 0 16px;color:#e9eadf}
.botao{display:inline-block;background:var(--ouro);color:#0a0b08;font-weight:800;font-size:17px;text-decoration:none;padding:15px 26px;border-radius:14px}
.cta small{display:block;margin-top:12px;color:var(--suave);font-size:13px}
.lista-guias{list-style:none;padding:0;display:grid;gap:12px}
.lista-guias a{display:block;background:var(--caixa);border:1px solid var(--borda);border-radius:16px;padding:18px 20px;text-decoration:none}
.lista-guias b{display:block;color:#fff;font-size:18px;margin-bottom:2px}
.lista-guias span{color:var(--suave);font-size:14.5px}
.outros{border-top:1px solid var(--borda);margin-top:40px;padding-top:8px}
.outros h2{font-size:22px;color:var(--suave)}
footer{max-width:720px;margin:0 auto;padding:26px 20px 60px;color:var(--suave);font-size:13px}
footer a{color:var(--suave)}
/* sorteador */
.sorteio{background:var(--caixa);border:1px solid var(--borda);border-radius:18px;padding:20px;margin:0 0 30px}
.sorteio label{display:block;font-size:13px;font-weight:700;color:var(--suave);letter-spacing:.06em;text-transform:uppercase;margin-bottom:8px}
.sorteio textarea{width:100%;min-height:220px;background:#0f0f0f;border:2px solid var(--borda);border-radius:12px;color:#f0f0f0;font:inherit;font-size:16px;padding:12px 14px;resize:vertical}
.sorteio textarea:focus,.sorteio select:focus,.sorteio button:focus-visible,a:focus-visible{outline:2px solid var(--ouro);outline-offset:2px}
.linha{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:14px}
.sorteio select{background:#0f0f0f;border:2px solid var(--borda);border-radius:12px;color:#f0f0f0;font:inherit;padding:12px}
.sorteio button{flex:1;min-width:160px;background:var(--verde);color:#052610;border:0;border-radius:12px;font:inherit;font-weight:800;font-size:17px;padding:14px;cursor:pointer}
.sorteio button.sec{background:transparent;color:var(--ouro);border:1px solid var(--ouro)}
.aviso{color:#fbbf24;font-size:14px;margin:12px 0 0;min-height:1.2em}
.equipas{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:16px}
.equipa{background:#0f0f0f;border:1px solid var(--borda);border-radius:14px;padding:14px 16px}
.equipa h3{font-family:'Bebas Neue',sans-serif;font-weight:400;font-size:24px;color:var(--ouro);margin:0 0 6px}
.equipa ol{margin:0;padding-left:20px}
"""

def pagina(slug, titulo, descricao, h1, entrada, corpo, faq=None, extra_head="", extra_body="", outros=True):
    url = f"{SITE}/guias/" + (f"{slug}/" if slug else "")
    ld = []
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": r}} for p, r in faq]})
    if slug:
        ld.append({"@context": "https://schema.org", "@type": "Article", "headline": h1, "description": descricao,
                   "inLanguage": "pt-PT", "dateModified": HOJE, "mainEntityOfPage": url,
                   "author": {"@type": "Organization", "name": "Hoje Há Jogo"},
                   "publisher": {"@type": "Organization", "name": "Hoje Há Jogo", "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png"}}})
    ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n' for x in ld)
    faq_html = ""
    if faq:
        faq_html = "<h2>Perguntas frequentes</h2>\n" + "".join(f"<h3>{html.escape(p)}</h3>\n<p>{html.escape(r)}</p>\n" for p, r in faq)
    outros_html = ""
    if outros:
        itens = "".join(f'<li><a href="/guias/{s}/"><b>{html.escape(t)}</b><span>{html.escape(d)}</span></a></li>'
                        for s, t, d in INDICE if s != slug)
        outros_html = f'<section class="outros"><h2>Outros guias</h2><ul class="lista-guias">{itens}</ul></section>'
    migalha = '<p class="migalha"><a href="/guias/">Guias</a> › ' + html.escape(h1) + "</p>" if slug else ""
    return f"""<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#0a0b08">
<title>{html.escape(titulo)}</title>
<meta name="description" content="{html.escape(descricao)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(titulo)}">
<meta property="og:description" content="{html.escape(descricao)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:locale" content="pt_PT">
<link rel="icon" type="image/svg+xml" href="/icon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@400;600;700;800&display=swap">
<link rel="stylesheet" href="/guias/estilo.css">
<script defer src="/_vercel/insights/script.js"></script>
{ld_html}{extra_head}</head>
<body>
<header class="topo"><div>
  <a class="marca" href="/"><img src="/icon.svg" alt="" width="28" height="28">HOJE HÁ <b>JOGO</b></a>
  <a class="guias" href="/guias/">Guias</a>
</div></header>
<main>
{migalha}
<h1>{html.escape(h1)}</h1>
<p class="entrada">{entrada}</p>
{corpo}
{faq_html}
<div class="cta">
  <p><strong>A Hoje Há Jogo trata disto por ti.</strong> Cada um responde VOU ou NÃO VOU e a lista faz-se sozinha.</p>
  <a class="botao" href="/">⚽ Criar o meu jogo grátis</a>
  <small>Grátis · Sem instalar · Sem publicidade</small>
</div>
{outros_html}
</main>
<footer>Hoje Há Jogo · <a href="/">Abrir a app</a> · <a href="/guias/">Guias</a> · <a href="/privacidade">Privacidade</a></footer>
{extra_body}</body>
</html>
"""

INDICE = [
    ("organizar-jogo-futebol-amigos", "Como organizar um jogo de futebol com amigos", "Do campo às contas: o que é preciso para o jogo acontecer todas as semanas."),
    ("sortear-equipas", "Sortear equipas de futebol", "Escreve os nomes e recebe as equipas feitas. Grátis, sem conta."),
    ("lista-de-presencas-futebol", "Lista de presenças para o futebol", "Como saber quantos são sem 40 mensagens no grupo."),
    ("dividir-custo-do-campo", "Como dividir o custo do campo", "Quanto paga cada um, quem cobra e o que fazer com quem falta."),
    ("lista-de-espera-futebol", "Lista de espera e convidados", "O que fazer quando o jogo enche e quando alguém desiste à última hora."),
]

PAGINAS = {}

PAGINAS["organizar-jogo-futebol-amigos"] = dict(
    titulo="Como organizar um jogo de futebol com amigos (todas as semanas)",
    descricao="Guia prático para organizar o futebol ou futsal semanal com amigos: marcar o campo, saber quem vai, fazer equipas e dividir as contas.",
    h1="Como organizar um jogo de futebol com amigos",
    entrada="Marcar um jogo é fácil. Difícil é ele acontecer todas as semanas, com gente suficiente e sem ser sempre a mesma pessoa a pagar o campo. Este guia junta o que resulta nos grupos que duram.",
    corpo="""
<h2>1. Um dia e uma hora fixos</h2>
<p>O jogo que muda de dia todas as semanas acaba por morrer. Escolhe um dia e uma hora e não mexas: <strong>quarta às 22h30</strong>, por exemplo. As pessoas organizam a semana à volta disso e deixa de ser preciso combinar tudo de cada vez.</p>

<h2>2. Mais gente no grupo do que lugares no campo</h2>
<p>Há sempre quem falhe. Para um jogo de futsal de 5 contra 5 precisas de 10 em campo, mas o grupo deve ter 15 a 20 pessoas. Com 10 certinhos, basta uma gripe para não haver jogo.</p>
<ul>
  <li><strong>Futsal ou futebol de 5:</strong> 10 em campo, grupo de 15 a 20.</li>
  <li><strong>Futebol de 7:</strong> 14 em campo, grupo de 20 a 25.</li>
  <li><strong>Futebol de 11:</strong> 22 em campo, grupo de 30 ou mais.</li>
</ul>

<h2>3. Saber quem vai, cedo</h2>
<p>É aqui que quase todos os grupos sofrem. A pergunta "quem vai?" no WhatsApp dá dezenas de mensagens, respostas a meio ("depois digo") e ninguém sabe o número final. O que funciona:</p>
<ul>
  <li>Cada pessoa dá <strong>uma resposta clara</strong>: vou ou não vou. "Talvez" não conta.</li>
  <li>Quem não vai também responde. Assim sabes quem ainda falta e não ficas à espera.</li>
  <li>Há um <strong>prazo</strong>: na véspera à noite a lista está fechada ou chamam-se reforços.</li>
</ul>
<p>Vê o guia da <a href="/guias/lista-de-presencas-futebol/">lista de presenças</a>.</p>

<h2>4. Uma regra para quando o jogo enche</h2>
<p>Quando há mais gente do que lugares, os primeiros a confirmar jogam e os outros ficam em <a href="/guias/lista-de-espera-futebol/">lista de espera</a>. Se alguém desiste, entra o primeiro da espera. Combina também se os amigos de fora (os convidados) têm o mesmo direito que quem é do grupo.</p>

<h2>5. Equipas sem discussão</h2>
<p>Capitães a escolher deixa sempre alguém para o fim. Um sorteio é mais rápido e ninguém se queixa. Podes usar o nosso <a href="/guias/sortear-equipas/">sorteador de equipas</a>, que é grátis.</p>

<h2>6. Contas à vista</h2>
<p>O campo paga-se, e é chato ser sempre o mesmo a adiantar e a cobrar. Decidam um valor fixo por jogo, um responsável pelo dinheiro e uma forma de toda a gente ver quem já pagou. Mais no guia sobre <a href="/guias/dividir-custo-do-campo/">dividir o custo do campo</a>.</p>
""",
    faq=[
        ("Quantas pessoas são precisas para um grupo de futebol semanal?", "Conta com um grupo 50% a 100% maior do que os lugares em campo. Para um jogo de 5 contra 5 (10 jogadores), 15 a 20 pessoas no grupo dão margem para faltas."),
        ("Como evito que o jogo seja cancelado à última hora?", "Pede respostas claras (vou ou não vou) com prazo na véspera, e tem uma lista de espera ou convidados para ocupar os lugares de quem desiste."),
        ("Preciso de uma app para organizar o jogo?", "Não é obrigatório, mas poupa trabalho. Na Hoje Há Jogo cada jogador responde VOU ou NÃO VOU, a lista de espera avança sozinha, as equipas são sorteadas e as contas ficam à vista. É grátis e não é preciso instalar."),
    ],
)

PAGINAS["lista-de-presencas-futebol"] = dict(
    titulo="Lista de presenças para o futebol: como saber quem vai ao jogo",
    descricao="Como fazer uma lista de presenças para o futebol ou futsal com amigos, sem dezenas de mensagens no WhatsApp. Regras simples e uma app grátis.",
    h1="Lista de presenças para o futebol",
    entrada="\"Quem vai quarta?\" \"Eu.\" \"Eu +1.\" \"Depois digo.\" \"Afinal não dá.\" Quarenta mensagens depois, ainda ninguém sabe quantos são. Uma lista de presenças resolve isto, desde que tenha três regras.",
    corpo="""
<h2>O problema da lista no WhatsApp</h2>
<p>A lista copiada e colada ("1. Rui 2. Tiago 3. …") funciona enquanto o grupo é pequeno. Depois começa a falhar sempre da mesma maneira:</p>
<ul>
  <li>Duas pessoas copiam a lista ao mesmo tempo e uma delas desaparece.</li>
  <li>Quem desiste não se risca, ou risca-se e ninguém repara.</li>
  <li>Quem não vai não diz nada, e ficas sem saber se ainda vai responder.</li>
  <li>A lista perde-se no meio das outras conversas.</li>
</ul>

<h2>Três regras para uma lista que funciona</h2>
<h3>1. Só duas respostas</h3>
<p><strong>Vou</strong> ou <strong>não vou</strong>. Sem "talvez". Quem não sabe ainda, não respondeu.</p>
<h3>2. Quem não vai também responde</h3>
<p>Parece estranho, mas é o que mais ajuda quem organiza. Com 8 "vou" e 6 "não vou", sabes que faltam 4 pessoas por responder e a quem perguntar. Sem isso, só vês silêncio.</p>
<h3>3. A lista está sempre no mesmo sítio</h3>
<p>Um link fixo que todos abrem, em vez de uma mensagem que sobe no grupo. Quem abre vê o estado de agora: quantos vão, quantos faltam, quem está em espera.</p>

<h2>O que a lista deve mostrar</h2>
<ul>
  <li><strong>Quantos confirmaram</strong> e quantos lugares há (por exemplo, 8 de 12).</li>
  <li><strong>Quem ainda não respondeu</strong>, para se poder lembrar só essas pessoas.</li>
  <li><strong>Quem está em espera</strong>, por ordem, quando o jogo já encheu.</li>
  <li><strong>A data, a hora e o local</strong> do jogo, para não se repetir a pergunta.</li>
</ul>

<h2>Como a Hoje Há Jogo faz</h2>
<p>Cada jogador abre o link do grupo e toca em <strong>VOU</strong> ou <strong>NÃO VOU</strong>. A lista atualiza-se para todos na hora. Quando o jogo enche, quem chega a seguir fica em <a href="/guias/lista-de-espera-futebol/">lista de espera</a> e entra sozinho se alguém desistir. Quem ainda não respondeu recebe um aviso, sem teres de ser tu a perguntar.</p>
""",
    faq=[
        ("Como faço uma lista de presenças para o futebol no WhatsApp?", "Podes usar uma mensagem numerada que cada um copia e acrescenta o nome, ou uma sondagem. Funciona em grupos pequenos, mas perde-se facilmente e não mostra quem falta responder nem gere lista de espera."),
        ("Qual é a melhor app para lista de presenças de futebol?", "Procura uma que mostre quem vai, quem não vai e quem ainda não respondeu, e que trate da lista de espera. A Hoje Há Jogo faz isso, é grátis, está em português e abre no browser, sem instalar."),
        ("Os jogadores precisam de instalar alguma coisa?", "Na Hoje Há Jogo não. Entram pelo link de convite do grupo, criam a conta e respondem. Quem quiser pode adicionar a app ao ecrã inicial do telemóvel."),
    ],
)

PAGINAS["dividir-custo-do-campo"] = dict(
    titulo="Como dividir o custo do campo de futebol entre amigos",
    descricao="Quanto deve pagar cada jogador pelo campo, quem cobra, o que fazer com quem falta e com quem fica a dever. Regras simples para o futebol semanal.",
    h1="Como dividir o custo do campo",
    entrada="O campo custa dinheiro e alguém tem de o adiantar. Se as regras não forem claras, é sempre a mesma pessoa a pagar e a andar atrás dos outros. Estas são as que evitam discussões.",
    corpo="""
<h2>Quanto paga cada um</h2>
<p>A conta é simples: <strong>preço do campo a dividir pelo número de lugares</strong>. Um campo de 30 € para 10 jogadores dá 3 € a cada um.</p>
<p>O melhor é fixar um valor redondo por jogo e não o mudar de semana para semana. Se num jogo forem 12 em vez de 10, sobra algum dinheiro, que fica guardado para as semanas em que faltar gente, para bolas ou para coletes.</p>

<h2>Um mealheiro do grupo</h2>
<p>É isto que resolve as semanas más. Com um valor fixo por jogador, os jogos cheios deixam uma pequena sobra. Essa sobra é o <strong>mealheiro</strong>, e paga a diferença quando só aparecem 9 em vez de 10. O importante é toda a gente poder ver quanto lá está.</p>

<h2>Quem paga quando alguém falta</h2>
<p>Combinem isto antes de acontecer. As regras mais comuns:</p>
<ul>
  <li><strong>Quem confirmou e não apareceu paga na mesma.</strong> O lugar ficou reservado para ele.</li>
  <li><strong>Quem desiste a tempo de ser substituído não paga.</strong> "A tempo" tem de ter uma hora marcada, por exemplo até à véspera.</li>
  <li><strong>Quem traz um convidado responde por ele.</strong> Se o convidado não pagar, paga quem o convidou.</li>
</ul>

<h2>Uma pessoa a tratar do dinheiro</h2>
<p>Um tesoureiro por jogo, que pode ir rodando. É quem recebe e quem marca os pagamentos. O que cansa não é pagar o campo, é andar a perguntar "já pagaste?". Por isso a lista de quem pagou deve estar à vista de todos: quem deve vê que deve, sem ninguém ter de lhe dizer.</p>

<h2>Como receber</h2>
<p>Em Portugal, o MB WAY resolve quase tudo. Deixa o número de quem recebe num sítio fixo, para ninguém ter de o pedir. Dinheiro em mão no balneário também serve, desde que fique registado logo.</p>

<h2>Como a Hoje Há Jogo faz</h2>
<p>O grupo define o preço por jogador. Ao lado de cada nome aparece <strong>Pago</strong> ou <strong>Deve 3 €</strong>. Quando o jogo fecha, quem confirmou e não pagou fica com a dívida registada, e os convidados ficam na conta de quem os trouxe. O mealheiro do grupo está sempre visível.</p>
""",
    faq=[
        ("Quanto custa a cada um um jogo de futsal?", "Depende do campo. Divide o preço do aluguer pelo número de jogadores: um campo de 30 € para 10 pessoas dá 3 € a cada um. Muitos grupos fixam um valor redondo e guardam a sobra num mealheiro."),
        ("Quem falta ao jogo deve pagar?", "A regra mais usada é: quem confirmou e não apareceu paga, porque ocupou um lugar. Quem avisa a tempo de ser substituído não paga."),
        ("Como controlo quem já pagou o campo?", "Com uma lista visível para todo o grupo, onde cada pagamento é marcado na hora. Na Hoje Há Jogo isso aparece ao lado de cada nome e as dívidas ficam registadas quando o jogo fecha."),
    ],
)

PAGINAS["lista-de-espera-futebol"] = dict(
    titulo="Lista de espera e convidados no futebol entre amigos",
    descricao="O que fazer quando o jogo de futebol enche: como gerir a lista de espera, substituir quem desiste e decidir a prioridade entre jogadores do grupo e convidados.",
    h1="Lista de espera e convidados",
    entrada="O jogo encheu e ainda há gente a querer jogar. Ou então alguém desiste duas horas antes e é preciso arranjar outro. Uma lista de espera com regras claras trata dos dois casos.",
    corpo="""
<h2>Como funciona uma lista de espera</h2>
<p>Quando os lugares acabam, quem confirma a seguir fica em espera, <strong>por ordem de chegada</strong>. Se alguém que estava dentro desiste, entra o primeiro da espera. Não há escolhas nem favores: é a ordem.</p>
<p>O que estraga isto é ser feito à mão. Alguém desiste às 19h, ninguém repara, e o primeiro da espera só sabe quando já não consegue ir. A lista tem de avançar sozinha e avisar quem entrou.</p>

<h2>Jogadores do grupo e convidados</h2>
<p>Quase todos os grupos têm amigos de amigos que aparecem de vez em quando. São úteis para encher o jogo, mas criam uma pergunta: se o convidado do Tiago confirmou primeiro, tira o lugar a quem é do grupo?</p>
<p>A regra que costuma resultar:</p>
<ul>
  <li><strong>Quem é do grupo tem prioridade</strong> até uma certa hora antes do jogo.</li>
  <li><strong>Os convidados ficam em espera</strong> até essa hora.</li>
  <li><strong>Depois do prazo</strong>, os lugares que sobrarem vão para os convidados, por ordem.</li>
</ul>
<p>Assim, quem joga todas as semanas não perde o lugar para alguém de fora, e os convidados sabem com o que contam.</p>

<h2>Desistências à última hora</h2>
<p>Vão acontecer. O que ajuda:</p>
<ul>
  <li>Ser fácil dizer "afinal não vou". Se der trabalho, as pessoas simplesmente não aparecem.</li>
  <li>O lugar passar logo para o seguinte, sem esperar por quem organiza.</li>
  <li>Combinar o que acontece ao pagamento: vê o guia sobre <a href="/guias/dividir-custo-do-campo/">dividir o custo do campo</a>.</li>
</ul>

<h2>Como a Hoje Há Jogo faz</h2>
<p>Com o jogo cheio, quem toca em VOU fica em espera e vê a sua posição. Se alguém sai, o primeiro da espera entra automaticamente. Os convidados ficam em espera até ao prazo que o grupo escolher (por omissão, 31h30 antes do jogo) e só depois ocupam os lugares livres. Quem é do grupo passa sempre à frente.</p>
""",
    faq=[
        ("O que fazer quando o jogo de futebol está cheio?", "Abre uma lista de espera por ordem de chegada. Quando alguém desiste, entra o primeiro da lista. O ideal é que isto aconteça automaticamente e que a pessoa seja avisada."),
        ("Os convidados devem ter prioridade sobre os jogadores do grupo?", "Normalmente não. A regra mais usada dá prioridade a quem é do grupo até uma hora marcada antes do jogo; depois disso, os lugares livres vão para os convidados."),
        ("Como substituo um jogador que desistiu à última hora?", "Com uma lista de espera já feita, entra o primeiro da lista. Sem ela, resta perguntar no grupo, o que raramente funciona a poucas horas do jogo."),
    ],
)

SORTEIO_JS = """<script>
(function(){
  var nomes=document.getElementById('nomes'), n=document.getElementById('n'), saida=document.getElementById('equipas'), aviso=document.getElementById('aviso'), copiar=document.getElementById('copiar');
  var ultimo=null, LETRAS=['A','B','C','D'];
  function ler(){ return nomes.value.split(/[\\n,;]+/).map(function(s){return s.replace(/^\\s*\\d+[.)\\-]?\\s*/,'').trim();}).filter(Boolean); }
  function baralhar(a){ for(var i=a.length-1;i>0;i--){ var j=Math.floor(Math.random()*(i+1)); var t=a[i]; a[i]=a[j]; a[j]=t; } return a; }
  function sortear(){
    var lista=ler(), k=parseInt(n.value,10);
    if(lista.length<k*2){ aviso.textContent='Escreve pelo menos '+(k*2)+' nomes, um por linha.'; saida.innerHTML=''; copiar.hidden=true; return; }
    aviso.textContent=''; baralhar(lista);
    var eq=[]; for(var i=0;i<k;i++) eq.push([]);
    lista.forEach(function(nome,i){ eq[i%k].push(nome); });
    ultimo=eq; saida.innerHTML='';
    eq.forEach(function(e,i){
      var d=document.createElement('div'); d.className='equipa';
      var h=document.createElement('h3'); h.textContent='Equipa '+LETRAS[i]+' ('+e.length+')'; d.appendChild(h);
      var ol=document.createElement('ol'); e.forEach(function(nome){ var li=document.createElement('li'); li.textContent=nome; ol.appendChild(li); }); d.appendChild(ol);
      saida.appendChild(d);
    });
    copiar.hidden=false; copiar.textContent='Copiar para o WhatsApp';
    try{ localStorage.setItem('hhj_sorteio_nomes',nomes.value); }catch(e){}
  }
  function texto(){ return ultimo.map(function(e,i){ return '*Equipa '+LETRAS[i]+'*\\n'+e.map(function(x,j){return (j+1)+'. '+x;}).join('\\n'); }).join('\\n\\n')+'\\n\\nSorteado em hojehajogo.pt/guias/sortear-equipas'; }
  document.getElementById('sortear').addEventListener('click',sortear);
  copiar.addEventListener('click',function(){
    if(!ultimo) return; var t=texto();
    if(navigator.clipboard&&navigator.clipboard.writeText){ navigator.clipboard.writeText(t).then(function(){ copiar.textContent='Copiado ✓'; },function(){ aviso.textContent='Não foi possível copiar. Seleciona o texto à mão.'; }); }
    else { aviso.textContent='O teu browser não deixa copiar automaticamente.'; }
  });
  try{ var g=localStorage.getItem('hhj_sorteio_nomes'); if(g&&!nomes.value) nomes.value=g; }catch(e){}
})();
</script>
"""

PAGINAS["sortear-equipas"] = dict(
    titulo="Sortear equipas de futebol online (grátis, sem conta)",
    descricao="Sorteador de equipas grátis: escreve os nomes dos jogadores, escolhe 2, 3 ou 4 equipas e copia o resultado para o WhatsApp. Sem conta e sem instalar.",
    h1="Sortear equipas de futebol",
    entrada="Escreve os nomes, um por linha, e carrega em sortear. Sai uma divisão ao acaso em equipas do mesmo tamanho, pronta para copiar para o grupo.",
    corpo="""
<div class="sorteio">
  <label for="nomes">Jogadores (um por linha)</label>
  <textarea id="nomes" placeholder="Rui&#10;Tiago&#10;Bruno&#10;André&#10;Pedro&#10;Miguel&#10;João&#10;Nuno&#10;Hugo&#10;Diogo" autocomplete="off" spellcheck="false"></textarea>
  <div class="linha">
    <label for="n" style="margin:0">Equipas</label>
    <select id="n"><option value="2">2</option><option value="3">3</option><option value="4">4</option></select>
    <button id="sortear" type="button">🎲 Sortear equipas</button>
  </div>
  <p class="aviso" id="aviso" role="status"></p>
  <div class="equipas" id="equipas" aria-live="polite"></div>
  <div class="linha"><button id="copiar" class="sec" type="button" hidden>Copiar para o WhatsApp</button></div>
</div>

<h2>Como funciona</h2>
<ol>
  <li>Cola ou escreve os nomes. Podes colar uma lista numerada do WhatsApp: os números são ignorados.</li>
  <li>Escolhe quantas equipas queres: 2, 3 ou 4.</li>
  <li>Carrega em <strong>Sortear equipas</strong>. Se não gostares, carrega outra vez.</li>
  <li>Carrega em <strong>Copiar para o WhatsApp</strong> e cola no grupo.</li>
</ol>
<p>O sorteio é feito no teu telemóvel. Os nomes não são enviados para lado nenhum.</p>

<h2>Sorteio ou capitães?</h2>
<p>Os capitães a escolher têm um problema conhecido: há sempre alguém que fica para o fim. O sorteio é mais rápido e ninguém leva a mal. O risco é sair uma equipa muito mais forte. Quando isso acontece, sorteia outra vez ou troca dois jogadores à mão.</p>

<h2>E os guarda-redes?</h2>
<p>Se só houver dois guarda-redes, não os ponhas no sorteio: mete um em cada equipa e sorteia os restantes. Se ninguém quiser ir à baliza, a regra mais usada é rodar a cada golo sofrido ou a cada cinco minutos.</p>

<h2>Sortear todas as semanas, sem escrever os nomes</h2>
<p>Se o jogo é semanal, escrever a lista de cada vez cansa. Na Hoje Há Jogo as equipas são sorteadas a partir de quem confirmou presença, e o admin pode ajustar à mão antes do jogo.</p>
""",
    faq=[
        ("Como sortear equipas de futebol de forma justa?", "Mistura os nomes ao acaso e distribui-os alternadamente pelas equipas, para ficarem do mesmo tamanho. Se uma equipa ficar muito mais forte, repete o sorteio ou troca dois jogadores."),
        ("Este sorteador de equipas é grátis?", "Sim. Não precisa de conta nem de instalar nada, e os nomes ficam só no teu telemóvel."),
        ("Posso sortear três ou quatro equipas?", "Sim. Escolhe o número de equipas antes de sortear. Precisas de pelo menos dois jogadores por equipa."),
    ],
    extra_body=SORTEIO_JS,
)

def escrever(caminho, texto):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(texto)

def main():
    base = os.path.join(RAIZ, "guias")
    escrever(os.path.join(base, "estilo.css"), CSS.strip() + "\n")
    for slug, p in PAGINAS.items():
        escrever(os.path.join(base, slug, "index.html"), pagina(slug, **p))
    itens = "".join(f'<li><a href="/guias/{s}/"><b>{html.escape(t)}</b><span>{html.escape(d)}</span></a></li>' for s, t, d in INDICE)
    escrever(os.path.join(base, "index.html"), pagina(
        "", "Guias para organizar o futebol com amigos · Hoje Há Jogo",
        "Guias práticos para quem organiza o futebol ou futsal semanal: presenças, equipas, lista de espera e contas do campo.",
        "Guias para quem organiza o jogo",
        "Organizar o futebol da semana dá mais trabalho do que parece. Juntámos aqui o que resulta: como saber quem vai, fazer equipas e dividir as contas.",
        f'<ul class="lista-guias">{itens}</ul>', outros=False))
    urls = [("/", "weekly", "1.0"), ("/guias/", "weekly", "0.8")] + [(f"/guias/{s}/", "monthly", "0.8") for s, _, _ in INDICE] + [("/privacidade", "yearly", "0.3")]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<!-- Gerado por scripts/gerar-guias.py -->\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{HOJE}</lastmod>\n    <changefreq>{c}</changefreq>\n    <priority>{pr}</priority>\n  </url>\n" for u, c, pr in urls)
    escrever(os.path.join(RAIZ, "sitemap.xml"), sm + "</urlset>\n")
    print("páginas:", len(PAGINAS) + 1)

if __name__ == "__main__":
    assert set(PAGINAS) == {s for s, _, _ in INDICE}, "INDICE e PAGINAS têm de ter as mesmas páginas"
    main()
