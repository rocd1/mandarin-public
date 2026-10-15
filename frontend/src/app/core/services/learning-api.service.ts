import { HttpClient } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { map, Observable } from 'rxjs';

import { API_CONFIG } from '../config/api.config';
import { HSKLevel } from '../models/hsk-level.model';
import { StudyWordsResponse } from '../../core/models/study-word.model';

import {
  QuizBatchAnswerResponse,
  QuizBatchSubmission,
  QuizQuestionsResponse,
  QuizType,
} from '../models/quiz.models';


interface PaginatedResponse<T> {
  results: T[];
}

@Injectable({
  providedIn: 'root',
})
export class LearningApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = `${API_CONFIG.baseUrl}/api/learning`;

  getLevels(): Observable<HSKLevel[]> {
    return this.http
      .get<HSKLevel[] | PaginatedResponse<HSKLevel>>(
        `${this.baseUrl}/levels/`,
      )
      .pipe(
        map((response) =>
          Array.isArray(response) ? response : response.results,
        ),
      );
  }

  getStudyWords(
    hskLevel: number,
    page: number,
    pageSize = 20,
  ): Observable<StudyWordsResponse> {
    return this.http.get<StudyWordsResponse>(
      `${this.baseUrl}/study/`,
      {
        params: {
          hsk_level: hskLevel,
          page,
          page_size: pageSize,
        },
      },
    );
  }


  getQuizQuestions(
    hskLevel: number,
    quizType: QuizType,
  ): Observable<QuizQuestionsResponse> {
    return this.http.get<QuizQuestionsResponse>(
      `${this.baseUrl}/quiz/questions/`,
      {
        params: {
          hsk_level: hskLevel,
          quiz_type: quizType,
        },
      },
    );
  }

  submitQuiz(
    submission: QuizBatchSubmission,
  ): Observable<QuizBatchAnswerResponse> {
    return this.http.post<QuizBatchAnswerResponse>(
      `${this.baseUrl}/quiz/answers/`,
      submission,
    );
  }

}
