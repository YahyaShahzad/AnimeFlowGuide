# AnimeFlowGuide

A small Flask app for curated anime watch orders.

## Deployment

You can deploy the app in several ways. The repository includes samples for Docker and a `Procfile` for platforms like Heroku.

### Environment variables

- `DATABASE_URL` - SQLAlchemy connection string (default: `sqlite:///anime.db`)
- `SECRET_KEY` - Flask secret key
- `FLASK_ENV` - `production` or `development`
- `PORT` - port to bind (used by Procfile / Docker)

### Run locally (development)

1. Create virtualenv and install deps:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Export env and run:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

### Run with Gunicorn (production)

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Or use the `Procfile` on Heroku-like platforms (heroku, fly.io, etc.).

### Docker

Build and run:

```bash
docker build -t animeflow .
docker run -p 8000:8000 --env-file .env animeflow
```

Or with docker compose:

```bash
cp .env.example .env
# edit .env as needed
docker-compose up --build -d
```

### Database migrations

This project includes `Flask-Migrate` in `requirements.txt`. To use migrations:

```bash
flask db init
flask db migrate -m "Initial"
flask db upgrade
```

(If you prefer, the app will still create tables automatically with `db.create_all()`.)

## Notes

- Ensure `SECRET_KEY` is set in production.
- If using a remote DB (Postgres), set `DATABASE_URL` accordingly.
