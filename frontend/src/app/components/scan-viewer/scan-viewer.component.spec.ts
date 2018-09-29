import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {ScanViewerComponent} from './scan-viewer.component';
import {MatSliderModule} from '@angular/material';

describe('ScanViewerComponent', () => {
    let component: ScanViewerComponent;
    let fixture: ComponentFixture<ScanViewerComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [ScanViewerComponent],
            imports: [
                MatSliderModule
            ]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(ScanViewerComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    // it('should create', () => {
    //     expect(component).toBeTruthy();
    // });
});
