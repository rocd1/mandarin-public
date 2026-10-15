import { Routes } from '@angular/router';

import { Landing } from './pages/landing/landing';
import { Study } from './pages/study/study';
import { QuizSetup } from './pages/quiz-setup/quiz-setup';
import { QuizPlay } from './pages/quiz-play/quiz-play';
import { QuizResults } from './pages/quiz-results/quiz-results';

export const routes: Routes = [
  {
    path: '',
    component: Landing,
  },
  {
    path: 'study/:level',
    component: Study,
  },
  {
    path: 'quiz/:level/play',
    component: QuizPlay,
  },
  {
    path: 'quiz/:level/results',
    component: QuizResults,
  },
  {
    path: 'quiz/:level',
    component: QuizSetup,
  },
  {
    path: '**',
    redirectTo: '',
  },
];