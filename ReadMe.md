# Relay API

[![CI](https://github.com/imviharevankar/relay-api/actions/workflows/ci.yml/badge.svg)](https://github.com/imviharevankar/relay-api/actions/workflows/ci.yml)

Backend for **Relay**, a workflow automation engine (think a small Zapier): users build
"when X happens, do Y then Z" flows, and workers run them reliably in the background.

This is a learning project built the way a production service would be: small pull
requests, tests for every change, and CI that must pass before anything is merged.

## Stack

Python 3.12 · FastAPI · SQLAlchemy 2 (async) · PostgreSQL · Redis · pytest · Ruff ·
Docker Compose · GitHub Actions

Planned: RabbitMQ workers, WebSocket live updates, Azure deployment, React frontend.

## Status

The project is built in sections. **Section 1: Auth and users** is in progress.

- [x] Password validator
- [x] Health endpoint
- [x] Settings and request schemas
- [ ] Database layer and migrations (Alembic)
- [ ] Register, login, JWT, protected routes
- [ ] Redis rate limiter
- [ ] Email OTP (verification and login)
- [ ] Dockerfile and Azure deployment

## Getting started

Requires Python 3.12 and Docker.

```bash
git clone https://github.com/imviharevankar/relay-api.git
cd relay-api

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

cp .env.dev .env                   # local settings (git-ignored)
docker compose up -d               # PostgreSQL and Redis
docker compose exec db createdb -U relay relay_test
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs for the interactive API docs.

## Tests and code quality

```bash
pytest                    # needs the containers above to be running
ruff check .              # lint
ruff format .             # format
```

CI runs the same checks on every pull request against real PostgreSQL and Redis.

## Configuration

Settings are read from environment variables (or `.env`). See `.env.dev` for a working
local example.

| Variable                      | Required | Purpose                                                    |
| ----------------------------- | -------- | ---------------------------------------------------------- |
| `DATABASE_URL`                | yes      | PostgreSQL connection string (asyncpg driver)              |
| `SECRET_KEY`                  | yes      | Signs JWTs; use 32+ random bytes outside local development |
| `REDIS_URL`                   | yes      | Redis connection string                                    |
| `ALGORITHM`                   | no       | JWT algorithm, default `HS256`                             |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | no       | Access token lifetime, default `30`                        |
| `OTP_TTL_SECONDS`             | no       | Email code validity, default `600`                         |
| `OTP_MAX_ATTEMPTS`            | no       | Wrong guesses before a code is voided, default `5`         |
| `OTP_RESEND_COOLDOWN_SECONDS` | no       | Wait between code requests, default `60`                   |

## Project layout

```text
app/
  main.py          FastAPI app and routes
  validators.py    Password rules
  core/            Settings and security helpers
  db/              Engine and session
  models/          SQLAlchemy models
  schemas/         Pydantic request and response models
tests/             pytest suite
```

## Working on this repo

- Branch from `main` (`feature/...`, `fix/...`, `ci/...`) and open a pull request.
- Commit messages follow Conventional Commits: `feat:`, `fix:`, `test:`, `chore:`.
- A pull request needs a green CI run before it is merged.
- Never commit `.env` or real secrets.
