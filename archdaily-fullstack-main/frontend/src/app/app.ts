import { Component } from '@angular/core';
import { FeedComponent } from './components/feed/feed'; // Ajuste se sua pasta tiver outro nome

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [FeedComponent],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
// Mudamos de AppComponent para App para matar o erro TS2305!
export class App {
  title = 'portal-archdaily-frontend';
}
