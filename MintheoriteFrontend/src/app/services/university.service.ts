import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class UniversityService {
    private apiUrl = environment.apiUrl;

    constructor(private http: HttpClient) { }

    getUniversities(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/universidades/`);
    }

    getFaculties(uniId: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/facultades/`);
    }

    getCareers(facultadId: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/carreras/`);
    }

    getCourses(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/cursos/`);
    }

    updateProfile(perfilId: number, data: any): Observable<any> {
        return this.http.patch(`${this.apiUrl}/perfiles/${perfilId}/`, data);
    }

    createProfile(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/perfiles/`, data);
    }
}
