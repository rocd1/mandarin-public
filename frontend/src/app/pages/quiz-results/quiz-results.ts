import { Component, computed, inject, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

import { DecimalPipe } from '@angular/common';

import { QuizType } from '../../core/models/quiz.models';
import { QuizStateService } from '../../core/services/quiz-state.service';




@Component({
  selector: 'app-quiz-results',
  imports: [DecimalPipe],
  standalone: true,
  templateUrl: './quiz-results.html',
  styleUrl: './quiz-results.css',
})
export class QuizResults implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);

  readonly quizState = inject(QuizStateService);

  readonly result = this.quizState.result;
  readonly quizType = this.quizState.quizType;

  level = 1;

  readonly incorrectCount = computed(() => {
    const result = this.result();

    return result
      ? result.total_questions - result.correct_count
      : 0;
  });

  readonly reviewItems = computed(() => {
    const questions = this.quizState.questions();
    const answers = this.quizState.answers();
    const result = this.result();

    return questions.map((question) => {
      const answerResult = result?.results.find(
        (item) => item.question_id === question.id,
      );

      return {
        question,
        userAnswer: answers[question.id] ?? 'No answer',
        correctAnswer: answerResult?.correct_answer ?? '',
        correct: answerResult?.correct ?? false,
      };
    });
  });

  ngOnInit(): void {
    const level = Number(this.route.snapshot.paramMap.get('level'));

    if (!Number.isInteger(level) || level < 1 || level > 7) {
      void this.router.navigate(['/']);
      return;
    }

    this.level = level;

    // Results depend on quiz data held in memory.
    // If the page is refreshed or opened directly, return to quiz setup.
    if (!this.result() || this.quizState.questions().length === 0) {
      void this.router.navigate(['/quiz', this.level]);
    }
  }

  formatQuizType(type: QuizType | null): string {
    const labels: Record<QuizType, string> = {
      hanzi_to_meaning: 'Hanzi to Meaning',
      meaning_to_hanzi: 'Meaning to Hanzi',
      hanzi_to_pinyin: 'Hanzi to Pinyin',
      pinyin_to_hanzi: 'Pinyin to Hanzi',
    };

    return type ? labels[type] : 'Vocabulary Quiz';
  }

  tryAgain(): void {
    // Return to quiz setup so the learner can choose a quiz type.
    void this.router.navigate(['/quiz', this.level]);
  }

  generateMoreQuestions(): void {
    const type = this.quizType();

    if (!type) {
      this.tryAgain();
      return;
    }

    // Leaving the results route creates a new quiz-play page,
    // which requests another batch from the backend.
    void this.router.navigate(['/quiz', this.level, 'play'], {
      queryParams: { quiz_type: type },
    });
  }

  backToStudy(): void {
    void this.router.navigate(['/study', this.level]);
  }
}
