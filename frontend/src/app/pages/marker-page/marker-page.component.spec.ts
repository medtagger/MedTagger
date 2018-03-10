import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {MarkerPageComponent} from './marker-page.component';

describe('MarkerPageComponent', () => {
    let component: MarkerPageComponent;
    let fixture: ComponentFixture<MarkerPageComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [MarkerPageComponent]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(MarkerPageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should be created', () => {
        expect(component).toBeTruthy();
    });
});
