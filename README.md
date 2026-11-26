# ChronicleTech &mdash; Next-Gen Tech Publishing Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-6.1-darkgreen.svg?logo=django&logoColor=white)](https://djangoproject.com)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20ORM-blueviolet.svg)](#database-architecture)
[![Tests](https://img.shields.io/badge/Tests-17%20Passed-brightgreen.svg)](#testing)
[![Live Feed](https://img.shields.io/badge/Live%20API-REST%20%7C%20Cached%20300s-success.svg)](#live-tech-wire)
[![Design](https://img.shields.io/badge/Design-Modern%20Dark%20System-06b6d4.svg)](#frontend--ui)

**ChronicleTech** is a production-ready, full-stack tech editorial and publication platform built with Python and Django. Designed around the technology landscape of 2026–2035, the platform delivers analytical dispatches across artificial intelligence, sovereign privacy, self-healing hardware, and ambient computing, complemented by a **live, real-time external tech news wire**.

---

## Key Features

- **Live External REST API Integration (Real-Time)**:
  - Consumes live developer and technology news via external REST APIs with dynamic topic filtering (`AI`, `Python`, `Cloud Architecture`, `Cybersecurity`, `DevOps & SRE`).
  - Implements **in-memory caching (TTL 300s)** to eliminate third-party rate limits, query-based cache-busting (`?refresh=true`), and graceful network fallbacks to offline cached dispatches.
  - Exposes an internal JSON API endpoint (`/api/live-news/`) for decoupled client-side data consumption.
- **Robust Relational Data Models**:
  - `Article`: Categorized dispatches with SEO-friendly auto-generated slugs, atomic view counters (`F('views_count') + 1`), read-time metrics, and featured spotlight flags.
  - `Category`: Domain taxonomies with customized color badges and cascading relationships.
  - `Event`: Global industry summits and expos with conference links and calendar badges.
- **Dynamic Search & Multi-Field Filtering**:
  - Full-text search across titles, summaries, content, and authors using Django `Q` expressions.
  - Taxonomy filtering by category slugs (`?category=artificial-intelligence`).
- **Server-Side Pagination**:
  - Clean pagination preserving active search queries and filter parameters across page traversals.
- **Automated Data Seeding CLI**:
  - Custom Django management command (`python manage.py seed_data`) to deterministically populate initial categories, rich articles, and tech events in one command.
- **Customized Django Admin Panel**:
  - Filter facets, search indexing, auto-prepopulated slugs, and date hierarchy navigation for content editors.
- **High-Fidelity Modern UI**:
  - Bespoke dark mode design system built with CSS Custom Properties, CSS Grid, and Flexbox.
  - Top scroll reading progress bar, author avatar badges, key takeaway callout boxes, and related article recommendations.
  - Zero heavy frontend framework dependencies for sub-second page loads.
- **Automated Test Coverage**:
  - 17 unit and integration tests verifying model invariants, slug collision resolution, search queries, pagination, live API integration, and atomic counter integrity.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12, Django 6.1 (MVT Architecture) |
| **Database** | SQLite (development) / PostgreSQL-ready Django ORM |
| **Frontend** | HTML5, Modern CSS3 (Variables, Grid, Flexbox), Vanilla JavaScript |
| **Testing** | Django Test Framework / `TestCase` (15 passing tests) |
| **Tooling** | Django Management Commands, Pip, Virtualenv |

---

## Architecture & Directory Structure

```text
article/
├── .gitignore                      # Git exclusion rules
├── requirements.txt                # Project dependencies
├── README.md                       # Documentation & setup guide
├── myenv/                          # Python virtual environment
└── myproject/
    ├── manage.py                   # Django CLI entrypoint
    ├── db.sqlite3                  # SQLite relational database
    ├── static/                     # Static assets
    │   ├── css/
    │   │   └── style.css           # Modern design system & components
    │   └── img/                    # High-res article photography
    ├── myproject/
    │   ├── settings.py             # Project configuration
    │   ├── urls.py                 # Root URL router
    │   ├── wsgi.py / asgi.py       # WSGI/ASGI gateways
    │   └── temp/                   # Base template layouts
    │       ├── main.html           # Master layout & footer
    │       └── nav.html            # Sticky navigation & search bar
    └── base/                       # Core publishing application
        ├── models.py               # Category, Article, Event models
        ├── views.py                # Business logic, search, pagination
        ├── urls.py                 # App route mapping
        ├── admin.py                # Django Admin dashboard customization
        ├── tests.py                # 15 automated unit & integration tests
        ├── management/
        │   └── commands/
        │       └── seed_data.py    # Deterministic database seeder CLI
        └── templates/              # Application views
            ├── home.html           # Hero, filter pills, article grid
            ├── read.html           # In-depth reading view & related posts
            ├── news.html           # Editorial news wire feed
            ├── events.html         # Global summits & expos
            └── about.html          # Mission & architectural specs
```

---

## Quickstart & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/chronicletech.git
cd article
```

### 2. Create and activate a virtual environment
```bash
# On Windows
python -m venv myenv
.\myenv\Scripts\activate

# On macOS/Linux
python3 -m venv myenv
source myenv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply database migrations
```bash
python myproject/manage.py migrate
```

### 5. Seed initial data
```bash
python myproject/manage.py seed_data
```

### 6. Run automated tests
```bash
python myproject/manage.py test base
```

### 7. Start the development server
```bash
python myproject/manage.py runserver
```
Visit **http://127.0.0.1:8000** in your browser.

---


---

## License

This project is licensed under the MIT License — see the LICENSE file for details.
