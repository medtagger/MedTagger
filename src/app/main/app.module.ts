import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {LoginPageComponent} from '../pages/login-page/login-page.component';
import {MarkerPageComponent} from '../pages/marker-page/marker-page.component';

import {MaterialModule} from '@angular/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {RouterModule, Routes} from '@angular/router';

const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch: 'full'},
  {path: 'login', component: LoginPageComponent},
  {path: 'marker', component: MarkerPageComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    LoginPageComponent,
    MarkerPageComponent
  ],
  imports: [
    RouterModule.forRoot(
      routes,
      {enableTracing: true} // do debugowania
    ),
    BrowserModule,
    MaterialModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
