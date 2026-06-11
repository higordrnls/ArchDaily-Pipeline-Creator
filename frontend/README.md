# 🏛️ ArchDaily Data Pipeline & Portal

Este projeto é um ecossistema completo que une engenharia de dados e desenvolvimento de interface para criar um portal automatizado de notícias de arquitetura. Ele é composto por um robô minerador em **Python** no backend e uma aplicação reativa em **Angular** no frontend.

---

## ⚙️ Como o Ecossistema Funciona

O projeto funciona de forma integrada através de um pipeline local de dados estruturados:

1. **Backend (Python):** O script `scraper.py` faz o web scraping do portal ArchDaily Brasil. Ele entra nos links das matérias para capturar de forma certeira os títulos e as URLs oficiais das imagens de capa em alta resolução.
2. **Pipeline de Dados:** O robô gera e exporta dinamicamente um arquivo chamado `noticias.json` diretamente para a pasta pública do frontend.
3. **Frontend (Angular):** A interface consome esse JSON local de forma assíncrona e renderiza um feed de cards modernos e responsivos.

---

## 🛠️ Tecnologias Utilizadas

### Backend:
- **Python 3**
- **BeautifulSoup4** (Análise e extração do HTML)
- **Requests** (Requisições HTTP com emulação de User-Agent)

### Frontend:
- **Angular** (Arquitetura de componentes Standalone)
- **TypeScript** (Controle de fluxo e tipagem)
- **HTML5 & CSS3** (Layout limpo com Flexbox)

---

## 🏃‍♂️ Como Rodar O Projeto Localmente

### 🐍 1. Executando o Robô (Python)
Navegue até a pasta do seu script Python, garanta que suas dependências estão instaladas e rode o comando abaixo para criar e atualizar o arquivo `noticias.json` com os dados e imagens reais do ArchDaily:
python scraper.py

🅰️ 2. Executando a Interface (Angular)
Abra o terminal na raiz do projeto frontend e siga os comandos para instalar as dependências e iniciar o servidor de desenvolvimento:
npm install
ng serve
Agora, abra o seu navegador e acesse: http://localhost:4200/

📂 Estrutura Principal Desenvolvida
scraper.py: Script automatizado de mineração com tratamento de exceções e varredura de metadados (og:image).
src/app/app.ts: Ponto de entrada modularizado configurado para carregar o feed principal.
src/app/app.html & src/app/app.css: Estrutura de layout global e cabeçalho estilizado de forma minimalista.

<img width="308" height="649" alt="image" src="https://github.com/user-attachments/assets/8a00e47a-34fa-4003-915e-4707ee0d2788" />
