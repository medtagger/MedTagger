import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {ValidationPageComponent} from './validation-page.component';
import {MatButtonModule} from '@angular/material';
import {ScanViewerComponent} from '../../components/scan-viewer/scan-viewer.component';

describe('ValidationPageComponent', () => {
    let component: ValidationPageComponent;
    let fixture: ComponentFixture<ValidationPageComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [ValidationPageComponent],
            imports: [
                MatButtonModule,
                ScanViewerComponent
            ]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(ValidationPageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    // it('should be created', () => {
    //     expect(component).toBeTruthy();
    // });
});
