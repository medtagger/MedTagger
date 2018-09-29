import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {LabelExplorerComponent} from './label-explorer.component';
import {MatButtonModule, MatIconModule, MatListModule} from '@angular/material';

describe('LabelExplorerComponent', () => {
    let component: LabelExplorerComponent;
    let fixture: ComponentFixture<LabelExplorerComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [LabelExplorerComponent],
            imports: [
                MatIconModule,
                MatListModule,
                MatButtonModule
            ]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(LabelExplorerComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    // it('should create', () => {
    //     expect(component).toBeTruthy();
    // });
});
