# Public Learning App Starter

A reusable full-stack starter for public learning experiences built with Django REST Framework and Angular.

This variant is intended for apps where visitors can use the learning flow without creating an account or signing in.

## Stack

- Django 6
- Django REST Framework
- Angular 21
- SQLite by default, with database configuration through environment variables
- CORS and Content Security Policy configuration

## Authentication status

- The Angular app does not register authentication routes, auth guards, a JWT interceptor, or an auth initializer.
- The Django API does not mount the starter's `/api/accounts/` authentication URLs.
- Django REST Framework defaults to `AllowAny` and has anonymous request throttling.
- SimpleJWT and PyJWT are not installed as dependencies in this variant.
- Django's built-in auth framework remains installed because it is part of Django's admin stack. There is no custom accounts app or public login/register API in this template.

**Important:** `AllowAny` is the global default for this public template. If you add private endpoints later, set explicit permission classes on those views rather than relying on the global default.

## Project structure

```text
backend/   Django + DRF API
frontend/  Angular application
```

## Run locally

### Backend (PowerShell)

```powershell
cd backend
py -m venv venv
.env\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py check
python manage.py migrate
python manage.py runserver localhost:8000
```

Set a strong, unique `SECRET_KEY` in `backend/.env` before using this outside local development. Do not commit `.env`.

Backend: `http://localhost:8000/`

### Frontend

Open another terminal:

```powershell
cd frontend
npm ci
npm start
```

Frontend: `http://localhost:4200/`

## Build and test

```powershell
# From backend/
python manage.py check
python manage.py test

# From frontend/
npm test -- --watch=false
npm run build
```

## Add your learning flow

1. Create a Django app for your learning domain (for example, `learning`).
2. Add public DRF views and URL routes for lessons, vocabulary, or quiz questions.
3. Add Angular pages and services that call those endpoints.
4. Add explicit permissions and validation to any endpoint that should not be public.
5. Run Django checks/tests and Angular tests/build before committing.

This is a starter, not a finished learning app; it does not include learning-specific models or endpoints yet.
