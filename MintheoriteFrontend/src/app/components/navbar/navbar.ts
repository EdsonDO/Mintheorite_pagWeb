import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.html',
  standalone: false,
  styleUrl: './navbar.css'
})
export class Navbar implements OnInit {
  username = localStorage.getItem('username') || 'Usuario';
  displayName = '';

  constructor(private auth: AuthService, private cd: ChangeDetectorRef) { }

  ngOnInit() {
    this.auth.getMe().subscribe({
      next: (user) => {
        console.log('NAVBAR USER:', user);
        this.displayName = user.first_name || user.username;
        this.username = this.displayName;
        this.cd.detectChanges();
      },
      error: (err) => {
        console.error('Navbar ME failed', err);
        this.displayName = this.username;
        this.cd.detectChanges();
      }
    });
  }

  logout() {
    this.auth.logout();
  }
}
