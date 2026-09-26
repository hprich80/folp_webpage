# Friends of Larkhall Park — local prototype

Django + Wagtail, with SQLite for local use. Navigation: Home, About, Volunteering, News, Events, Instagram and Donate. News and future events are selected automatically for the homepage. All seeded announcements and dates are explicitly marked as samples.

## Run locally

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 127.0.0.1:8000
```

Open http://127.0.0.1:8000/.

## Docker preview

Create `.env` from `.env.example` and replace the placeholder key. Generate a key with:

```sh
python3 -c "import secrets; print(secrets.token_urlsafe(50))"
```

All hostnames are accepted for this prototype. Open `/admin/` on whichever host and port you use; no base URL configuration is needed. Absolute links in notification emails are not configured (email currently goes to console only), so Wagtail's corresponding warning is intentionally silenced. Permit inbound TCP 8000 in the security group for the public preview. Then:

```sh
docker compose up --build -d
docker compose logs -f web
docker compose down
```

Gunicorn serves Django; WhiteNoise serves collected CSS and other static files. Container settings disable debug and require an environment secret. The container runs as a non-root user. Startup migrates SQLite and seeds demo pages. One worker with two threads limits memory use for a small instance.

There are deliberately no persistent volumes. A stop/start of the same container retains data, but removing/replacing it (including `docker compose down`) loses edits. Local SQLite, credentials and `.env` are excluded from the image. Startup creates or resets the prototype administrator from `DEMO_ADMIN_USERNAME` and `DEMO_ADMIN_PASSWORD` (defaults: `folpadmin` / `larkhall`). Admin routes remain enabled, but do not send admin passwords or session cookies over a public HTTP connection; use local editing until HTTPS is configured. Uploaded media is not served by this preview configuration.

On an Apple Silicon Mac, build for `linux/amd64` if exporting an image for an x86 T3 instance, or build directly on the target instance. This configuration creates no AWS resources and deploys nothing automatically.

## Edit content locally

```sh
source .venv/bin/activate
python manage.py createsuperuser
```

Then open http://127.0.0.1:8000/admin/. Under Pages, edit Home or its child pages. Add a News page beneath News or an Event page beneath Events. Save draft, preview and publish. Home headline, introduction, membership copy and optional hero image are editable. Navigation uses the pages marked 'Show in menus'; Instagram and Donate remain fixed links. Group summaries are currently in templates.

The seed command is idempotent: it does not overwrite existing pages. Sample dates are relative to the first seed run. Expired events automatically disappear from the upcoming lists. News with future dates is excluded from listings; use Wagtail scheduled publishing to keep a future article itself unavailable until publication.

## Prototype boundaries

- `/membership/` displays `<Membermojo joining form>`. Replace the link with the approved Membermojo URL later.
- Donations are not connected; the Donate page provides an email enquiry link.
- No payment data or membership details are collected.
- The local server binds only to localhost. Settings use DEBUG and are not suitable for public hosting.
- Docker startup configures the requested demo credentials: `folpadmin` / `larkhall`. These are prototype-only credentials.
- Production will need deployment settings, HTTPS, persistent media, backups, email delivery and secret management.

## Assets and copy

Images are labelled placeholders; no external images or fonts are required. Background information comes from https://www.friendsoflarkhallpark.org.uk/about-us. Sample articles/events are fictional.

## Checks

```sh
python manage.py check
python manage.py test core
```
