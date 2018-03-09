import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {ScanViewerComponent} from './scan-viewer.component';

describe('ScanViewerComponent', () => {
    let component: ScanViewerComponent;
    let fixture: ComponentFixture<ScanViewerComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [ScanViewerComponent]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(ScanViewerComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
