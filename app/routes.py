from flask import Blueprint, abort, render_template, request

from .models import LocalAuthority, School
from .services.queries import (
    get_authorities_with_counts,
    build_school_filters,
    get_authority_summary,
    get_school_filter_options,
    get_homepage_stats,
    get_similar_schools,
)


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    return render_template("home.html", stats=get_homepage_stats())


@main_bp.route("/schools")
def schools_index():
    query = School.query.order_by(School.name.asc())
    filters = build_school_filters(request.args)

    if filters["name"]:
        query = query.filter(School.name.ilike(f"%{filters['name']}%"))
    if filters["authority_id"]:
        query = query.filter(School.authority_id == filters["authority_id"])
    if filters["school_type"]:
        query = query.filter(School.school_type == filters["school_type"])
    if filters["status"]:
        query = query.filter(School.status == filters["status"])

    total_matches = query.count()
    schools = query.limit(100).all()
    authorities = LocalAuthority.query.order_by(LocalAuthority.name.asc()).all()
    filter_options = get_school_filter_options()
    return render_template(
        "schools/index.html",
        schools=schools,
        authorities=authorities,
        active_filters=filters,
        filter_options=filter_options,
        result_count=len(schools),
        total_matches=total_matches,
    )


@main_bp.route("/schools/<int:school_id>")
def school_show(school_id):
    school = School.query.get_or_404(school_id)
    similar_schools = get_similar_schools(school)
    return render_template(
        "schools/show.html",
        school=school,
        similar_schools=similar_schools,
    )


@main_bp.route("/authorities")
def authorities_index():
    include_empty = request.args.get("show", default="active") == "all"
    authorities = get_authorities_with_counts(include_empty=include_empty)
    return render_template(
        "authorities/index.html",
        authorities=authorities,
        include_empty=include_empty,
    )


@main_bp.route("/authorities/<int:authority_id>")
def authority_show(authority_id):
    authority = LocalAuthority.query.get_or_404(authority_id)
    summary = get_authority_summary(authority)
    return render_template(
        "authorities/show.html",
        authority=authority,
        summary=summary,
    )


@main_bp.route("/compare")
def compare_schools():
    first_id = request.args.get("first", type=int)
    second_id = request.args.get("second", type=int)

    if not first_id or not second_id:
        abort(404)

    first_school = School.query.get_or_404(first_id)
    second_school = School.query.get_or_404(second_id)

    return render_template(
        "schools/compare.html",
        first_school=first_school,
        second_school=second_school,
    )
