# Deploy Kuriftu Hospitality on Render

## What went wrong before

Your build command was corrupted (e.g. `pip inspip` and duplicated text). Use **exactly** one of the options below—copy/paste with no edits.

## Option A — Web Service (manual)

1. **New → Web Service** → connect `https://github.com/jho-G/Kuriftu-Hospitality`
2. **Root Directory:** `backend`  ← required for this repo layout
3. **Runtime:** Python 3
4. **Build Command** (copy the whole line):

   ```text
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate --noinput
   ```

5. **Start Command:**

   ```text
   gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
   ```

6. **Environment → Add:**

   | Key | Value |
   |-----|--------|
   | `PYTHON_VERSION` | `3.12.8` |
   | `DEBUG` | `False` |
   | `DJANGO_SECRET_KEY` | (your secret) |
   | `OPENROUTER_API_KEY` | (your OpenRouter key) |
   | `DATABASE_URL` | From PostgreSQL (see below) |
   | `ALLOWED_HOSTS` | `.onrender.com,your-service-name.onrender.com` |
   | `CSRF_TRUSTED_ORIGINS` | `https://your-service-name.onrender.com` |
   | `SITE_URL` | `https://your-service-name.onrender.com` |
   | `CORS_ALLOWED_ORIGINS` | `https://your-service-name.onrender.com` |

   Replace `your-service-name` with your real Render hostname.

7. **Database:** New → PostgreSQL → copy **Internal Database URL** into `DATABASE_URL` on the web service.

8. Deploy. First deploy runs migrations against Postgres.

## Option B — Blueprint

- **New → Blueprint** → select this repo.
- If `render.yaml` is at the **repo root**, Render should pick `rootDir: backend` and the correct `buildCommand`.

## Option C — Shell script build

- **Root Directory:** `backend`
- **Build Command:**

  ```text
  chmod +x render-build.sh && bash render-build.sh
  ```

## Python version

If Render picks **3.14**, set **`PYTHON_VERSION` = `3.12.8`** in the environment (and keep `backend/runtime.txt` as `python-3.12.8`).

## After deploy

- Open `https://YOUR-SERVICE.onrender.com/`
- Admin: `/admin/` (create superuser via Render shell: `python manage.py createsuperuser`)
