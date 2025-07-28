import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-menu',
  standalone: true,
  templateUrl: './menu.html',
  styleUrls: ['./menu.css'],
  imports: [CommonModule, ReactiveFormsModule],
})
export class Menu {
  items: any[] = [];
  headers: HttpHeaders;
  apiUrl = 'http://127.0.0.1:8000/api/items/items/';
  itemForm: FormGroup;
  editingIndex: number | null = null;

  constructor(private http: HttpClient, private fb: FormBuilder) {
    this.headers = new HttpHeaders({
      'Authorization': `Bearer ${localStorage.getItem('accessToken') || ''}`,
    });

    this.itemForm = this.fb.group({
      name: ['', Validators.required],
      price: ['', [Validators.required, Validators.min(1)]],
    });

    this.loadItems();
  }

  loadItems() {
    this.http.get<any[]>(this.apiUrl, { headers: this.headers })
      .subscribe({
        next: data => this.items = data,
        error: err => console.error('Failed to load items:', err)
      });
  }

  submitItem() {
    const payload = this.itemForm.value;
    if (this.editingIndex === null) {
      this.http.post(this.apiUrl, payload, { headers: this.headers }).subscribe({
        next: () => {
          this.itemForm.reset();
          this.loadItems();
        },
        error: err => alert('Error adding item')
      });
    } else {
      const oldName = this.items[this.editingIndex].name;
      this.http.put(`${this.apiUrl}${oldName}/`, payload, { headers: this.headers }).subscribe({
        next: () => {
          this.itemForm.reset();
          this.editingIndex = null;
          this.loadItems();
        },
        error: err => alert('Error updating item')
      });
    }
  }

  editItem(index: number) {
    const item = this.items[index];
    this.itemForm.setValue({ name: item.name, price: item.price });
    this.editingIndex = index;
  }

  cancelEdit() {
    this.itemForm.reset();
    this.editingIndex = null;
  }

  deleteItem(name: string) {
    this.http.delete(`${this.apiUrl}${name}/`, { headers: this.headers }).subscribe({
      next: () => this.loadItems(),
      error: err => alert('Error deleting item'),
    });
  }
}
