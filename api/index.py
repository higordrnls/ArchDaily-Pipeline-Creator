import json
import requests
from bs4 import BeautifulSoup
import time
from http.server import BaseHTTPRequestHandler

# URL da página inicial do ArchDaily Brasil
URL = "https://www.archdaily.com.br/br"

def raspar_noticias():
    print("🤖 Iniciando o robô raspador PROFISSIONAL E INFALÍVEL do ArchDaily...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8"
    }
    
    try:
        resposta = requests.get(URL, headers=headers)
        if resposta.status_code != 200:
            print(f"❌ Erro ao acessar o site: Status {resposta.status_code}")
            return []
            
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

            # --- Entrada na página interna do post ---
            if link != "#":
                try:
                    time.sleep(0.3) # Micro pausa estratégica
                    resposta_interna = requests.get(link, headers=headers)
                    if resposta_interna.status_code == 200:
                        soup_interno = BeautifulSoup(resposta_interna.text, 'html.parser')
                        
                        meta_img = soup_interno.find("meta", property="og:image")
                        if meta_img and meta_img.get('content'):
                            link_imagem = meta_img.get('content')
                        else:
                            img_interna = soup_interno.find('picture') or soup_interno.find('div', class_='article-header-image')
                            if img_interna:
                                img_tag = img_interna.find('img')
                                if img_tag:
                                    link_imagem = img_tag.get('src') or img_tag.get('data-src')
                except Exception as e_interno:
                    print(f"⚠️ Erro na página interna {index+1}: {e_interno}")

            if not link_imagem or "logo" in link_imagem.lower() or link_imagem.startswith('data:image'):
                link_imagem = f"https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=500&sig={index + 20}"

            noticia = {
                "titulo": titulo,
                "imagem": link_imagem,
                "tag": "Destaque",
                "link": link
            }
            noticias_raspadas.append(noticia)
            print(f"✅ [{index+1}] Coletado: {titulo[:30]}...")

        return noticias_raspadas

    except Exception as e:
        print(f"💥 Erro na execução: {e}")
        return []

# --- ESSA É A ESTRUTURA QUE A VERCEL EXIGE PARA CONECTAR COM O PYTHON ---
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Executa o raspador e pega a lista de notícias atualizada
        dados_noticias = raspar_noticias()
        
        # Envia a resposta de sucesso para o navegador/Angular
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Habilita o CORS para o Angular conseguir ler a API sem bloqueios de segurança
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        # Converte a lista do Python para texto JSON e responde
        resultado_final = json.dumps(dados_noticias, ensure_ascii=False, indent=2)
        self.wfile.write(resultado_final.encode('utf-8'))