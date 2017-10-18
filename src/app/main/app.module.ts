import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule} from '@angular/forms';
import {HttpModule} from '@angular/http';

import {SocketIoModule} from 'ng-socket-io';

import {AppComponent} from './app.component';
import {LoginPageComponent} from '../pages/login-page/login-page.component';
import {MarkerPageComponent} from '../pages/marker-page/marker-page.component';
import {UploadPageComponent} from '../pages/upload-page/upload-page.component';

import {MockService} from '../services/mock.service';

import {MarkerComponent} from '../components/marker/marker.component';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {RouterModule, Routes} from '@angular/router';

import {MatCardModule, MatSliderModule, MatButtonModule, MatIconModule} from '@angular/material';


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
    MarkerComponent,
    UploadPageComponent,
  ],
  imports: [
    RouterModule.forRoot(
      routes,
      {enableTracing: true} // do debugowania
    ),
    MatCardModule,
    MatSliderModule,
    MatButtonModule,
    MatIconModule,
    BrowserModule,
    BrowserAnimationsModule,
    BrowserAnimationsModule,
    FormsModule,
    SocketIoModule,
    HttpModule,
  ],
  providers: [MockService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
