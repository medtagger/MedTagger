import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpModule} from '@angular/http';

import {SocketIoModule} from 'ng-socket-io';

import {AppComponent} from './app.component';
import {LoginPageComponent} from '../pages/login-page/login-page.component';
import {MarkerPageComponent} from '../pages/marker-page/marker-page.component';
import {UploadPageComponent} from '../pages/upload-page/upload-page.component';

import {MockService} from '../services/mock.service';

import {MarkerComponent} from '../components/marker/marker.component';
import {UploadScansSelectorComponent} from '../components/upload-scans-selector/upload-scans-selector.component';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {RouterModule, Routes} from '@angular/router';

import {
  MatCardModule,
  MatProgressBarModule,
  MatProgressSpinnerModule,
  MatStepperModule,
  MatRadioModule,
  MatSliderModule,
  MatButtonModule,
  MatIconModule,
  MatFormFieldModule,
  MatInputModule,
  MatToolbarModule
} from '@angular/material';

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
    UploadScansSelectorComponent,
    UploadPageComponent,
  ],
  imports: [
    RouterModule.forRoot(
      routes,
      {enableTracing: true} // do debugowania
    ),
    MatToolbarModule,
    MatCardModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatStepperModule,
    MatRadioModule,
    MatFormFieldModule,
    MatInputModule,
    MatSliderModule,
    MatButtonModule,
    MatIconModule,
    BrowserModule,
    BrowserAnimationsModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    SocketIoModule,
    ReactiveFormsModule,
    HttpModule,
  ],
  providers: [MockService],
  bootstrap: [AppComponent]
})
export class AppModule {
}
