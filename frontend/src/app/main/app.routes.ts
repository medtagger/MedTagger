import { UploadPageComponent } from '../pages/upload-page/upload-page.component';
import { TutorialPageComponent } from '../pages/tutorial-page/tutorial-page.component';
import { HomePageComponent } from '../pages/home-page/home-page.component';
import { ValidationPageComponent } from '../pages/validation-page/validation-page.component';
import { SettingsPageComponent } from '../pages/settings-page/settings-page.component';
import { RouterModule, Routes } from '@angular/router';
import { MarkerPageComponent } from '../pages/marker-page/marker-page.component';
import { LoginPageComponent } from '../pages/login-page/login-page.component';
import { ModuleWithProviders } from '@angular/core';
import { AuthGuard } from '../guards/auth.guard';
import * as appRoutes from '../constants/routes';

export const labelingRoutes: Routes = [
    {
        path: appRoutes.LABELING,
        component: MarkerPageComponent,
        data: {title: 'Labelling'},
        canActivate: [AuthGuard]
    },
    {
        path: appRoutes.TUTORIAL,
        component: TutorialPageComponent,
        data: {title: 'Tutorial'},
        canActivate: [AuthGuard]
    },
];

export const routes: Routes = [
    {path: '', redirectTo: appRoutes.LOGIN, pathMatch: 'full'},
    {path: appRoutes.LOGIN, component: LoginPageComponent, data: {title: 'Welcome'}},
    {path: appRoutes.HOME, component: HomePageComponent, data: {title: 'Home'}, canActivate: [AuthGuard]},
    {path: appRoutes.UPLOAD, component: UploadPageComponent, data: {title: 'Upload new Scans'}, canActivate: [AuthGuard]},
    {path: appRoutes.SETTINGS, component: SettingsPageComponent, data: {title: 'Settings'}, canActivate: [AuthGuard]},
    {path: appRoutes.VALIDATION, component: ValidationPageComponent, data: {title: 'Validation'}, canActivate: [AuthGuard]},
    ...labelingRoutes
];

export const routing: ModuleWithProviders = RouterModule.forRoot(routes, {enableTracing: true} // config for debugging
);
