import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PeopleTableViewComponent } from './people-table-view.component';

describe('PeopleTableViewComponent', () => {
  let component: PeopleTableViewComponent;
  let fixture: ComponentFixture<PeopleTableViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PeopleTableViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PeopleTableViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
