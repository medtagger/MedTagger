import { TestBed, async } from '@angular/core/testing';

import { AppComponent } from './app.component';
import {
    MatButtonModule,
    MatIconModule,
    MatListModule,
    MatSidenavModule,
    MatSnackBarModule,
    MatToolbarModule
} from '@angular/material';
import { RouterTestingModule } from '@angular/router/testing';
import { TranslateService } from '@ngx-translate/core';
import { TranslateServiceStub } from '../mocks/TranslateServiceStub';

describe('AppComponent', () => {

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [
                AppComponent
            ],
            imports: [
                MatButtonModule,
                MatIconModule,
                MatListModule,
                RouterTestingModule,
                MatSidenavModule,
                MatToolbarModule,
                MatSnackBarModule
            ],
            providers: [
                {
                    provide: TranslateService,
                    useClass: TranslateServiceStub
                }
            ]
        }).compileComponents();
    }));

    it('should create the main', async(() => {
        const fixture = TestBed.createComponent(AppComponent);
        const app = fixture.debugElement.componentInstance;
        expect(app).toBeTruthy();
    }));
});
