import os
import sys

# Garante que o Python enxergue a pasta src
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.database import inicializar_banco, salvar_noticias_no_banco
from src.scraper import rodar_scraper

def main():
    print("🚀 Iniciando o pipeline ArchDaily...")
    inicializar_banco()
    dados_raspados = rodar_scraper()
    salvar_noticias_no_banco(dados_raspados)

if __name__ == "__main__":
    main()