from app.models import LocalAuthority, School


def test_authority_school_relationship(app):
    with app.app_context():
        authority = LocalAuthority.query.filter_by(short_code="AUTH-001").first()
        assert authority is not None
        assert len(authority.schools) == 2
        assert all(isinstance(school, School) for school in authority.schools)
