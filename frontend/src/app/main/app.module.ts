import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HttpClientModule, HTTP_INTERCEPTORS} from '@angular/common/http';
import {SocketIoModule} from 'ng-socket-io';

import {AppComponent} from './app.component';
import {LoginPageComponent} from '../pages/login-page/login-page.component';
import {HomePageComponent} from '../pages/home-page/home-page.component';
import {MarkerPageComponent} from '../pages/marker-page/marker-page.component';
import {MarkerTutorialPageComponent} from '../pages/marker-tutorial-page/marker-tutorial-page.component';
import {UploadPageComponent} from '../pages/upload-page/upload-page.component';
import {CategoryPageComponent} from '../pages/category-page/category-page.component';
import {SettingsPageComponent} from '../pages/settings-page/settings-page.component';
import {ValidationPageComponent} from '../pages/validation-page/validation-page.component';

import {HttpAuthenticationInterceptor} from '../services/http-authentication.interceptor';

import {MarkerComponent} from '../components/marker/marker.component';
import {UploadScansSelectorComponent} from '../components/upload-scans-selector/upload-scans-selector.component';

import {DomSanitizer} from '@angular/platform-browser';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';

import {
    MatCardModule,
    MatProgressBarModule,
    MatProgressSpinnerModule,
    MatStepperModule,
    MatRadioModule,
    MatSliderModule,
    MatButtonModule,
    MatButtonToggleModule,
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
    MatCheckboxModule,
    MatIconRegistry,
} from '@angular/material';
import {ScanViewerComponent} from '../components/scan-viewer/scan-viewer.component';
import {routing} from './app.routes';
import {AuthGuard} from '../guards/auth.guard';
import {AccountService} from '../services/account.service';
import {DialogService} from '../services/dialog.service';
import {InfoDialogComponent} from '../dialogs/info-dialog.component';
import {MedTaggerWebSocket} from '../services/websocket.service';

import {LabelExplorerComponent} from '../components/label-explorer/label-explorer.component';
import {NavbarComponent} from '../components/navbar/navbar.component';

@NgModule({
    declarations: [
        AppComponent,
        LoginPageComponent,
        MarkerPageComponent,
        HomePageComponent,
        CategoryPageComponent,
        MarkerComponent,
        LabelExplorerComponent,
        ScanViewerComponent,
        MarkerTutorialPageComponent,
        UploadScansSelectorComponent,
        UploadPageComponent,
        SettingsPageComponent,
        ValidationPageComponent,
        InfoDialogComponent,
        NavbarComponent
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
        MatButtonToggleModule,
        MatIconModule,
        MatSidenavModule,
        MatListModule,
        MatGridListModule,
        MatTooltipModule,
        MatDialogModule,
        BrowserAnimationsModule,
        FormsModule,
        ReactiveFormsModule,
        SocketIoModule,
        ReactiveFormsModule,
        MatExpansionModule,
        MatSnackBarModule,
        MatSelectModule,
        HttpClientModule,
        MatChipsModule,
        MatCheckboxModule,
    ],
    entryComponents: [
        InfoDialogComponent
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
        MatDialog,
        MedTaggerWebSocket,
    ],
    bootstrap: [AppComponent]
})
export class AppModule {
    constructor(matIconRegistry: MatIconRegistry, domSanitizer: DomSanitizer) {
    const MATERIAL_DESIGN_ICONS = 'assets/fonts/mdi.svg';
        matIconRegistry.addSvgIconSet(domSanitizer.bypassSecurityTrustResourceUrl(MATERIAL_DESIGN_ICONS));
    }
}
