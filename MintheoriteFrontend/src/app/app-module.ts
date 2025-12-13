import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing-module';

import { App } from './app';
import { Welcome } from './components/welcome/welcome';
import { Dashboard } from './components/dashboard/dashboard';
import { Login } from './components/login/login';
import { Register } from './components/register/register';
import { Navbar } from './components/navbar/navbar';
import { Onboarding } from './components/onboarding/onboarding';
import { RoleSelector } from './components/role-selector/role-selector';
import { FooterComponent } from './components/footer/footer';

import { authInterceptor } from './interceptors/auth.interceptor';

@NgModule({
  declarations: [
    App,
    Welcome,
    Dashboard,
    Login,
    Register,
    Navbar,
    Onboarding,
    RoleSelector,
    FooterComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule
  ],
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideHttpClient(withInterceptors([authInterceptor]))
  ],
  bootstrap: [App]
})
export class AppModule { }
