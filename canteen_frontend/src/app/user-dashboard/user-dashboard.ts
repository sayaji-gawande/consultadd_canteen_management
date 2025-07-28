import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-user-dashboard',
  imports: [RouterModule, ReactiveFormsModule, CommonModule],
  templateUrl: './user-dashboard.html',
  styleUrl: './user-dashboard.css'
})

 

export class UserDashboard implements OnInit {
  userRole: string | null = null;

  constructor(private router: Router, private http : HttpClient) {}

  ngOnInit(): void {
    
    this.userRole = localStorage.getItem('userRole');
  }
  fetchItems() {
    console.log("Entry inside fetech");
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('Token not found in localStorage');
      return;
    }

    const headers = {
      'Authorization': `Bearer ${token}`
    };

    this.http.get<any>('http://127.0.0.1:8000/api/accounts/employees/', { headers }).subscribe({
      next: res => {
      this.router.navigate(['/userlist']);
      },
      error: err => {
        console.error('Error fetching menu items', err);
      }
    });
  }
  logout(): void {
    localStorage.clear();
    this.router.navigate(['/login']);
  }
}


