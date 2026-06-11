import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-news-card',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './news-card.html',
  styleUrls: ['./news-card.css']
})
export class NewsCardComponent {
  // O @Input avisa pro Angular que essa propriedade vem lá do Feed!
  @Input() noticia: any;
}
