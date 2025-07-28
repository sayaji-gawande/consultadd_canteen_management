import { Component, OnInit } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { FormGroup, ReactiveFormsModule } from '@angular/forms';

@Component({
  selector: 'app-item-ofthe-day',
  standalone: true,
  imports: [CommonModule, RouterModule, ReactiveFormsModule],
  templateUrl: './item-ofthe-day.html',
  styleUrl: './item-ofthe-day.css'
})
export class ItemOftheDay implements OnInit {
  menuItems: any[] = [];
  userRole: string = '';

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
    this.fetchItems();
    const role = localStorage.getItem('userRole');
  }

  fetchItems() {
    const token = localStorage.getItem('accessToken');
    console.log("Entry");
    const headers = { 'Authorization': `Bearer ${token}` };
    this.http.get<any>('http://127.0.0.1:8000/api/items/todays-items-employee/', { headers }).subscribe({
      next: res => {
        this.menuItems = res || [];
      },
      error: err => {
        console.error('Error fetching menu items', err);
      }
    });
  }


  onPurchase(item: any) {
  const token = localStorage.getItem('accessToken');
  const headers = { 'Authorization': `Bearer ${token}` };

  const body = {
    item_name: item.name,
    quantity: 1 
  };

  this.http.post('http://127.0.0.1:8000/api/transactions/purchase/', body, { headers }).subscribe({
    next: (res: any) => {
      alert(res.message + ` Remaining Balance: ₹${res.remaining_balance}`);
    },
    error: err => {
      const errorMsg = err.error?.error || 'Failed to complete purchase.';
      alert(errorMsg);
      console.error('Purchase failed:', err);
    }
  });
}

}
