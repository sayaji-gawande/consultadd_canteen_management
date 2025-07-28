import { Routes } from '@angular/router';
import { Login } from './login/login';
import { Register } from './register/register';
import { App } from './app';

import { UserDashboard } from './user-dashboard/user-dashboard';
import { ItemOftheDay } from './item-ofthe-day/item-ofthe-day';
import { Transaction } from './transaction/transaction';
import { Userlist } from './userlist/userlist';
import { Adduser } from './adduser/adduser';
import { Additem } from './additem/additem';
import { authGuard } from './auth-guard';
import { UserTransactions } from './user-transactions/user-transactions';
import { ItemOfDayAdmin } from './item-of-day-admin/item-of-day-admin';
import { Menu } from './menu/menu';




export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'register', component: Register },

  { path: 'dashboard', component: UserDashboard, canActivate: [authGuard] },
  { path: 'itemoftheday', component: ItemOftheDay, canActivate: [authGuard] },
  { path: 'itemofdayadmin', component: ItemOfDayAdmin, canActivate: [authGuard] },
  { path: 'transaction', component: Transaction, canActivate: [authGuard] },
  { path: 'menu', component: Menu, canActivate: [authGuard] },
  { path: 'adduser', component: Adduser, canActivate: [authGuard] },
  { path: 'additem', component: Additem, canActivate: [authGuard] },
  { path: 'userlist', component: Userlist, canActivate: [authGuard] },
  { path: 'usertransactions', component: UserTransactions, canActivate: [authGuard] },
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: '**', redirectTo: 'dashboard' }

];
