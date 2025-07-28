import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { HttpClient, HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-register',
  imports: [ReactiveFormsModule, RouterModule, HttpClientModule],
  templateUrl: './register.html',
  styleUrl: './register.css'
})
export class Register {
  registerForm: FormGroup;

  constructor(
    private fb: FormBuilder,
    private router: Router,
    private http: HttpClient
  ) {
    this.registerForm = this.fb.group({
      user_id: ['', [Validators.required]],
      name: ['', [Validators.required]],
      role: ['employee', [Validators.required]],
      password: ['', [Validators.required]],
    });
  }

  onSubmit(): void {
    if (this.registerForm.valid) {
      const userData = this.registerForm.value;
      console.log('Registering:', userData);

      this.http.post('http://127.0.0.1:8000/api/accounts/register/', userData)
        .subscribe({
          next: (res) => {
            console.log('Registration successful:', res);
            this.router.navigate(['/login']);
          },
          error: (err) => {
            console.error('Registration failed:', err);
          }
        });
    } else {
      console.log('Form is invalid');
    }
  }
}
