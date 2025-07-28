import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-item-of-day-admin',
  standalone: true,
  imports: [RouterModule, CommonModule, ReactiveFormsModule],
  templateUrl: './item-of-day-admin.html',
  styleUrls: ['./item-of-day-admin.css']
})
export class ItemOfDayAdmin implements OnInit {
  itemForm!: FormGroup;
  items: any[] = [];

  private apiUrl = 'http://127.0.0.1:8000/api/items/todays-items/';
  private headers = new HttpHeaders({
    Authorization: `Bearer ${localStorage.getItem('accessToken') || ''}`,
    'Content-Type': 'application/json'
  });

  constructor(private http: HttpClient, private fb: FormBuilder) { }

  ngOnInit(): void {
    this.itemForm = this.fb.group({
      item_name: ['', Validators.required],
      quantity: [1, [Validators.required, Validators.min(1)]]
    });
    this.loadItems();
  }

  loadItems(): void {
    this.http.get<any[]>(this.apiUrl, { headers: this.headers })
      .subscribe({
        next: res => (this.items = res),
        error: err => console.error('Error fetching items:', err)
      });
  }

  addItem(): void {
    if (this.itemForm.invalid) return;
    this.http.post(this.apiUrl, this.itemForm.value, { headers: this.headers })
      .subscribe({
        next: () => { this.itemForm.reset(); this.loadItems(); },
        error: err => console.error('Error adding item:', err)
      });
  }
  deleteItem(itemName: string): void {
    const url = `${this.apiUrl}${itemName}/`;
    this.http.delete(url, { headers: this.headers })
      .subscribe({
        next: () => {
          console.log(`Deleted: ${itemName}`);
          this.loadItems();
        },
        error: err => {
          console.error(`Error deleting ${itemName}:`, err);
          alert(err?.error?.detail || 'Could not delete item.');
        }
      });


  }

  updateItem(item: any): void {
    const url = `${this.apiUrl}${item.original_name || item.item_name}/`;  
    const payload = {
      item_name: item.item_name,
      quantity: item.quantity || 1
    };

    this.http.put(url, payload, { headers: this.headers }).subscribe({
      next: () => {
        console.log(`Updated: ${item.item_name}`);
        this.loadItems();  
      },
      error: err => {
        console.error('Error updating item:', err);
        alert(err?.error?.detail || 'Could not update item.');
      }
    });

  }

}
