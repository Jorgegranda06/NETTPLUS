import { importProvidersFrom } from '@angular/core';
import { IonicModule } from '@ionic/angular';
import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter, withHashLocation } from '@angular/router';
import { routes } from './app/app.routes';
import { AppComponent } from './app/app.component';
import { authInterceptor } from './app/core/config/api.config';
bootstrapApplication(AppComponent,{providers:[provideRouter(routes,withHashLocation()),importProvidersFrom(IonicModule.forRoot()),provideHttpClient(withInterceptors([authInterceptor]))]}).catch(console.error);
