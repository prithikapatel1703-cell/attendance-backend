# College deployment checklist

Use this for deploying the attendance backend in a college environment.

## Before deployment

1. **Run API tests**
   ```bash
   python manage.py test core.tests -v 2
   ```
   All tests should pass.

2. **Set environment variables** (do not use defaults in production):

   | Variable | Example | Purpose |
   |----------|---------|---------|
   | `DJANGO_SECRET_KEY` | Long random string (e.g. from `python -c "import secrets; print(secrets.token_urlsafe(50))"`) | Required for security |
   | `DJANGO_DEBUG` | `False` | Never use `True` in production |
   | `DJANGO_ALLOWED_HOSTS` | `attendance.yourcollege.edu,www.attendance.yourcollege.edu` | Comma-separated hostnames |
   | `CORS_ALLOWED_ORIGINS` | `https://attendance.yourcollege.edu` | Frontend URL(s) (comma-separated) |

3. **Database**: Default is SQLite (`db.sqlite3`). For college use, consider PostgreSQL:
   - Install `psycopg2`, set `DATABASES` in settings from env (e.g. `DATABASE_URL`).
   - Run `python manage.py migrate`.

4. **Static files**: For production, run:
   ```bash
   python manage.py collectstatic --noinput
   ```
   and serve static files via your web server (e.g. Nginx) or a CDN.

5. **HTTPS**: Serve the app over HTTPS only. Use your college’s reverse proxy (e.g. Nginx/Apache) with SSL.

6. **Frontend**: Point the frontend API base URL to your deployed backend (e.g. `https://api.attendance.yourcollege.edu`) and build the frontend for production.

## Quick production env example (Linux/macOS)

```bash
export DJANGO_SECRET_KEY="your-long-random-secret"
export DJANGO_DEBUG="False"
export DJANGO_ALLOWED_HOSTS="attendance.yourcollege.edu"
export CORS_ALLOWED_ORIGINS="https://attendance.yourcollege.edu"
```

Then run the app with a production WSGI server (e.g. Gunicorn) behind a reverse proxy.
