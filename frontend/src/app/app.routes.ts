import { Routes } from '@angular/router';

import { Landing } from './pages/landing/landing';
import { Study } from './pages/study/study';

export const routes: Routes = [
  { path: '', component: Landing,},
  { path: 'study/:level', component: Study },
  { path: '**', redirectTo: '',},
];


