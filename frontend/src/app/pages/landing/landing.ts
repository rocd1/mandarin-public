import { Footer } from '../../shared/ui/footer/footer';
import { Component, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';

import { HSKLevel } from '../../core/models/hsk-level.model';
import { LearningApiService } from '../../core/services/learning-api.service';

@Component({
  selector: 'app-landing',
  imports: [RouterLink, Footer],
  templateUrl: './landing.html',
  styleUrl: './landing.css',
})
export class Landing implements OnInit {
  private readonly learningApi = inject(LearningApiService);

  readonly levels = signal<HSKLevel[]>([]);
  readonly loading = signal(true);
  readonly error = signal('');

  ngOnInit(): void {
    this.learningApi.getLevels().subscribe({
      next: (levels) => {
        this.levels.set(levels);
        this.loading.set(false);
      },
      error: (err: unknown) => {
        console.error('Unable to load HSK levels.', err);
        this.error.set(
          'Unable to load HSK levels. Please check that the Django backend is running.',
        );
        this.loading.set(false);
      },
    });
  }
}
