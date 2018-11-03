import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {MarkerComponent} from './marker.component';
import {MatProgressSpinnerModule, MatSliderModule, MatSnackBarModule} from '@angular/material';

describe('MarkerComponent', () => {
    let component: MarkerComponent;
    let fixture: ComponentFixture<MarkerComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [MarkerComponent],
            imports: [
                MatSliderModule,
                MatProgressSpinnerModule,
                MatSnackBarModule
            ]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(MarkerComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    // it('should be created', () => {
    //     expect(component).toBeTruthy();
    // });
});
