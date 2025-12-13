import { Component } from '@angular/core';

@Component({
    selector: 'app-footer',
    templateUrl: './footer.html',
    styleUrls: ['./footer.css'],
    standalone: false
})
export class FooterComponent {
    currentYear = new Date().getFullYear();
}
