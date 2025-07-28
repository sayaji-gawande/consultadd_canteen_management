import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ItemOftheDay } from './item-ofthe-day';

describe('ItemOftheDay', () => {
  let component: ItemOftheDay;
  let fixture: ComponentFixture<ItemOftheDay>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ItemOftheDay]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ItemOftheDay);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
