import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-additem',
  imports: [CommonModule],
  templateUrl: './additem.html',
  styleUrl: './additem.css'
})
export class Additem {

  userform: FormGroup;

  constructor(private fb: FormBuilder,  private router: Router, private http: HttpClient) {
    
    this.userform = this.fb.group({
    });
  }

  onSubmit(): void {
  if (this.userform.valid) {
    const formData = this.userform.value;

    this.http.post('http://localhost:8080/StudentLogin', formData)
      .subscribe({
        next: (response) => {
          console.log('Success:', response);
          // this.router.navigate(['/dashboard']);
        },
        error: (error) => {
          console.error('Error:', error);
        }
      });
  } else {
    console.log('Invalid login form');
  }
}

}
