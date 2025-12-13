import { Component, OnInit, signal, ChangeDetectorRef } from '@angular/core';
import { UniversityService } from '../../services/university.service';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-onboarding',
  standalone: false,
  templateUrl: './onboarding.html',
  styleUrls: ['./onboarding.css']
})
export class Onboarding implements OnInit {
  step = signal(1);
  username = localStorage.getItem('username') || 'Usuario';
  rol = 'ESTUDIANTE';

  universities: any[] = [];
  faculties: any[] = [];
  careers: any[] = [];
  courses: any[] = [];

  selectedUni: any = null;
  selectedFaculty: any = null;
  selectedCareer: any = null;
  selectedCourses: any[] = [];

  constructor(
    private uniService: UniversityService,
    private auth: AuthService,
    private router: Router,
    private cd: ChangeDetectorRef
  ) { }

  ngOnInit() {
    this.uniService.getUniversities().subscribe(data => this.universities = data);

    this.auth.getMe().subscribe({
      next: (user) => {
        console.log('ONBOARDING ME CHECK:', user);
        this.username = user.first_name || user.username;
        this.rol = user.rol || 'ESTUDIANTE';
        this.cd.detectChanges();
      },
      error: (err) => {
        console.error('ONBOARDING ME FAILED:', err);
      }
    });
  }

  nextStep() {
    this.step.update(v => v + 1);
  }

  selectUni(uni: any) {
    this.selectedUni = uni;
    this.uniService.getFaculties(uni.id).subscribe(data => {
      this.faculties = data;
      this.nextStep();
    });
  }

  onFacultyChange() {
    if (this.selectedFaculty) {
      this.uniService.getCareers(this.selectedFaculty.id).subscribe(data => this.careers = data);
    }
  }

  selectCareer(car: any) {
    this.selectedCareer = car;
    this.uniService.getCourses().subscribe(data => {
      this.courses = data.filter((c: any) => c.carrera === car.id || c.carrera_id === car.id);
      this.nextStep();
    });
  }

  toggleCourse(course: any) {
    const index = this.selectedCourses.findIndex(c => c.id === course.id);
    if (index > -1) {
      this.selectedCourses.splice(index, 1);
    } else {
      this.selectedCourses.push(course);
    }
  }

  isCourseSelected(course: any): boolean {
    return this.selectedCourses.some(c => c.id === course.id);
  }

  completeOnboarding() {
    this.nextStep();

    this.auth.getMe().subscribe({
      next: (user) => {
        const updateData = {
          carrera: this.selectedCareer.id,
          carrera_id: this.selectedCareer.id,
          cursos_inscritos: this.selectedCourses.map(c => c.id)
        };

        if (user.perfil) {
          const perfilId = user.perfil.id;
          console.log('Profile exists, updating:', perfilId);

          this.uniService.updateProfile(perfilId, updateData).subscribe({
            next: (res) => this.handleSuccess(res),
            error: (err) => this.handleError(err)
          });
        }
        else {
          console.warn('Profile missing. Attempting to create new profile...');
          const createData = {
            usuario: user.id,
            ...updateData
          };

          this.uniService.createProfile(createData).subscribe({
            next: (res) => this.handleSuccess(res),
            error: (err) => this.handleError(err)
          });
        }
      },
      error: (err) => {
        console.warn('User not found (ME failed), redirecting...', err);
        setTimeout(() => this.router.navigate(['/app']), 3000);
      }
    });
  }

  handleSuccess(res: any) {
    console.log('Onboarding Success:', res);
    setTimeout(() => {
      this.router.navigate(['/app']);
    }, 3000);
  }

  handleError(err: any) {
    console.error('Onboarding Error:', err);
    setTimeout(() => {
      this.router.navigate(['/app']);
    }, 3000);
  }

  forceFinish() {
    this.router.navigate(['/app']);
  }
}
