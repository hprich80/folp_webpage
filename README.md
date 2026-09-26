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

## Edit content

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
- Create your own editor credentials; no default account or password is shipped.
- Production will need deployment settings, HTTPS, persistent media, backups, email delivery and secret management.

## Assets and copy

Images are labelled placeholders; no external images or fonts are required. Background information comes from https://www.friendsoflarkhallpark.org.uk/about-us. Sample articles/events are fictional.

## Checks

```sh
python manage.py check
python manage.py test core
```
