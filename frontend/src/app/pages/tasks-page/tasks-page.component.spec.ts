import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {TasksPageComponent} from './tasks-page.component';

describe('TasksPageComponent', () => {
    let component: TasksPageComponent;
    let fixture: ComponentFixture<TasksPageComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [TasksPageComponent]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(TasksPageComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should be created', () => {
        expect(component).toBeTruthy();
    });
});
