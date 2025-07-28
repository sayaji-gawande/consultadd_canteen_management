import { inject } from '@angular/core';
import { CanActivateFn } from '@angular/router';
import { Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const token = localStorage.getItem('accessToken');
  const router = inject(Router);

  if (token) {
    return true;
  } else {
    router.navigate(['/login']);
    return false;
  }
};
