
import { Component, OnInit, inject, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { LearningApiService } from '../../core/services/learning-api.service';

import {
  StudyWord,
  StudyWordsResponse,
} from '../../core/models/study-word.model';

@Component({
  selector: 'app-study',
  imports: [RouterLink],
  templateUrl: './study.html',
  styleUrl: './study.css',
})
export class Study implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly learningApi = inject(LearningApiService);

  private readonly flippedCards = signal<Set<number>>(new Set());

  readonly level = signal(1);
  readonly words = signal<StudyWord[]>([]);
  readonly page = signal(1);
  readonly pageSize = 20;
  readonly totalCount = signal(0);
  readonly totalPages = signal(0);
  readonly loading = signal(true);
  readonly error = signal('');

  ngOnInit(): void {
    this.route.paramMap.subscribe((params) => {
      const level = Number(params.get('level'));

      if (!Number.isInteger(level) || level < 1 || level > 7) {
        this.error.set('Please select a valid HSK level.');
        this.loading.set(false);
        return;
      }

      this.level.set(level);
      this.loadPage(1);
    });
  }

  loadPage(pageNumber: number): void {
    this.loading.set(true);
    this.error.set('');
    this.flippedCards.set(new Set());

    this.learningApi
      .getStudyWords(this.level(), pageNumber, this.pageSize)
      .subscribe({
        next: (response: StudyWordsResponse) => {
          this.words.set(response.results);
          this.page.set(response.page);
          this.totalCount.set(response.count);
          this.totalPages.set(response.total_pages);
          this.loading.set(false);
        },
        error: (err: unknown) => {
          console.error('Unable to load vocabulary.', err);
          this.error.set(
            'Unable to load vocabulary. Please check your connection and try again.',
          );
          this.loading.set(false);
        },
      });
  }

  
  isCardFlipped(wordId: number): boolean {
    return this.flippedCards().has(wordId);
  }

  toggleCard(wordId: number): void {
    this.flippedCards.update((current) => {
      const updated = new Set(current);

      if (updated.has(wordId)) {
        updated.delete(wordId);
      } else {
        updated.add(wordId);
      }

      return updated;
    });
  }



  previousPage(): void {
    if (this.page() > 1) {
      this.loadPage(this.page() - 1);
    }
  }

  nextPage(): void {
    if (this.page() < this.totalPages()) {
      this.loadPage(this.page() + 1);
    }
  }
}
