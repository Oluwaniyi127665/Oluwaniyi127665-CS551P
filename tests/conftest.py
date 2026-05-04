import pytest

from app import create_app
from app.models import LocalAuthority, School, db
from config import TestConfig


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.drop_all()
        db.create_all()

        authority = LocalAuthority(
            code="E09000001",
            short_code="AUTH-001",
            name="Sample Authority",
            region="Sample Region",
            combined_authority_name="Sample Combined Authority",
            local_authority_type="Unitary Authority",
            website="https://example.org/authority",
        )
        db.session.add(authority)
        db.session.flush()

        school_one = School(
            urn="100001",
            establishment_number="001",
            name="Sample Primary School",
            school_type="11",
            phase=None,
            status="1",
            capacity=450,
            point="POINT (-2.10 57.15)",
            website_url="https://example.org/primary",
            gender=None,
            district_code="E09000001",
            authority_id=authority.id,
        )
        school_two = School(
            urn="100002",
            establishment_number="002",
            name="Sample Secondary School",
            school_type="28",
            phase=None,
            status="1",
            capacity=900,
            point="POINT (-2.11 57.16)",
            website_url="https://example.org/secondary",
            gender=None,
            district_code="E09000001",
            authority_id=authority.id,
        )
        db.session.add_all([school_one, school_two])
        db.session.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()
