# Mithila-Panji

**An open, community-stewarded lineage database for the Maithil Brahmins of Mithila.**

Mithila-Panji is a graph database and a small web application that
digitises the *Panji Prabandh* — the seven-century-old Maithil genealogical
record-keeping tradition instituted under Maharaj Harisimhadeva in 1326 CE —
and makes it searchable, extensible, and useful to ordinary Maithil families.

The goal is simple to state: **every Maithil Brahmin family branch should be
connectable, through documented ancestry, to its *Ādibīja*** — the
originating ancestor of its line. When that is achieved across the
community, the number of distinct surviving family trees should equal the
number of distinct *Ādibījas*, and not more.

This repository hosts the data, the schema, the ingestion code, and a
small viewer application. See
[`docs/MVP_SETUP.md`](docs/MVP_SETUP.md) to stand up your own copy and
[`CONTRIBUTING.md`](CONTRIBUTING.md) for how to help.

---

## Status

This is an early-stage project (Phase 0 — public release). The current data
comes from:

- **Thakur, Gajendra; Jha, Nagendra Kumar; Jha, Panjikar Vidyanand.**
  *Genome Mapping (450 A.D. to 2009 A.D.) — Mithilak Panji Prabandh, Vol.
  I–III.* Shruti Publication, New Delhi, 2009. ISBN 978-81-907729-6-9.

### What's in the graph today

| Layer | Count | Source |
| --- | --- | --- |
| Gotra nodes | 20 | Front-matter index of the 2009 volumes |
| Mool nodes (deduplicated) | ~135 | Front-matter index |
| `IN_GOTRA` edges (mool ↔ gotra) | 165 | Front-matter index |
| Person records (cleaned) | ~6,000 | Panji_1 + Panji_2 of the 2009 volumes |
| Multi-generation chains (3+ gen) | tens, to be precise after run | `build_lineage_exports.py` reports this |
| Founding-history nodes | 4 (Harisimhadeva + 3 first panjikars) | Front-matter narrative |

The 2009 volumes are best understood as **a comprehensive index of
founding ancestors (*Bījī*) by *mool***. They are not yet a complete
generational atlas. That gap is what the project's call for further
manuscripts and contributions is designed to close.

---

## Try the live demo

If a public AuraDB instance is configured, the demo at
**https://&lt;your-github-username&gt;.github.io/mithila-panji/** lets you:

- Search for a Maithil Brahmin ancestor by name (IAST, Devanagari, or
  ad-hoc romanisation like *Jha / Jhaa / Zha*).
- See their mool and the gotra(s) the mool belongs to.
- Walk known parent / sibling / child chains.

The demo is read-only. Contributions go through GitHub issues — see
[`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## How to use this repository

| If you are… | Start with |
| --- | --- |
| A Maithil family wanting to find ancestors | The live demo above; if it isn't running, browse [`data/seed/`](data/seed/) and read the [article](docs/article.md). |
| A scholar who can read Mithilakshara or classical Maithili | [`CONTRIBUTING.md`](CONTRIBUTING.md) → "Scholar contributions". We need transcription help. |
| A Panjikar or family with manuscripts | [`CONTRIBUTING.md`](CONTRIBUTING.md) → "Source contributions". Photographic capture only; originals stay with you. |
| A software engineer | [`docs/SCHEMA.md`](docs/SCHEMA.md) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). Issues are tagged `good first issue` where applicable. |
| Curious about the design rationale | The article in [`docs/article.md`](docs/article.md). |

---

## Repository layout

```
mithila-panji/
├── README.md                       ← you are here
├── LICENSE                         ← MIT (covers the code)
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── .gitignore
├── .github/
│   └── ISSUE_TEMPLATE/
│       ├── contribute-data.md
│       ├── bug-report.md
│       └── feature-request.md
├── data/
│   ├── LICENSE-DATA.md             ← CC-BY-SA 4.0 (covers the data)
│   ├── seed/                       ← the manually-curated reference graph
│   │   ├── panji_seed_gotras_mools.cypher
│   │   ├── panji_seed_gotras_mools.jsonl
│   │   └── panji_founding_history.cypher
│   ├── extracted/                  ← person records from the 2009 volumes
│   │   ├── persons.json            (input to build_lineage_exports.py)
│   │   ├── panji_lineage_persons.cypher
│   │   ├── panji_lineage_persons.jsonl
│   │   ├── panji_lineage.graphml
│   │   ├── panji_trees_summary.csv
│   │   └── panji.ged
│   └── README.md
├── scripts/
│   ├── extract.py                  ← DOCX → persons.json
│   ├── build_lineage_exports.py    ← persons.json → all portable formats
│   ├── load_neo4j.py               ← persons.json → Neo4j (direct loader)
│   └── requirements.txt
└── docs/
    ├── index.html                  ← the GitHub Pages demo viewer
    ├── article.md                  ← the public-facing article
    ├── ARCHITECTURE.md             ← layered design + diagram
    ├── SCHEMA.md                   ← node / edge reference
    ├── MVP_SETUP.md                ← step-by-step bring-up
    └── HISTORICAL_CONTEXT.md       ← Panji history, gotra/mool background
```

---

## License

- **Code** (everything in `scripts/`, `docs/index.html`, etc.):
  [MIT](LICENSE).
- **Data** (everything in `data/`, plus the schema documentation):
  [Creative Commons Attribution-ShareAlike 4.0](data/LICENSE-DATA.md).

Attribution must include both Mithila-Panji and the upstream source —
Thakur, Jha & Jha (2009).

---

## Contact

Maintained by **Rajiv Jha** — jharajiv@hotmai.com.

This project belongs to the Maithil community as much as it belongs to its
maintainers. Contributions, corrections, and questions are all welcome.
