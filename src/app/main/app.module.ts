import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpModule} from '@angular/http';

import {SocketIoModule} from 'ng-socket-io';

import {AppComponent} from './app.component';
import {LoginPageComponent} from '../pages/login-page/login-page.component';
import {HomePageComponent} from '../pages/home-page/home-page.component';
import {MarkerPageComponent} from '../pages/marker-page/marker-page.component';
import {MarkerTutorialPageComponent} from '../pages/marker-tutorial-page/marker-tutorial-page.component';
import {UploadPageComponent} from '../pages/upload-page/upload-page.component';
import {CategoryPageComponent} from '../pages/category-page/category-page.component';

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
  MatToolbarModule,
  MatSidenavModule,
  MatListModule,
  MatGridListModule,
} from '@angular/material';


const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch: 'full'},
  {path: 'login', component: LoginPageComponent, data: {title: 'Logowanie'}},
  {path: 'home', component: HomePageComponent, data: {title: 'Strona Główna'}},
  {path: 'category', component: CategoryPageComponent, data: {title: 'Wybór kategorii'}},
  {path: 'marker', component: MarkerPageComponent, data: {title: 'Etykietowanie'}},
  {path: 'marker-tutorial', component: MarkerTutorialPageComponent, data: {title: 'Poradnik'}},
  {path: 'upload', component: UploadPageComponent, data: {title: 'Dodawanie skanów'}}
];

@NgModule({
  declarations: [
    AppComponent,
    LoginPageComponent,
    MarkerPageComponent,
    HomePageComponent,
    CategoryPageComponent,
    MarkerComponent,
    MarkerTutorialPageComponent,
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
    MatSidenavModule,
    MatListModule,
    MatGridListModule,
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
