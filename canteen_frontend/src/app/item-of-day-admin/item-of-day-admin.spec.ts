import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ItemOfDayAdmin } from './item-of-day-admin';

describe('ItemOfDayAdmin', () => {
  let component: ItemOfDayAdmin;
  let fixture: ComponentFixture<ItemOfDayAdmin>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ItemOfDayAdmin]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ItemOfDayAdmin);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
