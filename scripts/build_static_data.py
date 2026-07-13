"""Generate the static JSON files served by docs/index.html on GitHub Pages.

Reads the CSVs in data/ and writes:
  - docs/data/persons.json   full person records, enriched with mool/gotra
                              inferred from the person's recorded village.
  - docs/data/edges.json     the FULL child_of and sibling_of relationship
                              lists (not a capped sample) so the client can
                              build a real ancestors/descendants/siblings
                              lineage view for any person in the corpus.

No external dependencies; run with any Python 3.9+.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DATA_DIR = ROOT / "docs" / "data"


def read_csv_rows(path):
    if not path.exists():
        print(f"Optional file missing: {path}")
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def norm(text):
    return (text or "").strip().lower()


def main():
    DOCS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    person_rows = read_csv_rows(DATA_DIR / "persons.csv")
    if not person_rows:
        raise SystemExit("Missing or empty data/persons.csv")

    child_of_rows = read_csv_rows(DATA_DIR / "child_of_edges.csv")
    sibling_of_rows = read_csv_rows(DATA_DIR / "sibling_of_edges.csv")
    from_village_rows = read_csv_rows(DATA_DIR / "from_village_edges.csv")
    village_rows = read_csv_rows(DATA_DIR / "villages.csv")
    mool_rows = read_csv_rows(DATA_DIR / "mools.csv")
    gotra_rows = read_csv_rows(DATA_DIR / "gotras.csv")
    in_gotra_rows = read_csv_rows(DATA_DIR / "in_gotra_edges.csv")

    villages_by_id = {r["id"]: r for r in village_rows if r.get("id")}
    village_by_person_id = {
        r["person_id"]: r["village_id"]
        for r in from_village_rows
        if r.get("person_id") and r.get("village_id")
    }

    gotras_by_id = {r["id"]: r for r in gotra_rows if r.get("id")}
    gotras_by_mool_id = {}
    for r in in_gotra_rows:
        mool_id, gotra_id = r.get("mool_id"), r.get("gotra_id")
        if not mool_id or not gotra_id or gotra_id not in gotras_by_id:
            continue
        gotras_by_mool_id.setdefault(mool_id, []).append(
            gotras_by_id[gotra_id]["name_roman"]
        )

    # Map every known village-name spelling (roman or devanagari, including
    # aka alternates) to its mool, so a person's recorded village can be
    # resolved to a mool/gotra the same way the old OF_MOOL_GUESS edge did.
    mool_name_lookup = {}
    mools_by_id = {r["id"]: r for r in mool_rows if r.get("id")}
    for r in mool_rows:
        names = [r.get("name_roman"), r.get("name_dev")]
        for alt in (r.get("aka") or "").split("/"):
            names.append(alt)
        for name in names:
            key = norm(name)
            if key:
                mool_name_lookup[key] = r["id"]

    def resolve_mool_gotra(village_roman, village_dev):
        mool_id = mool_name_lookup.get(norm(village_roman)) or mool_name_lookup.get(
            norm(village_dev)
        )
        if not mool_id:
            return "", ""
        mool = mools_by_id.get(mool_id, {})
        gotras = gotras_by_mool_id.get(mool_id, [])
        return mool.get("name_roman", ""), ", ".join(gotras)

    persons = []
    person_ids = set()

    for row in person_rows:
        person_id = (row.get("id") or row.get("person_id") or "").strip()
        if not person_id:
            continue

        name_dev = (row.get("name_dev") or row.get("name") or "").strip()
        name_roman = (row.get("name_roman") or row.get("roman_name") or "").strip()
        village_dev = (row.get("village_dev") or "").strip()
        village_roman = (row.get("village_roman") or row.get("village") or "").strip()

        if not village_roman and not village_dev:
            village_id = village_by_person_id.get(person_id)
            village = villages_by_id.get(village_id) if village_id else None
            if village:
                village_dev = village.get("name_dev", "")
                village_roman = village.get("name_roman", "")

        mool, gotra = resolve_mool_gotra(village_roman, village_dev)

        persons.append(
            {
                "id": person_id,
                "name_dev": name_dev,
                "name_roman": name_roman,
                "label": name_roman or name_dev or person_id,
                "village_dev": village_dev,
                "village_roman": village_roman,
                "gotra": gotra,
                "mool": mool,
                "titles": (row.get("titles") or "").strip(),
                "source_ref": (row.get("source_ref") or "").strip(),
                "source_file": (row.get("source_file") or "").strip(),
                "type": "Person",
            }
        )
        person_ids.add(person_id)

    persons.sort(key=lambda p: (p.get("label") or "").lower())

    (DOCS_DATA_DIR / "persons.json").write_text(
        json.dumps(persons, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    child_of = []
    for row in child_of_rows:
        child_id, parent_id = row.get("child_id", "").strip(), row.get(
            "parent_id", ""
        ).strip()
        if child_id in person_ids and parent_id in person_ids:
            child_of.append([child_id, parent_id])

    sibling_of = []
    for row in sibling_of_rows:
        a_id, b_id = row.get("person_a_id", "").strip(), row.get(
            "person_b_id", ""
        ).strip()
        if a_id in person_ids and b_id in person_ids:
            sibling_of.append([a_id, b_id])

    edges = {
        "generated_from": [
            "data/persons.csv",
            "data/child_of_edges.csv",
            "data/sibling_of_edges.csv",
        ],
        "child_of": child_of,
        "sibling_of": sibling_of,
    }

    (DOCS_DATA_DIR / "edges.json").write_text(
        json.dumps(edges, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    old_sample = DOCS_DATA_DIR / "graph_sample.json"
    if old_sample.exists():
        old_sample.unlink()

    print(f"Generated persons.json with {len(persons)} persons")
    print(
        f"Generated edges.json with {len(child_of)} child_of and "
        f"{len(sibling_of)} sibling_of edges"
    )


if __name__ == "__main__":
    main()
