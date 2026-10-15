import { Component, computed, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';

import {
  QuizBatchSubmission,
  QuizType,
} from '../../core/models/quiz.models';
import { LearningApiService } from '../../core/services/learning-api.service';
import { QuizStateService } from '../../core/services/quiz-state.service';

@Component({
  selector: 'app-quiz-play',
  imports: [RouterLink],
  standalone: true,
  templateUrl: './quiz-play.html',
  styleUrl: './quiz-play.css',
})
export class QuizPlay implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly learningApi = inject(LearningApiService);
  readonly quizState = inject(QuizStateService);

  readonly currentIndex = signal(0);
  readonly loading = signal(true);
  readonly submitting = signal(false);
  readonly error = signal('');

  readonly questions = this.quizState.questions;

  readonly currentQuestion = computed(
    () => this.questions()[this.currentIndex()] ?? null,
  );

  readonly answeredCount = computed(
    () => Object.keys(this.quizState.answers()).length,
  );

  readonly questionCount = computed(() => this.questions().length);

  level = 1;
  private quizType: QuizType = 'hanzi_to_meaning';

  ngOnInit(): void {
    const level = Number(this.route.snapshot.paramMap.get('level'));
    const quizType = this.route.snapshot.queryParamMap.get('quiz_type');

    const validQuizTypes: QuizType[] = [
      'hanzi_to_meaning',
      'meaning_to_hanzi',
      'hanzi_to_pinyin',
      'pinyin_to_hanzi',
    ];

    if (
      !Number.isInteger(level) ||
      level < 1 ||
      level > 7 ||
      !validQuizTypes.includes(quizType as QuizType)
    ) {
      void this.router.navigate(['/']);
      return;
    }

    this.level = level;
    this.quizType = quizType as QuizType;
    this.loadQuestions();
  }

  loadQuestions(): void {
    this.loading.set(true);
    this.error.set('');
    this.currentIndex.set(0);

    this.learningApi.getQuizQuestions(this.level, this.quizType).subscribe({
      next: (response) => {
        if (!response.questions?.length) {
          this.error.set('No questions are available for this quiz.');
          this.loading.set(false);
          return;
        }

        this.quizState.setQuiz(this.level, this.quizType, response.questions);
        this.loading.set(false);
      },
      error: (err: unknown) => {
        console.error('Unable to load quiz questions.', err);
        this.error.set(
          'Unable to load quiz questions. Please check your connection and try again.',
        );
        this.loading.set(false);
      },
    });
  }

  selectAnswer(answer: string): void {
    const question = this.currentQuestion();

    if (!question || this.submitting()) {
      return;
    }

    this.quizState.setAnswer(question.id, answer);
  }

  isSelected(answer: string): boolean {
    const question = this.currentQuestion();

    return question
      ? this.quizState.getAnswer(question.id) === answer
      : false;
  }

  previousQuestion(): void {
    if (this.currentIndex() > 0) {
      this.currentIndex.update((index) => index - 1);
    }
  }

  nextQuestion(): void {
    if (this.currentIndex() < this.questionCount() - 1) {
      this.currentIndex.update((index) => index + 1);
    }
  }

  submitQuiz(): void {
    if (this.submitting() || this.questionCount() === 0) {
      return;
    }

    const questions = this.questions();
    const answers = this.quizState.answers();

    const unanswered = questions.filter(
      (question) => !answers[question.id],
    );

    if (unanswered.length > 0) {
      this.error.set(
        `Please answer all questions before submitting. ${unanswered.length} question(s) remain.`,
      );
      return;
    }

    this.error.set('');
    this.submitting.set(true);

    const submission: QuizBatchSubmission = {
      answers: questions.map((question) => ({
        question_id: question.id,
        answer: answers[question.id],
      })),
    };

    this.learningApi.submitQuiz(submission).subscribe({
      next: (result) => {
        this.quizState.setResult(result);
        void this.router.navigate([
          '/quiz',
          this.level,
          'results',
        ]);
      },
      error: (err: unknown) => {
        console.error('Unable to submit quiz.', err);
        this.error.set(
          'Unable to submit your answers. Please try again.',
        );
        this.submitting.set(false);
      },
    });
  }

  exitQuiz(): void {
    void this.router.navigate(['/study', this.level]);
  }
}