import {
  ApplicationConfig,
  ErrorHandler,
  provideBrowserGlobalErrorListeners,
} from '@angular/core';

import {
  provideHttpClient,
} from '@angular/common/http';

import { provideRouter } from '@angular/router';

import { routes } from './app.routes';


import { AppErrorHandler } from './core/errors/app-error-handler';


export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),

    {
      provide: ErrorHandler,
      useClass: AppErrorHandler,
    },

    provideRouter(routes),

    provideHttpClient(),
  ],
};