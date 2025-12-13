import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Welcome } from './components/welcome/welcome';
import { Dashboard } from './components/dashboard/dashboard';
import { Login } from './components/login/login';
import { Register } from './components/register/register';
import { Onboarding } from './components/onboarding/onboarding';
import { RoleSelector } from './components/role-selector/role-selector';
import { authGuard } from './auth-guard';

const routes: Routes = [
  { path: 'welcome', component: Welcome },
  { path: 'join', component: RoleSelector },
  { path: 'login', component: Login },
  { path: 'register', component: Register },
  { path: 'onboarding', component: Onboarding, canActivate: [authGuard] },
  {
    path: 'app',
    component: Dashboard,
    canActivate: [authGuard]
  },
  {
    path: '',
    redirectTo: 'app',
    pathMatch: 'full'
  },
  { path: '**', redirectTo: 'welcome' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
