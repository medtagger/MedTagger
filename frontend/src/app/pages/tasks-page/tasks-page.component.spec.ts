import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {TasksPageComponent} from './tasks-page.component';
import {MatButtonModule, MatIconModule, MatProgressSpinnerModule} from '@angular/material';
import {RouterTestingModule} from '@angular/router/testing';

describe('TasksPageComponent', () => {
    let component: TasksPageComponent;
    let fixture: ComponentFixture<TasksPageComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [TasksPageComponent],
            imports: [
                MatProgressSpinnerModule,
                MatIconModule,
                MatButtonModule,
                RouterTestingModule
            ]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(TasksPageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    // it('should be created', () => {
    //     expect(component).toBeTruthy();
    // });
});
