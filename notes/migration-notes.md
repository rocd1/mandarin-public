# Mandarin Public — Development and Migration Notes

## 1. Project Overview

**Project name:** Mandarin Public

**Project path:** `E:\django-projects\mandarin-public`

**Purpose:** Build a Mandarin Chinese vocabulary learning app using Django REST Framework and Angular, without requiring users to register or log in.

This project was generated from the PublicLearning version of the Project App Starter.

## 2. Technology Stack

- **Backend:** Python, Django, Django REST Framework
- **Frontend:** Angular
- **Database:** SQLite for initial development
- **Vocabulary source:** `drkameleon/complete-hsk-vocabulary`
- **Development environment:** Windows, PowerShell, Visual Studio Code

## 3. Project Goals

The initial version will focus on the core Mandarin learning experience:

1. Browse vocabulary by HSK level.
2. Review Chinese vocabulary using flashcards.
3. Practice multiple-choice quizzes.
4. Receive immediate feedback on answers.
5. View quiz results.
6. Optionally add local learning progress later.

The app will not require user accounts, login, registration, JWT authentication, or user-specific server-side progress tracking in the initial version.

## 4. Reference Project

The existing project is located at:

`E:\django-projects\mandarin-v4`

It contains previously developed Mandarin learning functionality, including vocabulary models, imported HSK vocabulary, quiz generation, and quiz API endpoints.

The reference project must remain unchanged while features are selectively migrated.

## 5. Migration Plan

### Step 1 — Project foundation

- [x] Generate the new project from the PublicLearning template.
- [x] Keep the existing `mandarin-v4` project unchanged.
- [x] Establish a separate project directory.

### Step 2 — Vocabulary dataset and models

- [ ] Inspect the existing HSK vocabulary dataset.
- [ ] Copy the necessary dataset files into the new project.
- [ ] Create or adapt the `HSKLevel` model.
- [ ] Create or adapt the `Vocabulary` model.
- [ ] Create and apply Django migrations.
- [ ] Test the models and database.

### Step 3 — Vocabulary importer

- [ ] Migrate the vocabulary import management command.
- [ ] Import the HSK vocabulary dataset.
- [ ] Verify imported counts and representative vocabulary entries.

### Step 4 — Quiz backend

- [ ] Migrate the quiz types and question generator.
- [ ] Migrate distractor generation and validation.
- [ ] Add public quiz question and answer endpoints.
- [ ] Test all four quiz types.

### Step 5 — Angular learning experience

- [ ] Build the learning home page.
- [ ] Add HSK level selection and vocabulary browsing.
- [ ] Add flashcards.
- [ ] Add quiz and results pages.
- [ ] Connect the frontend to the backend API.

### Step 6 — Final testing

- [ ] Run Django system checks and backend tests.
- [ ] Run Angular tests and production build.
- [ ] Verify that no authentication is required for the learning flow.
- [ ] Update the main README with setup and usage instructions.

## 6. Migration Rules

- Do not modify or delete the existing `mandarin-v4` project.
- Do not copy authentication-specific code into the new project.
- Reuse working vocabulary and quiz logic where appropriate.
- Keep the new project's settings, URLs, models, and dependencies independent.
- Test each migration stage before continuing to the next stage.
- Never commit `backend/.env` or expose the Django secret key.

## 7. Current Status

**Completed:** PublicLearning project generated successfully.

**Next task:** Inspect and migrate the HSK vocabulary dataset and the `HSKLevel` and `Vocabulary` models.
