import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
    selector: 'app-role-selector',
    standalone: false,
    templateUrl: './role-selector.html',
    styleUrls: ['./role-selector.css']
})
export class RoleSelector {

    constructor(private router: Router) { }

    selectRole(role: 'ESTUDIANTE' | 'MENTOR') {
        this.router.navigate(['/register'], { queryParams: { rol: role } });
    }
}
