"""Create an offline editorial queue; this does not verify provider pages."""

import argparse
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit

from grantde.catalogue import load_catalogue, write_json
from grantde.presentation import round_status
from grantde.validate import require_valid


def normalise(text):
    text = unicodedata.normalize("NFKD", text).casefold()
    text = "".join(character for character in text if not unicodedata.combining(character))
    return " ".join(re.findall(r"[^\W_]+", text))


def programme_key(url):
    if not url:
        return None
    parsed = urlsplit(url)
    query = dict(parse_qsl(parsed.query))
    if parsed.hostname and (parsed.hostname == "daad.de" or parsed.hostname.endswith(".daad.de")):
        programme = query.get("detail") or next(iter(re.findall(r"stipa(\d+)", parsed.path)), None)
        if programme:
            return f"daad:{programme}"
    query = [(key, value) for key, value in parse_qsl(parsed.query) if not key.startswith("utm_")]
    return f"{parsed.netloc.lower()}{parsed.path.rstrip('/')}?{urlencode(sorted(query))}"


def audit(data_dir, as_of):
    catalogue = load_catalogue(data_dir)
    require_valid(catalogue)
    queue, titles, urls = [], defaultdict(list), defaultdict(list)
    for path, record in catalogue.records:
        flags = []
        if record["provenance"]["review_method"] == "extracted_draft":
            flags.append("source_review_pending")
        if record["publication"]["review_notes"]:
            flags.append("editorial_notes_present")
        criteria = {
            "degree": record["study_scope"]["degree_levels"],
            "subject": record["study_scope"]["subject_areas"],
            "institution": record["study_scope"]["institutions"],
            "nationality": record["applicant_requirements"]["nationality"],
            "residence": record["applicant_requirements"]["residence"],
        }
        flags.extend(f"{name}_unknown" for name, value in criteria.items() if value["status"] == "unknown")
        if record["application_process"]["required_documents_status"] == "unknown":
            flags.append("documents_unknown")
        funding = record["funding"]
        if funding["amount_min"] is None and funding["amount_max"] is None:
            flags.append("numeric_funding_not_summarised")
        rounds = record["application_rounds"]
        statuses = [round_status(round_, as_of) for round_ in rounds]
        if all(status == "dates_unconfirmed" for status in statuses):
            flags.append("current_dates_unconfirmed")
        if statuses and all(status == "closed" for status in statuses):
            flags.append("past_rounds_only")
        soon = [round_["deadline"] for round_ in rounds if round_["deadline"]
                and as_of <= date.fromisoformat(round_["deadline"]) <= as_of + timedelta(days=30)]
        if soon:
            flags.append("deadline_within_30_days")
        url = record["application_process"]["official_programme_url"]
        if not url:
            flags.append("official_programme_link_missing")
        priority = 1 if soon or not url else 2 if flags else 3
        queue.append({"id": record["id"], "title": record["title"], "priority": priority,
                      "flags": flags, "near_deadlines": sorted(soon), "official_url": url,
                      "publication_status": record["publication"]["status"],
                      "last_checked": record["provenance"]["last_checked"],
                      "last_reviewed": record["provenance"]["last_reviewed"],
                      "review_method": record["provenance"]["review_method"],
                      "review_notes": record["publication"]["review_notes"]})
        titles[(normalise(record["title"]), normalise(record["provider"]["name"]))].append(record["id"])
        key = programme_key(url)
        if key:
            urls[key].append(record["id"])
    counts = Counter(flag for item in queue for flag in item["flags"])
    return {"as_of": as_of.isoformat(), "scope": "Offline structural and editorial triage only; no live link verification.",
            "records": len(queue), "flag_counts": dict(sorted(counts.items())),
            "exact_title_provider_groups": [ids for ids in titles.values() if len(ids) > 1],
            "shared_programme_urls": [{"key": key, "ids": ids} for key, ids in urls.items() if len(ids) > 1],
            "queue": sorted(queue, key=lambda item: (item["priority"], item["near_deadlines"] or ["9999"], -len(item["flags"]), item["id"]))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--as-of", type=date.fromisoformat, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.data_dir, args.as_of)
    write_json(args.output, result)
    print(json.dumps({key: value for key, value in result.items() if key != "queue"}, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
