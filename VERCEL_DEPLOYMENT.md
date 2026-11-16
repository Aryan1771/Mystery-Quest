# Vercel deployment (Django + Turso)

This project is configured to use local SQLite for development and Turso/libSQL when the
Turso environment variables are present. Vercel deployments must use Turso because the
Vercel function filesystem is not a durable database.

## 1. Vercel project environment variables

In Vercel, open **Project → Settings → Environment Variables** and add the following
for **Production** and **Preview**:

| Name | Value |
| --- | --- |
| `DJANGO_SECRET_KEY` | A newly generated, long random Django secret |
| `DJANGO_DEBUG` | `false` |
| `TURSO_DB_URL` | The database URL from the Turso dashboard (usually `libsql://...`) |
| `TURSO_AUTH_TOKEN` | A database auth token generated in Turso |
| `DJANGO_ALLOWED_HOSTS` | `.vercel.app` (add your custom domain, if any, comma-separated) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` (add your custom domain as an HTTPS origin, if any) |

Do not put real values in this repository, commit a real `.env` file, or share the Turso
token in chat. The `.env.example` file contains placeholders only.

Generate a Django secret locally with:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 2. Initialise the empty Turso database

Install this repository's requirements locally, then set the same Turso URL and token in
your local shell. For PowerShell:

```powershell
$env:DJANGO_DEBUG = "false"
$env:DJANGO_SECRET_KEY = "paste-your-generated-secret"
$env:TURSO_DB_URL = "libsql://your-database-name-your-org.turso.io"
$env:TURSO_AUTH_TOKEN = "paste-your-turso-token"
python manage.py migrate
python manage.py createsuperuser
```

Run migrations once before using the deployed site. Do not run migrations concurrently from
multiple preview deployments.

## 3. Deploy

Connect the GitHub repository `Aryan1771/Mystery-Quest` to Vercel and use the repository
root as the project root. Select the Django framework preset (or allow Django auto-detection).
Vercel detects `manage.py`, resolves `WSGI_APPLICATION`, runs `collectstatic` when
`STATIC_ROOT` is set, and serves collected static files through its CDN. No custom
`vercel.json` or `api/index.py` is needed for current Django support.

After adding or changing environment variables, redeploy so the new values are applied.

## Important production notes

- The Turso Django backend is a third-party package. It supports Django ORM and migrations,
  but its remote HTTP mode has transaction limitations; test writes and scoring flows
  thoroughly before treating this as a high-traffic production service.
- Do not run `python manage.py seed_data` on production. That demo command creates accounts
  with published sample passwords, including a predictable administrator account. Create
  your own administrator with `createsuperuser` instead.
- The database starts empty. Add your cases, clues, suspects, and evidence through the
  protected management UI or Django admin after creating your administrator.
- Vercel's function filesystem is ephemeral. Uploaded case/suspect/clue images are not
  durable with the current `MEDIA_ROOT` configuration. Do not rely on image uploads until
  external object storage is configured.
- Django migrations and application tables live in Turso; static assets are collected at
  build time and served by Vercel.
