import { Injectable, signal } from '@angular/core';

import {
  QuizBatchAnswerResponse,
  QuizQuestion,
  QuizType,
} from '../models/quiz.models';

@Injectable({
  providedIn: 'root',
})
export class QuizStateService {
  readonly hskLevel = signal<number | null>(null);
  readonly quizType = signal<QuizType | null>(null);

  readonly questions = signal<QuizQuestion[]>([]);
  readonly answers = signal<Record<string, string>>({});
  readonly result = signal<QuizBatchAnswerResponse | null>(null);

  setQuiz(
    hskLevel: number,
    quizType: QuizType,
    questions: QuizQuestion[],
  ): void {
    this.hskLevel.set(hskLevel);
    this.quizType.set(quizType);
    this.questions.set(questions);
    this.answers.set({});
    this.result.set(null);
  }

  setAnswer(questionId: string, answer: string): void {
    this.answers.update((current) => ({
      ...current,
      [questionId]: answer,
    }));
  }

  getAnswer(questionId: string): string | null {
    return this.answers()[questionId] ?? null;
  }

  setResult(result: QuizBatchAnswerResponse): void {
    this.result.set(result);
  }

  clearQuiz(): void {
    this.hskLevel.set(null);
    this.quizType.set(null);
    this.questions.set([]);
    this.answers.set({});
    this.result.set(null);
  }
}
