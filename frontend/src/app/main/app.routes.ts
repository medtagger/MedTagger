import {UploadPageComponent} from "../pages/upload-page/upload-page.component";
import {MarkerTutorialPageComponent} from "../pages/marker-tutorial-page/marker-tutorial-page.component";
import {HomePageComponent} from "../pages/home-page/home-page.component";
import {CategoryPageComponent} from "../pages/category-page/category-page.component";
import {ValidationPageComponent} from "../pages/validation-page/validation-page.component";
import {SettingsPageComponent} from "../pages/settings-page/settings-page.component";
import {RouterModule, Routes} from "@angular/router";
import {MarkerPageComponent} from "../pages/marker-page/marker-page.component";
import {LoginPageComponent} from "../pages/login-page/login-page.component";
import {ModuleWithProviders} from "@angular/core";

export const labellingRoutes: Routes = [
  {path: 'labelling', component: MarkerPageComponent, data: {title: 'Labelling'}},
  {path: 'labelling/choose-category', component: CategoryPageComponent, data: {title: 'Choosing category'}},
  {path: 'labelling/tutorial', component: MarkerTutorialPageComponent, data: {title: 'Marker tutorial'}}
];

export const routes: Routes = [
  {path: '', redirectTo: 'login', pathMatch: 'full'},
  {path: 'login', component: LoginPageComponent, data: {title: 'Welcome'}},
  {path: 'home', component: HomePageComponent, data: {title: 'Home'}},
  {path: 'upload', component: UploadPageComponent, data: {title: 'Upload new scans'}},
  {path: 'settings', component: SettingsPageComponent, data: {title: 'Settings'}},
  {path: 'validation', component: ValidationPageComponent, data: {title: 'Validation'}},
  ...labellingRoutes
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes, {enableTracing: true} // config for debugging
);
