import json
import requests
from bs4 import BeautifulSoup
import os # <-- Adicionamos isso para o Python saber criar pastas
import time

# URL da página inicial do ArchDaily Brasil
URL = "https://www.archdaily.com.br/br"

def raspar_noticias():
    print("🤖 Iniciando o robô raspador PROFISSIONAL E INFALÍVEL do ArchDaily...")
    
    # Fingindo ser um navegador real para evitar bloqueios
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
    }
    
    try:
        resposta = requests.get(URL, headers=headers)
        if resposta.status_code != 200:
            print(f"❌ Erro ao acessar o site: Status {resposta.status_code}")
            return
            
        soup = BeautifulSoup(resposta.text, 'html.parser')
        noticias_raspadas = []

        # Buscar os blocos de link que contêm títulos de notícias
        links_noticias = soup.find_all('a', class_='stream-item__title-link')
        
        if not links_noticias:
            links_noticias = soup.find_all('a', class_='afd-news-item__title-link')
            
        if not links_noticias:
            links_noticias = [tag.find('a') for tag in soup.find_all(['h2', 'h3']) if tag.find('a')]

        # Filtra e pega os 6 primeiros válidos
        links_noticias = [lk for lk in links_noticias if lk][:6]

        print(f"🔍 Encontramos {len(links_noticias)} posts. Entrando em cada um para buscar a foto de capa real...")

        for index, link_tag in enumerate(links_noticias):
            titulo = link_tag.text.strip()
            if not titulo or len(titulo) < 10:
                continue

            link = link_tag['href'] if link_tag.has_attr('href') else "#"
            if link.startswith('/'):
                link = f"https://www.archdaily.com.br{link}"

            link_imagem = None

            # --- ESTRATÉGIA MÁGICA: Entra na página interna do post para pegar a foto oficial ---
            if link != "#":
                try:
                    # Dá uma micro pausa de 0.5 segundos para o site não bloquear o robô
                    time.sleep(0.5)
                    
                    resposta_interna = requests.get(link, headers=headers)
                    if resposta_interna.status_code == 200:
                        soup_interno = BeautifulSoup(resposta_interna.text, 'html.parser')
                        
                        # Procria a imagem de destaque principal do artigo interno (geralmente fica numa tag meta ou imagem grande)
                        meta_img = soup_interno.find("meta", property="og:image")
                        if meta_img and meta_img.get('content'):
                            link_imagem = meta_img.get('content')
                        else:
                            # Se não achar a meta tag, pega a primeira imagem grande do artigo
                            img_interna = soup_interno.find('picture') or soup_interno.find('div', class_='article-header-image')
                            if img_interna:
                                img_tag = img_interna.find('img')
                                if img_tag:
                                    link_imagem = img_tag.get('src') or img_tag.get('data-src')
                except Exception as e_interno:
                    print(f"⚠️ Não consegui acessar a página interna da notícia {index+1}: {e_interno}")

            # Se tudo falhar ou não achar imagem interna, usa o backup lindo do Unsplash (com IDs diferentes)
            if not link_imagem or "logo" in link_imagem.lower() or link_imagem.startswith('data:image'):
                link_imagem = f"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=500&sig={index + 20}"

            noticia = {
                "titulo": titulo,
                "imagem": link_imagem,
                "tag": "Destaque",
                "link": link
            }
            noticias_raspadas.append(noticia)
            print(f"✅ [{index+1}] Coletado com SUCESSO REAL: {titulo[:45]}...")

       # -----------------------------------------------------------------
        # PASTA PÚBLICA DO ANGULAR (Caminho Relativo Automático):
        # -----------------------------------------------------------------
        # os.path.dirname(__file__) pega a pasta atual onde o scraper.py está (backend).
        # ".." volta uma pasta (para a raiz) e depois entra em frontend/src/public.
        base_dir = os.path.dirname(__file__)
        pasta_publica = os.path.abspath(os.path.join(base_dir, "..", "frontend", "src", "public"))
        pasta_principal_angular = os.path.abspath(os.path.join(base_dir, "..", "frontend"))
        
        if not os.path.exists(pasta_principal_angular):
            print("❌ Alerta: Não encontrei a pasta principal do Angular no caminho especificado!")
            
        os.makedirs(pasta_publica, exist_ok=True)

        # Caminho final do arquivo json
        caminho_final = os.path.join(pasta_publica, "noticias.json")

        # Salva o arquivo de verdade no lugar certinho
        with open(caminho_final, 'w', encoding='utf-8') as f:
            json.dump(noticias_raspadas, f, ensure_ascii=False, indent=2)
            
        print(f"💾 Sucesso absoluto! Dados entregues na pasta pública do Angular!")

    except Exception as e:
        print(f"💥 Erro na execução: {e}")

if __name__ == "__main__":
    raspar_noticias()