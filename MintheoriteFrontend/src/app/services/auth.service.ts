import { Injectable, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, switchMap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface LoginResponse {
    token: string;
}

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private apiUrl = environment.apiUrl;
    isAuthenticated = signal<boolean>(!!localStorage.getItem('token'));

    constructor(private http: HttpClient, private router: Router) { }

    login(username: string, password: string): Observable<any> {
        return this.http.post<LoginResponse>(`${this.apiUrl}/api-token-auth/`, { username, password })
            .pipe(
                tap(response => {
                    localStorage.setItem('token', response.token);
                    localStorage.setItem('username', username);
                    this.isAuthenticated.set(true);
                }),
                switchMap(() => {
                    console.log('Login successful, fetching profile...');
                    return this.getMe();
                }),
                tap(user => {
                    console.log('User fetched for redirect check:', user);
                    if (user && user.perfil && user.perfil.carrera) {
                        console.log('Profile completed (Carrera set), going to Dashboard.');
                        this.router.navigate(['/app']);
                    } else {
                        console.log('Incomplete profile (No Carrera), triggering Onboarding.');
                        this.router.navigate(['/onboarding']);
                    }
                })
            );
    }

    register(userData: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/usuarios/`, userData);
    }

    getProfile(username: string): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/usuarios/?username=${username}`);
    }

    getMe(): Observable<any> {
        return this.http.get<any>(`${this.apiUrl}/usuarios/me/`);
    }

    logout() {
        localStorage.removeItem('token');
        this.isAuthenticated.set(false);
        this.router.navigate(['/welcome']);
    }
}
