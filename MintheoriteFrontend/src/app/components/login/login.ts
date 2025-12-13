import { Component, ChangeDetectorRef } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.html',
  standalone: false,
  styleUrl: './login.css'
})
export class Login {
  username = '';
  password = '';
  errorMessage = '';

  constructor(private auth: AuthService, private cd: ChangeDetectorRef) { }

  onLogin() {
    this.errorMessage = '';
    console.time('LoginRequest');

    this.auth.login(this.username, this.password).subscribe({
      next: () => {
        console.timeEnd('LoginRequest');
      },
      error: (err) => {
        console.timeEnd('LoginRequest');
        console.error('Login Failed:', err);

        if (err.error && typeof err.error === 'object') {
          const messages = Object.values(err.error).flat();
          this.errorMessage = messages.join(' ');
        } else {
          this.errorMessage = 'Credenciales inválidas. Intenta de nuevo.';
        }

        this.cd.detectChanges();
      }
    });
  }
}
