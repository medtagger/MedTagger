import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpModule} from '@angular/http';

import {SocketIoModule} from 'ng-socket-io';

import {AppComponent} from './app.component';
import {LoginPageComponent} from '../pages/login-page/login-page.component';
import {MarkerPageComponent} from '../pages/marker-page/marker-page.component';
import {UploadPageComponent} from '../pages/upload-page/upload-page.component';

import {MarkerComponent} from '../components/marker/marker.component';

import {MaterialModule} from '@angular/material';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {RouterModule, Routes} from '@angular/router';

const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch: 'full'},
  {path: 'login', component: LoginPageComponent},
  {path: 'marker', component: MarkerPageComponent},
  {path: 'upload', component: UploadPageComponent}
];

@NgModule({
  declarations: [
    AppComponent,
    LoginPageComponent,
    MarkerPageComponent,
    MarkerComponent
    MarkerPageComponent,
    UploadPageComponent,
  ],
  imports: [
    RouterModule.forRoot(
      routes,
      {enableTracing: true} // do debugowania
    ),
    BrowserModule,
    MaterialModule,
    BrowserAnimationsModule,
    FormsModule,
    SocketIoModule,
    HttpModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule {
}
