# 🏛️ ArchDaily Fullstack Pipeline & Live Portal

Este é um projeto fullstack moderno que realiza a raspagem de dados (*web scraping*) das notícias mais recentes do portal **ArchDaily** e as exibe em uma interface responsiva, elegante e minimalista desenvolvida em **Angular**.

O grande diferencial técnico deste projeto é a sua arquitetura de **Monorepo Serverless**: em vez de depender de arquivos estáticos gerados por tarefas agendadas ou manter um servidor ativo 24/7, a aplicação utiliza funções serverless em nuvem. Quando o usuário abre o portal, o Angular faz uma requisição para uma API em Python que raspa e entrega os dados em tempo real.

---

## 🛠️ Tecnologias Utilizadas

### **Backend & API Serverless**
* **Python 3.x:** Linguagem utilizada para construir o motor lógico de raspagem.
* **BeautifulSoup4 & Requests:** Bibliotecas responsáveis pela requisição HTTP e extração cirúrgica dos dados (títulos, imagens, links e tags) do portal original.
* **Vercel Serverless Functions:** Tecnologias que transformam o script Python em uma API viva de execução instantânea e sob demanda, exposta na rota `/api`.

### **Frontend**
* **Angular:** Framework utilizado para construir uma aplicação SPA (*Single Page Application*) robusta, performática e fortemente componentizada.
* **TypeScript:** Garantia de tipagem estática, segurança de dados e contratos de interface limpos para o consumo da API.
* **CSS Moderno / Tailwind CSS:** Layout responsivo focado na estética limpa e geométrica característica de grandes portais de arquitetura.

---

## 📐 Arquitetura do Projeto e Fluxo de Dados

A engenharia do projeto foi desenhada utilizando o conceito de **Monorepo** gerenciado pelo ecossistema da Vercel, separando completamente as responsabilidades de Frontend e Backend:

[ Usuário ] ───► Consome Interface (SPA) ───► [ Angular Frontend ]
│
Dispara fetch('/api')
│
▼
[ Resposta JSON ] ◄── Excuta Raspagem ◄─── [ API Serverless (Python) ]
no ArchDaily

1. **Requisição Sob Demanda:** O usuário acessa o portal e o componente de feed do Angular (`FeedComponent`) dispara um `fetch()` assíncrono para a rota relativa `/api`.
2. **Invocação Serverless:** A Vercel intercepta a rota `/api` com base nas regras do `vercel.json` e acorda a função serverless em Python (`api/index.py`) de forma instantânea.
3. **Live Scraping & Resposta:** O script Python faz a varredura em tempo real no ArchDaily, estrutura os dados em um dicionário, converte para JSON e responde ao cliente aplicando os cabeçalhos de CORS.
4. **Renderização Reativa:** O Angular recebe o JSON puro, atualiza o estado do componente pai e renderiza dinamicamente os cartões visuais (`NewsCardComponent`) na tela através da diretiva estrutural `*ngFor`.

---

## 📁 Estrutura do Repositório (Monorepo)

archdaily-fullstack/
├── api/
│   ├── index.py             # API Backend Serverless em Python (Web Scraper Vivo)
│   └── requirements.txt     # Dependências de execução do motor Python na nuvem
├── frontend/
│   ├── src/
│   │   ├── app/             # Componentes modulares do Angular (Feed, NewsCard)
│   │   └── index.html       # Arquivo principal de montagem da SPA
│   ├── package.json         # Scripts de build e dependências do ecossistema Angular
│   └── angular.json         # Configurações de compilação do framework
└── vercel.json              # Orquestrador global de build, runtimes e reescrita de rotas

⚙️ Configuração de Infraestrutura (Vercel)
Para reproduzir este deploy mantendo as tecnologias isoladas na raiz do repositório, o arquivo de configuração global vercel.json instrui o servidor com builders explícitos:
Backend Builder: Utiliza o runtime @vercel/python mapeando o ponto de entrada em api/index.py.
Frontend Builder: Utiliza o runtime @vercel/static-build para compilar o Angular e aponta a pasta de saída para o diretório de distribuição (dist/).
Router Rewrites: Encaminha requisições de /api para o motor Python, enquanto delega as demais rotas para a index do ecossistema Angular.
