import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common'; // <-- ISSO AQUI É OBRIGATÓRIO!
import { NewsCardComponent } from '../news-card/news-card';

@Component({
  selector: 'app-feed',
  standalone: true,
  imports: [CommonModule, NewsCardComponent], // <-- GARANTA O COMMONMODULE AQUI!
  templateUrl: './feed.html',
  styleUrls: ['./feed.css']
})
export class FeedComponent implements OnInit {
  noticias: any[] = [];

  constructor(private cdr: ChangeDetectorRef) {}

  async ngOnInit() {
    try {
      console.log("🔍 Chamando a API viva em Python...");
      // Mudamos de 'noticias.json' para '/api' para buscar direto do robô em tempo real!
      const resposta = await fetch('/api');

      if (!resposta.ok) {
        throw new Error(`Erro: ${resposta.status}`);
      }

      this.noticias = await resposta.json();
      console.log("📰 Notícias atualizadas carregadas com sucesso:", this.noticias);

      // Força o HTML a desenhar
      this.cdr.detectChanges();

    } catch (erro) {
      console.error("❌ Erro ao ler a API Python:", erro);
    }
  }
}
