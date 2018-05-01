import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpModule} from '@angular/http';
import {HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';
import {SocketIoModule, SocketIoConfig} from 'ng-socket-io';

import {AppComponent} from './app.component';
import {LoginPageComponent} from '../pages/login-page/login-page.component';
import {HomePageComponent} from '../pages/home-page/home-page.component';
import {MarkerPageComponent} from '../pages/marker-page/marker-page.component';
import {MarkerTutorialPageComponent} from '../pages/marker-tutorial-page/marker-tutorial-page.component';
import {UploadPageComponent} from '../pages/upload-page/upload-page.component';
import {CategoryPageComponent} from '../pages/category-page/category-page.component';
import {SettingsPageComponent} from '../pages/settings-page/settings-page.component';
import {ValidationPageComponent} from '../pages/validation-page/validation-page.component';

import {HttpAuthenticationInterceptor} from "../services/http-authentication.interceptor";

import {MarkerComponent} from '../components/marker/marker.component';
import {UploadScansSelectorComponent} from '../components/upload-scans-selector/upload-scans-selector.component';

import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

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
    MatExpansionModule,
    MatSnackBarModule,
    MatSelectModule,
    MatTooltipModule,
    MatDialog,
    MatDialogModule,
    MatChipsModule,
} from '@angular/material';
import {ScanViewerComponent} from '../components/scan-viewer/scan-viewer.component';
import {routing} from "./app.routes";
import {AuthGuard} from "../guards/auth.guard";
import {AccountService} from "../services/account.service";
import {DialogService} from "../services/dialog.service";
import {InfoDialog} from "../dialogs/info.dialog";
import {environment} from '../../environments/environment';

const config: SocketIoConfig = {url: environment.WEBSOCKET_URL + '/slices', options: {path: environment.WEBSOCKET_PATH}};

@NgModule({
    declarations: [
        AppComponent,
        LoginPageComponent,
        MarkerPageComponent,
        HomePageComponent,
        CategoryPageComponent,
        MarkerComponent,
        ScanViewerComponent,
        MarkerTutorialPageComponent,
        UploadScansSelectorComponent,
        UploadPageComponent,
        SettingsPageComponent,
        ValidationPageComponent,
        InfoDialog
    ],
    imports: [
        routing,
        BrowserModule,
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
        MatTooltipModule,
        MatDialogModule,
        BrowserAnimationsModule,
        FormsModule,
        ReactiveFormsModule,
        SocketIoModule.forRoot(config),
        ReactiveFormsModule,
        MatExpansionModule,
        MatSnackBarModule,
        MatSelectModule,
        HttpModule,
        HttpClientModule,
        MatChipsModule
    ],
    entryComponents: [
        InfoDialog
    ],
    providers: [
        {
            provide: HTTP_INTERCEPTORS,
            useClass: HttpAuthenticationInterceptor,
            multi: true
        },
        AuthGuard,
        AccountService,
        DialogService,
        MatDialog
    ],
    bootstrap: [AppComponent]
})
export class AppModule {}
