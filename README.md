# UK Schools Explorer

UK Schools Explorer is a database-driven Flask application built with open government data from the Planning Data platform. It explores schools in England and the local authorities they belong to, using linked tables, filterable list pages, detail pages, summary statistics, comparison views, and automated tests.

## Project Summary

- Framework: Flask
- Database: SQLite
- ORM: Flask-SQLAlchemy
- Test framework: pytest
- Data source: Planning Data / `data.gov.uk`
- Records loaded for the coursework subset: `4000` schools linked to `379` local authorities

## Features

- Browse schools and local authorities
- View linked detail pages for schools and authorities
- Filter schools by name, authority, type, and status
- Compare two schools side by side
- Show summary statistics on the home page
- Translate raw government codes into readable labels
- Handle missing pages with custom `404` and `500` templates
- Run automated tests for routes, relationships, and the loader

## Dataset and Licence

This project uses open public sector information published through the Planning Data service.

- Educational establishment dataset:
  https://www.planning.data.gov.uk/dataset/educational-establishment
- Local authority dataset:
  https://www.planning.data.gov.uk/dataset/local-authority
- Planning Data platform overview:
  https://www.planning.data.gov.uk/about

Dataset facts checked on **27 April 2026**:

- Educational establishments total: `47,047`
- Local authorities total: `379`
- Both dataset pages reported the collector last ran on **27 April 2026**

Licence:

- Open Government Licence v3.0
- Attribution: `© Crown copyright and database right 2026`

## Data Model

The application uses two linked tables:

1. `local_authorities`
2. `schools`

Relationship:

- one local authority has many schools
- each school belongs to one local authority

The join is based on:

- `educational-establishment.local-authority-district`
- `local-authority.local-authority-district`

Within the app:

- `local_authorities.code` stores the district code such as `E09000001`
- `local_authorities.short_code` stores the short authority reference such as `ADU`

## Project Structure

```text
app/                 Flask application package
app/templates/       Jinja templates
app/static/          CSS
data/raw/            Downloaded CSV files
instance/            SQLite database file
scripts/             Data-loading script
tests/               pytest test suite
config.py            Application configuration
run.py               Local Flask entry point
render.yaml          Render deployment blueprint
```

## Setup and Installation

### Requirements

- Python 3.13 or similar modern Python 3 version
- `pip`

### Local Setup

```bash
cd /Users/olaluwoyeolalekantaofeek/Documents/MLOps/uk-schools-explorer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Downloading the Data

Download these CSV files into [data/raw](/Users/olaluwoyeolalekantaofeek/Documents/MLOps/uk-schools-explorer/data/raw):

- `educational-establishment.csv`
- `local-authority.csv`

The loader expects these filenames exactly.

## Loading the Coursework Subset

The coursework requires between `2000` and `7000` records. This project uses a subset of `4000` schools.

Load the data with:

```bash
MAX_SCHOOL_RECORDS=4000 python3 scripts/load_data.py
```

Expected output:

```text
Loaded 4000 schools
Loaded 379 local authorities
```

## Running the Application Locally

Start the development server with:

```bash
python3 run.py
```

Then open:

```text
http://127.0.0.1:5000
```

## Testing

Run the automated tests with:

```bash
pytest tests
```

Current status during development:

- `10 passed`

The test suite covers:

- successful route responses
- missing-page handling
- school and authority relationships
- compare page behavior
- loader failure for missing files

## Error Handling

The application includes custom templates for:

- `404 Not Found`
- `500 Internal Server Error`

This improves usability and helps meet the coursework requirement for appropriate error handling.

## Design and Development Notes

The project was developed incrementally:

1. Scaffold the Flask structure
2. Inspect the real CSV fields
3. Correct the schema and table join
4. Load a coursework-sized subset
5. Improve the interface and data presentation
6. Add tests and rerun them after each significant change

Important implementation decisions:

- The raw datasets did not fully match the first schema assumptions, so the table relationship was corrected to use `local-authority-district`.
- Government codes for school type, school status, and region were mapped to readable labels in the interface.
- The authorities list was refined to focus on authorities with linked schools in the loaded subset by default.

## Deployment on Render

This repository includes [render.yaml](/Users/olaluwoyeolalekantaofeek/Documents/MLOps/uk-schools-explorer/render.yaml:1) for deployment on Render.

### Render Configuration

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn --bind 0.0.0.0:$PORT run:app`
- Secret key: generated by Render from `render.yaml`

### Important Deployment Note

Render requires applications to bind to `0.0.0.0` and use the platform `PORT`, which is why the start command uses:

```bash
gunicorn --bind 0.0.0.0:$PORT run:app
```

Render gives each deployed web service a public URL like:

```text
https://your-service-name.onrender.com
```

Your local URL `http://127.0.0.1:5000` is **not** a Render deployment URL.

### SQLite on Render

This project currently uses SQLite. Render’s documentation says web services use an **ephemeral filesystem by default**, meaning runtime file changes do not survive redeploys unless you attach a persistent disk. Because this app is read-focused and the coursework dataset can be shipped with the project, it can run as a simple deployment, but a persistent disk is the safer choice if you want the database file to persist after runtime changes. Sources:

- Render Flask deployment docs: https://render.com/docs/deploy-flask
- Render deploy docs: https://render.com/docs/deploys/
- Render persistent disk docs: https://render.com/docs/disks
- Render web services docs: https://render.com/docs/web-services

### Steps to Deploy on Render

1. Push this project to a GitHub, GitLab, or Bitbucket repository.
2. Sign in to Render.
3. Create a new Web Service or Blueprint from the repository.
4. If deploying as a Blueprint, allow Render to read `render.yaml`.
5. Confirm the build and start commands.
6. After the deploy finishes, open the generated `onrender.com` URL.
7. Add that public URL to your final PDF report and this README.

### Deployment Status

- Local application: working
- Render configuration: prepared
- GitHub repository: https://github.com/Oluwaniyi127665/cs551p
- Live public Render URL: pending deployment

Example placeholder:

```text
Render URL: https://your-service-name.onrender.com
```

## Maintenance

If you need to refresh the dataset:

1. Replace the CSV files in `data/raw/`
2. Reload the subset with `MAX_SCHOOL_RECORDS=4000 python3 scripts/load_data.py`
3. Rerun `pytest tests`
4. Restart the app locally or redeploy on Render

## Submission Checklist

- Flask app runs locally
- Two linked tables are implemented
- Open data source is documented
- Dataset subset is within `2000-7000` records
- Templates are used across pages
- Error pages are included
- Tests run successfully
- README explains setup, testing, maintenance, and deployment
- One-page PDF report is prepared
- `git-log.txt` is included
- Render deployment URL is added after live deployment
