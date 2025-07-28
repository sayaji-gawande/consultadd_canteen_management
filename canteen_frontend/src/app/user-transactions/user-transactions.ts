import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-user-transactions',
  standalone: true,
  templateUrl: './user-transactions.html',
  styleUrl: './user-transactions.css',
  imports: [CommonModule, ReactiveFormsModule]
})
export class UserTransactions {
  addMoneyForm: FormGroup;
  balance: number = 0.0;
  transactions: any[] = [];

  constructor(private http: HttpClient, private fb: FormBuilder) {
    this.addMoneyForm = this.fb.group({
      amount: ['', [Validators.required, Validators.min(1)]]
    });

    this.fetchBalance();
    this.fetchTransactions(); 
  }

  getToken(): string {
    return localStorage.getItem('accessToken') || '';
  }

  fetchBalance() {
    const token = this.getToken();
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    const username = localStorage.getItem('username');

    this.http.get<any>('http://127.0.0.1:8000/api/accounts/my-balance/', { headers })
      .subscribe({
        next: res => {
          console.log('Balance Response:', res);
          this.balance = parseFloat(res.balance);
        },
        error: err => {
          console.error('Error fetching balance:', err);
          alert('Could not fetch balance');
        }
      });
  }

  fetchTransactions() {
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${this.getToken()}` });

    this.http.get<any[]>('http://127.0.0.1:8000/api/transactions/passbook/', { headers })
      .subscribe({
        next: res => this.transactions = res,
        error: err => console.error('Error fetching transactions:', err)
      });
  }

  onAddMoney() {
    if (this.addMoneyForm.invalid) return;

    const headers = new HttpHeaders({ 'Authorization': `Bearer ${this.getToken()}` });
    const body = { amount: this.addMoneyForm.value.amount };

    this.http.post('http://127.0.0.1:8000/api/transactions/add-money/', body, { headers })
      .subscribe({
        next: () => {
          alert('Money added successfully!');
          this.addMoneyForm.reset();
          this.fetchBalance();
          this.fetchTransactions();
        },
        error: err => {
          console.error('Error adding money:', err);
          alert('Failed to add money.');
        }
      });
  }
}
