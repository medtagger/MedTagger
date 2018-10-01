import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {MarkerPageComponent} from './marker-page.component';
import {MatFormFieldModule, MatIconModule, MatOptionModule, MatSelectModule} from '@angular/material';
import {MarkerComponent} from '../../components/marker/marker.component';

describe('MarkerPageComponent', () => {
    let component: MarkerPageComponent;
    let fixture: ComponentFixture<MarkerPageComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [MarkerPageComponent],
            imports: [
                MatFormFieldModule,
                MatSelectModule,
                MatOptionModule,
                MatIconModule,
                MarkerComponent
            ]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(MarkerPageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    // it('should be created', () => {
    //     expect(component).toBeTruthy();
    // });
});
