import { Component, OnInit, ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-welcome',
  standalone: false,
  templateUrl: './welcome.html',
  styleUrls: ['./welcome.css'],
})
export class Welcome implements OnInit {

  fullText = "Una plataforma diseñada para la excelencia. Conecta estudiantes, mentores y conocimiento en un ecosistema digital unificado.";
  displayedText = "";

  constructor(private cd: ChangeDetectorRef) { }

  ngOnInit() {
    this.typeText();
  }

  typeText() {
    let index = 0;
    const interval = setInterval(() => {
      if (index < this.fullText.length) {
        this.displayedText += this.fullText.charAt(index);
        index++;
        this.cd.detectChanges();
      } else {
        clearInterval(interval);
      }
    }, 30); // Speed: 30ms per char
  }

}
