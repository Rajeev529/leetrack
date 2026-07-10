# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Leettrack is a Django-based web application that helps users track and find curated LeetCode questions organized by company.

## Architecture
- **Project Root**: Contains `manage.py` and the `project/` configuration directory.
- **`project/`**: Django project settings, ASGI/WSGI configurations, and root URL routing.
- **`app/`**: The main Django application.
    - `views.py`: Contains the logic for fetching company-specific question lists and handling search.
    - `freq.py`: Stores hardcoded question frequencies (`count`) and company tier classifications (`tier`).
    - `models.py`: Currently empty; the application primarily uses CSV files for data storage.
- **`Companies/`**: A directory acting as a flat-file database. Each company has its own folder containing CSV files (e.g., `5. All.csv`, `2. Three Months.csv`) with question data.
- **`logos/`**: Stores company logo images used in the UI.
- **`templates/`**: Contains HTML templates (e.g., `homepage.html`, `search_page.html`, `qlist.html`).
- **`static/` & `staticfiles/`**: Project static assets.

## Common Commands
- **Run Development Server**: `python manage.py runserver`
- **Database Migrations**: 
    - Create migrations: `python manage.py makemigrations`
    - Apply migrations: `python manage.py migrate`
- **Running Tests**:
    - Run all tests: `python manage.py test`
    - Run specific app tests: `python manage.py test app`
- **Django Shell**: `python manage.py shell`
- **Dependency Management**: `pip install -r requirements.txt`

## Development Notes
- **Data Storage**: The app reads data from CSV files in the `Companies/` directory using `pandas`. If adding new companies, ensure the folder structure and CSV filenames match the expected patterns in `views.py`.
- **Company Logos**: Logos are expected to be in the `logos/` directory, named after the company (e.g., `Apple.png`).
- **Tiers**: Company tiers are defined in `app/freq.py`.
- **Deployment**: Configured for deployment on Vercel via `vercel.json`.
