import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {LoginPageComponent} from './login-page.component';
import {MatButtonModule, MatFormFieldModule, MatIconModule, MatProgressSpinnerModule} from '@angular/material';

describe('LoginPageComponent', () => {
    let component: LoginPageComponent;
    let fixture: ComponentFixture<LoginPageComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [LoginPageComponent],
            imports: [
                MatFormFieldModule,
                MatButtonModule,
                MatIconModule,
                MatProgressSpinnerModule
            ]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(LoginPageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    // it('should be created', () => {
    //     expect(component).toBeTruthy();
    // });
});
