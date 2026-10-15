
import { Component, inject, signal } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { QuizType } from '../../core/models/quiz.models';

@Component({
  selector: 'app-quiz-setup',
  standalone: true,
  templateUrl: './quiz-setup.html',
  styleUrl: './quiz-setup.css',
})
export class QuizSetup {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  readonly hskLevel = signal<number | null>(null);

  constructor() {
    const level = Number(this.route.snapshot.paramMap.get('level'));

    if (Number.isInteger(level) && level >= 1 && level <= 7) {
      this.hskLevel.set(level);
    } else {
      void this.router.navigate(['/']);
    }
  }

  selectQuizType(quizType: QuizType): void {
    const level = this.hskLevel();

    if (level === null) {
      return;
    }

    void this.router.navigate(['/quiz', level, 'play'], {
      queryParams: { quiz_type: quizType },
    });
  }
}
