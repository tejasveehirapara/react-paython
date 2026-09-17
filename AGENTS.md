# AGENTS.md

## Project

Full-stack application with:
- React frontend
- Python FastAPI backend

## Frontend

### Stack
- React
- Vite
- JavaScript
- Tailwind CSS
- React Router
- Axios
- React Hook Form
- Lucide React

### Rules
- Use functional components.
- Use reusable components.
- Keep API calls inside `services/`.
- Do not put API calls directly inside UI components.
- Use environment variables for API URLs.
- Handle loading, error and empty states.
- Do not duplicate components.

Frontend structure:

frontend/
  src/
    assets/
    components/
    constants/
    hooks/
    layouts/
    pages/
    routes/
    services/
    utils/

## Backend

### Stack
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL

### Rules
- Use Python type hints.
- Use async endpoints where appropriate.
- Keep routes/controllers thin.
- Put business logic inside services.
- Put database models inside models/.
- Put request/response schemas inside schemas/.
- Keep configuration inside core/.
- Use environment variables for secrets.
- Never hardcode passwords, API keys or database credentials.
- Add proper HTTP status codes.
- Add validation using Pydantic.
- Add error handling.
- Add API tests.

Backend structure:

backend/
  app/
    api/
    models/
    schemas/
    services/
    core/
    db/
    main.py
  tests/

## API

Use REST APIs.

Example:

GET    /api/v1/clients
GET    /api/v1/clients/{id}
POST   /api/v1/clients
PUT    /api/v1/clients/{id}
DELETE /api/v1/clients/{id}

API responses should have a consistent structure.

## Development

Frontend:
npm run dev

Backend:
uvicorn app.main:app --reload

## Quality

Before completing a task:

- Run frontend build.
- Run backend tests.
- Check API errors.
- Check frontend console errors.
- Check CORS.
- Check API/frontend integration.
- Do not leave broken placeholder code.