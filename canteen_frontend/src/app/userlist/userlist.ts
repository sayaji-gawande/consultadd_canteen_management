import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { RouterModule, Router } from '@angular/router';
@Component({
  selector: 'app-userlist',
  imports: [CommonModule, RouterModule],
  templateUrl: './userlist.html',
  styleUrl: './userlist.css'
})
export class Userlist {

  userItems: any[] = [];
  userRole: string = '';
  filteredUsers: any[] = [];

  constructor(private http: HttpClient, private router: Router) { }

  ngOnInit(): void {
    this.fetchItems();
    const role = localStorage.getItem('userRole');
    this.userRole = role ? role : '';
  }
  getToken(): string {
    return localStorage.getItem('accessToken') || '';
  }
  fetchItems() {
  const token = localStorage.getItem('accessToken');

  if (!token) {
    console.error('Token not found in localStorage');
    return;
  }

  const headers = {
    'Authorization': `Bearer ${token}`
  };

  this.http.get<any>('http://127.0.0.1:8000/api/accounts/employees/', { headers }).subscribe({
    next: res => {
      console.log("Entry");
      console.log(res);
      this.userItems = res;
      console.log(this.userItems);
    },
    error: err => {
      console.error('Error fetching menu items', err);
    }
  });
}

  onAddItem() {
    this.router.navigate(['/adduser']);
  }

  filterUsers() {
    this.http.get<any>('http://127.0.0.1:8000/api/accounts/').subscribe({
      next: res => {
        this.filteredUsers = res.data;
        console.log(this.filteredUsers);
      },
      error: err => {
        console.error('Error fetching menu items', err);
      }
    });

  }

   onDeleteUser(username: string) {
    if (!confirm(`Are you sure you want to delete user "${username}"?`)) return;

    const token = this.getToken();
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });

    this.http.delete(`http://127.0.0.1:8000/api/accounts/employees/${username}/`, { headers })
      .subscribe({
        next: () => {
          alert('User deleted successfully.');
          this.fetchItems();
        },
        error: err => {
          console.error('Error deleting user', err);
          alert('Failed to delete user.');
        }
      });
  }

}
