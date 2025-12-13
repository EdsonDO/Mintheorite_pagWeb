import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.html',
  standalone: false,
  styleUrl: './register.css'
})
export class Register implements OnInit {
  userData = {
    username: '',
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    rol: 'ESTUDIANTE'
  };
  errorMessage = '';

  constructor(private auth: AuthService, private router: Router, private route: ActivatedRoute) { }

  ngOnInit() {
    this.route.queryParams.subscribe(params => {
      if (params['rol']) {
        this.userData.rol = params['rol'];
      }
    });
  }

  onRegister() {
    this.auth.register(this.userData).subscribe({
      next: () => {
        this.router.navigate(['/login']);
      },
      error: (err) => {
        if (err.error && typeof err.error === 'object') {
          const messages = Object.values(err.error).flat();
          this.errorMessage = messages.join(' ');
        } else {
          this.errorMessage = 'Error en el registro. Intenta de nuevo.';
        }
        console.error(err);
      }
    });
  }
}
