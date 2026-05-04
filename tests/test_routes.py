from app.models import LocalAuthority, School


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"UK Schools Explorer" in response.data


def test_schools_page(client):
    response = client.get("/schools")
    assert response.status_code == 200
    assert b"Sample Primary School" in response.data
    assert b"Open" in response.data


def test_schools_name_filter(client):
    response = client.get("/schools?name=Primary")
    assert response.status_code == 200
    assert b"Sample Primary School" in response.data


def test_school_detail_page(client, app):
    with app.app_context():
        school = School.query.filter_by(urn="100001").first()

    response = client.get(f"/schools/{school.id}")
    assert response.status_code == 200
    assert b"Sample Primary School" in response.data


def test_missing_school_returns_404(client):
    response = client.get("/schools/999999")
    assert response.status_code == 404


def test_authorities_page(client):
    response = client.get("/authorities")
    assert response.status_code == 200
    assert b"Sample Authority" in response.data
    assert b"Sample Region" in response.data
    assert b"2" in response.data
    assert b"linked school" in response.data


def test_authorities_page_with_all_authorities(client):
    response = client.get("/authorities?show=all")
    assert response.status_code == 200
    assert b"Show only authorities with linked schools" in response.data


def test_compare_page(client, app):
    with app.app_context():
        schools = School.query.order_by(School.id.asc()).all()

    response = client.get(f"/compare?first={schools[0].id}&second={schools[1].id}")
    assert response.status_code == 200
    assert b"Compare Schools" in response.data
    assert b"District code" in response.data
