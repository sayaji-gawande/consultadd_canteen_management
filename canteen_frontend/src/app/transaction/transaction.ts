import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { RouterModule, Router } from '@angular/router';


@Component({
  selector: 'app-transaction',
  imports: [RouterModule, CommonModule],
  templateUrl: './transaction.html',
  styleUrl: './transaction.css'
})
export class Transaction implements OnInit{

  transactions: any[] = [];
  apiUrl: string = '';
  headers: HttpHeaders;

  constructor(private http: HttpClient, private router: Router) {
    const token = localStorage.getItem('accessToken');
    const role = localStorage.getItem('role');
    
      this.apiUrl = 'http://127.0.0.1:8000/api/transactions/all-transactions/';

    this.headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`,
    });
  }

  ngOnInit(): void {
    this.fetchTransactions();
  }

  fetchTransactions(): void {
    this.http.get<any[]>(this.apiUrl, { headers: this.headers }).subscribe({
      next: (res) => {
        this.transactions = res;
      },
      error: (err) => {
        console.error('Error fetching transactions:', err);
      }
    });
  }
  
}