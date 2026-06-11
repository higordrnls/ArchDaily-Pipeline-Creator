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
      console.log("🔍 Buscando noticias.json...");
      const resposta = await fetch('noticias.json');

      if (!resposta.ok) {
        throw new Error(`Erro: ${resposta.status}`);
      }

      this.noticias = await resposta.json();
      console.log("📰 Notícias carregadas no componente:", this.noticias);

      // Força o HTML a desenhar
      this.cdr.detectChanges();

    } catch (erro) {
      console.error("❌ Erro ao ler o JSON:", erro);
    }
  }
}
