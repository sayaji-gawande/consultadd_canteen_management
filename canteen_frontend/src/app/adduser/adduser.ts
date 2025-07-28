import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-adduser',
  standalone: true,
  imports: [CommonModule, RouterModule, ReactiveFormsModule],
  templateUrl: './adduser.html',
  styleUrl: './adduser.css'
})
export class Adduser {
  userform: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private http: HttpClient
  ) {
    this.userform = this.fb.group({
      user_id: ['', Validators.required],
      name: ['', Validators.required],
      role: ['', Validators.required],
      password: ['', Validators.required]
    });
  }

  onSubmit(): void {
    if (this.userform.valid) {
      const token = localStorage.getItem('accessToken');

      const headers = new HttpHeaders({
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      });

      const payload = this.userform.value;

      this.http.post('http://127.0.0.1:8000/api/accounts/add-employee/', payload, { headers })
        .subscribe({
          next: (res) => {
            console.log('User added successfully:', res);
            this.router.navigate(['/userlist']);
          },
          error: (err) => {
            console.error('Error while adding user:', err);
          }
        });
    } else {
      console.warn('Form is invalid');
    }
  }
}
