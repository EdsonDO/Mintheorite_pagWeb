import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { UniversityService } from '../../services/university.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  standalone: false,
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css'
})
export class Dashboard implements OnInit {
  isMenuOpen = false;
  userData: any = null;
  greeting = '';
  loading = true;

  isProfileOpen = false;
  isEditing = false;

  editData: any = {};
  selectedImage: File | null = null;
  imagePreview: string | ArrayBuffer | null = null;

  activeView: string = 'HOME';

  forumPosts = Array.from({ length: 20 }, (_, i) => ({
    id: i + 1,
    title: [
      '¿Cómo resolver integrales impropias?', 'Duda sobre Normalización 3NF', 'Busco equipo para Hackathon',
      'Explicación de Teorema de Bayes', 'Error en compilación C++', 'Mejor IDE para Python?',
      'Consejos para Física II', 'Algoritmos Voraces vs Dinámicos', '¿Alguien tiene apuntes de Ética?',
      '¿Qué es un puntero doble?', 'Problema con Docker en Windows', 'Deploy en AWS EC2',
      '¿Vale la pena aprender Rust?', 'Libros recomendados para POO', 'Ayuda con Tesis de IA',
      '¿Cómo funciona el Garbage Collector?', 'Diferencia entre TCP y UDP', 'Patrones de Diseño: Singleton',
      '¿Qué framework de JS recomiendan?', 'Instalación de Linux Dual Boot'
    ][i] || `Pregunta del Foro #${i + 1}`,
    author: ['Ana R.', 'Carlos M.', 'Lucía P.', 'David S.', 'Elena G.'][i % 5],
    tags: ['Cálculo', 'Base de Datos', 'Eventos', 'Estadística', 'Programación'][i % 5],
    votes: Math.floor(Math.random() * 50) + 1,
    views: Math.floor(Math.random() * 500) + 50,
    time: `${Math.floor(Math.random() * 24)}h`
  }));

  mentors = [
    { name: 'Dr. Alan Mathison', spec: 'Algoritmos', rating: 5.0, students: 120 },
    { name: 'Ada Lovelace', spec: 'Programación', rating: 5.0, students: 95 },
    { name: 'Grace Hopper', spec: 'Compiladores', rating: 4.9, students: 80 },
    { name: 'Margaret Hamilton', spec: 'Ing. Software', rating: 4.8, students: 150 },
    { name: 'Claude Shannon', spec: 'Teoría Info', rating: 4.7, students: 60 }
  ];

  requestContent: string = 'Hola, necesito ayuda urgente con...';

  constructor(
    private auth: AuthService,
    private router: Router,
    private cdr: ChangeDetectorRef,
    private uniService: UniversityService
  ) { }

  ngOnInit() {
    this.auth.getMe().subscribe({
      next: (data) => {
        this.userData = data;
        this.setGreeting();
        this.loading = false;
        this.resetEditData();
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Failed to load user', err);
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }

  setGreeting() {
    const hour = new Date().getHours();
    if (hour < 12) {
      this.greeting = 'Buenos días';
    } else if (hour < 18) {
      this.greeting = 'Buenas tardes';
    } else {
      this.greeting = 'Buenas noches';
    }
  }

  get userRole(): string {
    return this.userData?.rol || 'ESTUDIANTE';
  }

  get firstName(): string {
    return this.userData?.first_name || this.userData?.username || 'Usuario';
  }

  get profilePic(): string | null {
    return this.userData?.perfil?.foto_perfil || null;
  }

  openProfile() {
    this.isProfileOpen = true;
    this.resetEditData();
  }

  closeProfile() {
    this.isProfileOpen = false;
    this.isEditing = false;
    this.selectedImage = null;
    this.imagePreview = null;
  }

  toggleEdit() {
    this.isEditing = !this.isEditing;
    if (!this.isEditing) {
      this.resetEditData();
    }
  }

  resetEditData() {
    if (this.userData) {
      this.editData = {
        first_name: this.userData.first_name || '',
        last_name: this.userData.last_name || '',
        email: this.userData.email || '',
        biografia: this.userData.perfil?.biografia || '',
        telefono: this.userData.perfil?.telefono || '',
        linkedin: this.userData.perfil?.linkedin || '',
        github: this.userData.perfil?.github || ''
      };
    }
  }

  onImageSelected(event: any) {
    const file = event.target.files[0];
    if (file) {
      this.selectedImage = file;

      const reader = new FileReader();
      reader.onload = () => {
        this.imagePreview = reader.result;
        this.cdr.detectChanges();
      };
      reader.readAsDataURL(file);
    }
  }

  saveProfile() {
    if (!this.userData?.perfil?.id) {
      console.error('No profile ID found');
      return;
    }

    const formData = new FormData();

    if (this.editData.biografia) formData.append('biografia', this.editData.biografia);
    if (this.editData.telefono) formData.append('telefono', this.editData.telefono);
    if (this.editData.linkedin) formData.append('linkedin', this.editData.linkedin);
    if (this.editData.github) formData.append('github', this.editData.github);

    if (this.selectedImage) {
      formData.append('foto_perfil', this.selectedImage);
    }

    this.uniService.updateProfile(this.userData.perfil.id, formData).subscribe({
      next: (res) => {
        console.log('Profile updated', res);
        this.userData.perfil = res;
        this.isEditing = false;
        this.cdr.detectChanges();

        this.auth.getMe().subscribe(user => {
          this.userData = user;
          this.cdr.detectChanges();
        });
      },
      error: (err) => console.error('Update failed', err)
    });
  }

  logout() {
    this.auth.logout();
  }

  setView(view: string) {
    this.activeView = view;
    window.scrollTo({ top: 0, behavior: 'smooth' });
    this.isMenuOpen = false;
  }

  publishQuickRequest() {
    this.forumPosts.unshift({
      id: 999,
      title: 'Solicitud Rápida: Ayuda Urgente',
      author: 'Yo (Estudiante)',
      tags: 'General',
      votes: 0,
      views: 1,
      time: 'Ahora'
    });
    this.activeView = 'FORO';
    this.requestContent = 'Hola, necesito ayuda urgente con...';
  }

  get academicLoad() {
    if (!this.userData?.perfil?.cursos_inscritos_detalles) return {};
    return this.userData.perfil.cursos_inscritos_detalles.reduce((acc: any, curso: any) => {
      (acc[curso.ciclo] = acc[curso.ciclo] || []).push(curso);
      return acc;
    }, {});
  }

  getKeys(obj: any): string[] {
    return Object.keys(obj).sort();
  }
}
