# 🏛️ ArchDaily Fullstack Pipeline & Portal

Este é um projeto fullstack automatizado que realiza a raspagem de dados (web scraping) das notícias mais recentes do portal **ArchDaily**, processa e estrutura as informações através de um script Python, e as exibe em uma interface responsiva e moderna desenvolvida em **Angular**.

O grande diferencial do projeto é a sua arquitetura **Serverless & Automotiva**: o scraper roda de forma 100% autônoma na nuvem através do GitHub Actions (via Cron Job) e atualiza os dados diretamente no ecossistema da aplicação frontend.

---

## 🛠️ Tecnologias Utilizadas

### **Backend & Automação**
* **Python 3.x:** Linguagem base para o script de automação.
* **BeautifulSoup4 & Requests:** Responsáveis pela requisição HTTP e extração cirúrgica dos dados do portal ArchDaily.
* **GitHub Actions:** Utilizado para criar o pipeline de CI/CD e rodar o script de raspagem periodicamente via tarefas agendadas (Cron).

### **Frontend**
* **Angular:** Framework utilizado para construir uma aplicação SPA (Single Page Application) robusta, performática e componentizada.
* **TypeScript:** Garantia de tipagem estática e segurança no consumo dos dados raspados.
* **Tailwind CSS / CSS Moderno:** Layout responsivo focado na experiência de leitura do usuário, simulando a estética minimalista de portais de arquitetura.

---

## 📐 Arquitetura do Projeto e Fluxo de Dados

A engenharia do projeto foi desenhada para eliminar a necessidade de manter um servidor de banco de dados ativo 24/7, reduzindo custos de infraestrutura e otimizando o tempo de resposta:

1. **Agendamento (Cron):** O GitHub Actions ativa o container Python de forma automatizada em intervalos programados.
2. **Raspagem (Scraper):** O script Python varre o portal do ArchDaily capturando títulos, links, imagens de destaque, categorias e datas das notícias.
3. **Persistência Estática:** Os dados extraídos são validados e injetados diretamente na pasta pública do Angular (`frontend/src/public/noticias.json`).
4. **Entrega Automática:** O pipeline realiza o commit dessas mudanças de volta ao repositório, disparando o deploy automático para os usuários finais.
5. **Consumo Rápido:** O frontend Angular consome o arquivo JSON de forma estática instantânea, entregando performance máxima de carregamento.

---

## 📁 Estrutura do Repositório

```text
archdaily-fullstack/
├── .github/
│   └── workflows/
│       └── cron.yml          # Configuração do robô agendado do GitHub
├── backend/
│   ├── scraper.py            # Script Python de extração de dados (Web Scraper)
│   └── requirements.txt      # Dependências do motor Python
└── frontend/
    ├── src/
    │   ├── app/              # Componentes e serviços do Angular
    │   └── public/
    │       └── noticias.json # Banco de dados estático atualizado pelo robô
    ├── package.json          # Dependências e scripts do ecossistema Angular
    └── angular.json          # Configurações globais do Framework****
