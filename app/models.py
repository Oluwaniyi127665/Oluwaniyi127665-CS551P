from flask_sqlalchemy import SQLAlchemy

from .lookups import region_label, school_status_label, school_type_label


db = SQLAlchemy()


class LocalAuthority(db.Model):
    __tablename__ = "local_authorities"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(32), unique=True, nullable=False, index=True)
    short_code = db.Column(db.String(32), unique=True, nullable=True, index=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    region = db.Column(db.String(255), nullable=True)
    combined_authority_name = db.Column(db.String(255), nullable=True)
    local_authority_type = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(255), nullable=True)

    schools = db.relationship(
        "School",
        back_populates="authority",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def region_label(self):
        return region_label(self.region)

    def __repr__(self):
        return f"<LocalAuthority {self.code} {self.name}>"


class School(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True)
    urn = db.Column(db.String(32), unique=True, nullable=False, index=True)
    establishment_number = db.Column(db.String(32), nullable=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    school_type = db.Column(db.String(255), nullable=True, index=True)
    phase = db.Column(db.String(255), nullable=True, index=True)
    status = db.Column(db.String(255), nullable=True, index=True)
    capacity = db.Column(db.Integer, nullable=True)
    postcode = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    point = db.Column(db.String(64), nullable=True)
    website_url = db.Column(db.String(255), nullable=True)
    gender = db.Column(db.String(64), nullable=True)
    district_code = db.Column(db.String(32), nullable=True, index=True)
    authority_id = db.Column(
        db.Integer,
        db.ForeignKey("local_authorities.id"),
        nullable=False,
        index=True,
    )

    authority = db.relationship("LocalAuthority", back_populates="schools")

    @property
    def status_label(self):
        return school_status_label(self.status)

    @property
    def school_type_label(self):
        return school_type_label(self.school_type)

    def __repr__(self):
        return f"<School {self.urn} {self.name}>"
