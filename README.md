# Mandarin Public Learning App

A Mandarin vocabulary learning app built with **Django REST Framework** and **Angular**. Learners can browse HSK vocabulary, study words with flashcards, take multiple-choice quizzes, and review their results without creating an account.

## Features

- **HSK levels:** Browse vocabulary by level, from HSK 1 to HSK 7–9.
- **Vocabulary study:** View vocabulary in a paginated list.
- **Flashcards:** Reveal word information while studying.
- **Multiple-choice quizzes:** Practice four quiz types:
  - Hanzi to Meaning
  - Meaning to Hanzi
  - Hanzi to Pinyin
  - Pinyin to Hanzi
- **Quiz navigation:** Move between questions and change selected answers before submitting.
- **Quiz results:** View your score, correct and incorrect counts, and answer-by-answer review.
- **Guest access:** All learning features are available without login or registration.

## Technology Stack

### Backend
- Python
- Django
- Django REST Framework
- SQLite for local development

### Frontend
- Angular
- TypeScript
- HTML and CSS

## Project Structure

```text
mandarin-public/
├── backend/
│   ├── config/
│   ├── learning/
│   │   ├── api/
│   │   └── data/
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── angular.json
│   └── package.json
└── README.md
```

The exact files and folders may vary slightly as the project evolves.

## Requirements

Install the following before running the app:

- Python
- Node.js and npm
- Angular CLI (optional if using `npx ng`)

## Backend Setup

Open PowerShell and navigate to the backend:

```powershell
cd E:\django-projects\mandarin-public\backend
```

Create a virtual environment if one does not already exist:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the backend dependencies:

```powershell
python -m pip install -r requirements.txt
```

Apply database migrations:

```powershell
python manage.py migrate
```

### Import HSK vocabulary

Place the vocabulary dataset files `1.json` through `7.json` in:

```text
backend/learning/data/
```

Run the project's vocabulary import command:

```powershell
python manage.py import_vocabulary
```

If the vocabulary has already been imported, there is no need to import it again unless you are updating or rebuilding the database.

### Start the backend

```powershell
python manage.py runserver
```

The backend API is available at:

`http://localhost:8000/`

## Frontend Setup

Open a second PowerShell terminal:

```powershell
cd E:\django-projects\mandarin-public\frontend
```

Install the dependencies:

```powershell
npm install
```

Start the Angular development server:

```powershell
npx ng serve
```

Open the app at:

`http://localhost:4200/`

Keep both development servers running while using the app locally.

## Learning API Endpoints

The learning API is available under `/api/learning/`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/learning/levels/` | Retrieve available HSK levels |
| GET | `/api/learning/study/` | Retrieve paginated vocabulary |
| GET | `/api/learning/quiz/question/` | Retrieve a single quiz question |
| GET | `/api/learning/quiz/questions/` | Retrieve a batch of quiz questions |
| POST | `/api/learning/quiz/answer/` | Submit one answer |
| POST | `/api/learning/quiz/answers/` | Submit a batch of answers |

Quiz requests support the following quiz types:

```text
hanzi_to_meaning
meaning_to_hanzi
hanzi_to_pinyin
pinyin_to_hanzi
```

Quiz questions can be filtered by HSK level using the `hsk_level` query parameter and by quiz type using `quiz_type`, where supported.

Example:

```text
http://localhost:8000/api/learning/quiz/questions/?hsk_level=1&quiz_type=hanzi_to_meaning
```

The batch-answer endpoint accepts submitted answers and returns the score and correctness results. The frontend combines those results with the questions and selected answers held in memory to display the review page.

## Authentication and Data

This is a **public, no-login learning app**.

- No login or registration is required.
- No JWT authentication is used for the learning flow.
- Quiz selections and results are kept in frontend memory.
- Quiz results are not saved as user history or personal progress.
- Refreshing the results page loses the in-memory quiz state.

## Production Build

Build the Angular frontend:

```powershell
cd E:\django-projects\mandarin-public\frontend
npx ng build
```

Before deploying, configure Django and Angular for the production environment, including allowed hosts, CORS and CSRF settings where applicable, HTTPS, environment secrets, and the production database and static-file setup.

## Notes

This project is intended as a reusable public Mandarin-learning app. Keep authentication and user-progress features out of this version unless the app's requirements change.
