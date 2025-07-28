import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule, RouterModule],
  standalone: true,
  templateUrl: './login.html',
  styleUrl: './login.css'
})

export class Login {
  loginForm: FormGroup;

  constructor(private fb: FormBuilder, private router: Router, private http: HttpClient) {

    this.loginForm = this.fb.group({
      user_id : ['', [Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  isLoading = false;

  onSubmit(): void {
   
    if (this.loginForm.valid) {
      this.isLoading = true;
    
      const formData = this.loginForm.value;
      this.http.post<any>('http://127.0.0.1:8000/api/accounts/login/', formData)
        .subscribe({
          next: (response) => {
            localStorage.setItem('accessToken', response.access);
            localStorage.setItem('refreshToken', response.refresh);
            localStorage.setItem('userRole', response.role);
            localStorage.setItem('userName', response.name);
            this.router.navigate(['/dashboard']);
          },
          error: (error) => {
            alert('Login failed. Please check your credentials.');
            console.error('Login failed:', error);
          },
          complete: () => {
            this.isLoading = false;
          }
        });
    }
  }

}