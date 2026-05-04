from collections import Counter

from sqlalchemy import func

from ..lookups import region_label, school_status_label, school_type_label
from ..models import LocalAuthority, School


def get_homepage_stats():
    school_count = School.query.count()
    authority_count = LocalAuthority.query.count()
    top_types = Counter(
        school_type
        for (school_type,) in School.query.with_entities(School.school_type).all()
        if school_type
    ).most_common(5)
    top_statuses = Counter(
        status for (status,) in School.query.with_entities(School.status).all() if status
    ).most_common(4)
    largest_authorities = Counter(
        authority_id
        for (authority_id,) in School.query.with_entities(School.authority_id).all()
        if authority_id
    ).most_common(5)
    authority_lookup = {
        authority.id: authority.name
        for authority in LocalAuthority.query.filter(
            LocalAuthority.id.in_([authority_id for authority_id, _ in largest_authorities])
        ).all()
    }

    return {
        "school_count": school_count,
        "authority_count": authority_count,
        "top_types": [(school_type_label(code), count) for code, count in top_types],
        "top_statuses": [
            (school_status_label(code), count) for code, count in top_statuses
        ],
        "largest_authorities": [
            (authority_lookup.get(authority_id, f"Authority {authority_id}"), count)
            for authority_id, count in largest_authorities
        ],
    }


def build_school_filters(args):
    return {
        "authority_id": args.get("authority_id", type=int),
        "name": args.get("name", default="").strip(),
        "school_type": args.get("school_type", default="").strip(),
        "status": args.get("status", default="").strip(),
    }


def get_school_filter_options():
    school_types = sorted(
        {
            school_type
            for (school_type,) in School.query.with_entities(School.school_type).all()
            if school_type
        }
    )
    statuses = sorted(
        {status for (status,) in School.query.with_entities(School.status).all() if status}
    )
    return {
        "school_types": [(code, school_type_label(code)) for code in school_types],
        "statuses": [(code, school_status_label(code)) for code in statuses],
    }


def get_authorities_with_counts(include_empty=False):
    authorities = (
        LocalAuthority.query.outerjoin(School)
        .with_entities(
            LocalAuthority.id,
            LocalAuthority.name,
            LocalAuthority.code,
            LocalAuthority.region,
            func.count(School.id).label("school_count"),
        )
        .group_by(
            LocalAuthority.id,
            LocalAuthority.name,
            LocalAuthority.code,
            LocalAuthority.region,
        )
        .order_by(LocalAuthority.name.asc())
        .all()
    )
    authority_rows = [
        {
            "id": authority.id,
            "name": authority.name,
            "code": authority.code,
            "region_label": region_label(authority.region),
            "school_count": authority.school_count,
        }
        for authority in authorities
    ]
    if not include_empty:
        authority_rows = [
            authority for authority in authority_rows if authority["school_count"] > 0
        ]
    authority_rows.sort(
        key=lambda authority: (-authority["school_count"], authority["name"])
    )
    return authority_rows


def get_similar_schools(school):
    return (
        School.query.filter(
            School.authority_id == school.authority_id,
            School.id != school.id,
        )
        .order_by(School.name.asc())
        .limit(5)
        .all()
    )


def get_authority_summary(authority):
    type_counter = Counter(
        school.school_type for school in authority.schools if school.school_type
    )
    status_counter = Counter(school.status for school in authority.schools if school.status)
    return {
        "school_count": len(authority.schools),
        "type_counts": [
            (school_type_label(code), count)
            for code, count in type_counter.most_common()
        ],
        "status_counts": [
            (school_status_label(code), count)
            for code, count in status_counter.most_common()
        ],
    }
