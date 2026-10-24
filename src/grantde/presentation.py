"""Public view models, dates and labels for the static site."""

from datetime import date


LABELS = {
    "bachelor": "Bachelor’s", "master": "Master’s", "doctorate": "Doctorate",
    "state_exam": "State examination", "diploma": "Diploma", "preparatory": "Preparatory study",
    "short_course": "Short course", "exchange": "Exchange", "other": "Other",
    "engineering": "Engineering", "computer_science": "Computer science",
    "mathematics": "Mathematics", "natural_sciences": "Natural sciences", "medicine": "Medicine",
    "health_sciences": "Health sciences", "agriculture": "Agriculture", "environment": "Environment",
    "business_economics": "Business & economics", "law": "Law", "social_sciences": "Social sciences",
    "humanities": "Humanities", "education": "Education", "arts_design": "Arts & design",
    "music": "Music", "architecture": "Architecture", "living_costs": "Living costs",
    "tuition": "Tuition", "research": "Research", "travel": "Travel", "insurance": "Insurance",
    "language_course": "Language course", "study_completion": "Study completion",
    "in_germany": "Already in Germany", "outside_germany": "Outside Germany",
    "open": "Open", "upcoming": "Upcoming", "closed": "Closed", "rolling": "Rolling applications",
    "dates_unconfirmed": "Dates unconfirmed",
}
FREQUENCIES = {"monthly": " / month", "semester": " / semester", "annual": " / year", "one_off": " one-off"}


def label(value: str) -> str:
    return LABELS.get(value, value.replace("_", " "))


def date_label(value: str | None) -> str:
    return date.fromisoformat(value).strftime("%d %b %Y").lstrip("0") if value else "Not confirmed"


def funding_label(funding: dict) -> str:
    minimum, maximum = funding["amount_min"], funding["amount_max"]
    currency = funding["currency"]
    if currency and (minimum is not None or maximum is not None):
        unit = "€" if currency == "EUR" else f"{currency} "
        number = lambda value: f"{value:,.0f}" if value == int(value) else f"{value:,.2f}"
        if minimum is not None and maximum is not None:
            amount = number(minimum) if minimum == maximum else f"{number(minimum)}–{number(maximum)}"
            return f"{unit}{amount}{FREQUENCIES.get(funding['frequency'], '')}"
        if maximum is not None:
            return f"Up to {unit}{number(maximum)}{FREQUENCIES.get(funding['frequency'], '')}"
        return f"From {unit}{number(minimum)}{FREQUENCIES.get(funding['frequency'], '')}"
    return "Amount varies" if funding["frequency"] == "variable" else "See funding details"


def round_status(round_: dict, today: date) -> str:
    now = today.isoformat()
    if round_["deadline"] and round_["deadline"] < now:
        return "closed"
    if round_["opens_on"] and round_["opens_on"] > now:
        return "upcoming"
    recorded = round_["availability"]
    if recorded in {"open", "upcoming"} and round_["as_of"] < now:
        if recorded == "open" and round_["deadline"] and round_["deadline"] >= now:
            return "open"
        return "dates_unconfirmed"
    return recorded


def round_view(round_: dict, today: date) -> dict:
    return {
        **{key: round_[key] for key in (
            "id", "opens_on", "deadline", "deadline_time", "timezone", "as_of", "applicable_country_codes"
        )},
        "recorded_status": round_["availability"],
        "status": round_status(round_, today),
    }


def primary_round(rounds: list[dict]) -> dict:
    priority = {"open": 0, "upcoming": 1, "rolling": 2, "dates_unconfirmed": 3, "closed": 4}
    return min(rounds, key=lambda r: (
        priority[r["status"]],
        r["deadline"] or "9999-12-31",
        r["id"],
    ))


def public_record(record: dict, today: date) -> dict:
    scope = record["study_scope"]
    requirements = record["applicant_requirements"]
    rounds = [round_view(round_, today) for round_ in record["application_rounds"]]
    return {
        "id": record["id"], "slug": record["slug"], "title": record["title"],
        "is_draft": record["publication"]["status"] == "draft",
        "provider": record["provider"]["name"], "summary": record["summary"],
        "url": f"/scholarships/{record['slug']}/",
        "funding": funding_label(record["funding"]), "purposes": record["funding"]["covered_costs"],
        "degrees": {key: scope["degree_levels"][key] for key in ("status", "values")},
        "subjects": {key: scope["subject_areas"][key] for key in ("status", "values")},
        "institutions": {key: scope["institutions"][key] for key in ("status", "values")},
        "residence": {key: requirements["residence"][key] for key in ("status", "values")},
        "has_exceptions": bool(requirements["exceptions"]), "rounds": rounds,
        "primary_round": primary_round(rounds),
        "last_checked": record["provenance"]["last_checked"],
    }
