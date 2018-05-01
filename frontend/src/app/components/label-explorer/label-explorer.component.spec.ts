import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelExplorerComponent } from './label-explorer.component';

describe('LabelExplorerComponent', () => {
  let component: LabelExplorerComponent;
  let fixture: ComponentFixture<LabelExplorerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LabelExplorerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LabelExplorerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
