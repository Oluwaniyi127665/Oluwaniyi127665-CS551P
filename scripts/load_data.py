import csv
import os
from pathlib import Path

from app import create_app
from app.models import LocalAuthority, School, db


BASE_DIR = Path(__file__).resolve().parents[1]
SCHOOLS_DATA_PATH = BASE_DIR / "data" / "raw" / "educational-establishment.csv"
AUTHORITIES_DATA_PATH = BASE_DIR / "data" / "raw" / "local-authority.csv"


def clean_value(value):
    if value is None:
        return None
    value = value.strip()
    return value or None


def clean_int(value):
    value = clean_value(value)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def load_local_authorities(csv_path):
    authorities_by_code = {}

    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            code = clean_value(row.get("local-authority-district"))
            if not code:
                continue

            authority = LocalAuthority(
                code=code,
                short_code=clean_value(row.get("reference")),
                name=clean_value(row.get("name")) or "Unknown authority",
                region=clean_value(row.get("region")),
                combined_authority_name=clean_value(row.get("combined-authority")),
                local_authority_type=clean_value(row.get("local-authority-type")),
                website=clean_value(row.get("website")),
            )
            db.session.add(authority)
            db.session.flush()
            authorities_by_code[code] = authority

    return authorities_by_code


def load_schools(csv_path, authorities_by_code, max_records=None):
    loaded_schools = 0

    with csv_path.open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            authority_code = clean_value(row.get("local-authority-district"))
            authority = authorities_by_code.get(authority_code)
            if authority is None:
                continue

            school = School(
                urn=clean_value(row.get("reference")) or f"missing-{loaded_schools + 1}",
                establishment_number=clean_value(
                    row.get("educational-establishment-number")
                ),
                name=clean_value(row.get("name")) or "Unknown school",
                school_type=clean_value(row.get("educational-establishment-type")),
                phase=clean_value(row.get("phase")),
                status=clean_value(row.get("educational-establishment-status")),
                capacity=clean_int(row.get("school-capacity")),
                point=clean_value(row.get("point")),
                website_url=clean_value(row.get("website-url")),
                gender=clean_value(row.get("gender")),
                district_code=authority_code,
                authority_id=authority.id,
            )
            db.session.add(school)
            loaded_schools += 1

            if max_records and loaded_schools >= max_records:
                break

    return loaded_schools


def load_data(
    schools_csv_path=SCHOOLS_DATA_PATH,
    authorities_csv_path=AUTHORITIES_DATA_PATH,
    max_records=None,
):
    if not schools_csv_path.exists():
        raise FileNotFoundError(f"Expected schools CSV file at {schools_csv_path}")
    if not authorities_csv_path.exists():
        raise FileNotFoundError(
            f"Expected authorities CSV file at {authorities_csv_path}"
        )

    app = create_app()

    with app.app_context():
        db.session.query(School).delete()
        db.session.query(LocalAuthority).delete()
        db.session.commit()

        authorities_by_code = load_local_authorities(authorities_csv_path)
        loaded_schools = load_schools(
            schools_csv_path,
            authorities_by_code,
            max_records=max_records,
        )

        db.session.commit()

        print(f"Loaded {loaded_schools} schools")
        print(f"Loaded {LocalAuthority.query.count()} local authorities")


if __name__ == "__main__":
    limit_value = os.environ.get("MAX_SCHOOL_RECORDS")
    max_records = int(limit_value) if limit_value else None
    load_data(max_records=max_records)
