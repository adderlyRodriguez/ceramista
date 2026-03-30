# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Ceramista is a Flask portfolio web app for a ceramics artist. It allows an admin to manage projects (images/videos) uploaded to Cloudinary, displayed publicly in a responsive gallery. Categories organize the portfolio and appear in the navigation.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Run production server
gunicorn app:app

# Database migrations
flask db migrate -m "description"
flask db upgrade
```

Environment variables are loaded from `.env`. The app uses SQLite by default (`instance/db.sqlite3`), or the `DATABASE_URL` env var if set.

## Architecture

All application logic lives in `app.py` — models, routes, and configuration are defined there (not in `models.py`, which is unused).

**Models:** `Category` (id, name) and `Project` (id, title, description, media_url, media_type, date, category_id). Projects reference categories via foreign key.

**Admin auth:** Session-based. Visiting `/admin` with the correct `ADMIN_CODE` sets `session['admin'] = True`. Protected routes check this flag.

**Media uploads:** Images and videos are uploaded to Cloudinary on project create/edit. The Cloudinary URL is stored in `media_url`; `media_type` is `'image'` or `'video'`.

**Category navigation:** A `@app.context_processor` injects all categories into every template so the nav bar is always populated.

**Two public views:**
- `/` (`portfolio.html`) — chronological grid of all projects
- `/inicio` (`inicio.html`) — projects grouped by category

**Contact form** (`/contact`) sends email via Gmail SMTP using credentials from `.env`.

**Deployment:** `Procfile` for Heroku, `render.yaml` for Render.com (with a 1GB disk mount for SQLite persistence).
