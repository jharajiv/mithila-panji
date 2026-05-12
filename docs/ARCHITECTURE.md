# Architecture

This document specifies the layered design of Mithila-Panji. For a
non-technical overview, see [`article.md`](article.md) §6. For the
end-to-end bring-up of the demo, see [`MVP_SETUP.md`](MVP_SETUP.md). For
the graph schema, see [`SCHEMA.md`](SCHEMA.md).

## Design principles

Five principles govern every choice below.

- **Provenance over polish.** Every fact is tied to a source. The graph
  never silently picks a winner among disagreeing manuscripts.
- **Open by default.** Schema, ingestion code, and the deceased-ancestor
  graph are open. Living-individual data is private by default.
- **Read-heavy, append-rarely.** Family-tree lookups dominate; new
  records arrive in batches via human curation, not high-frequency writes.
- **Federated authority.** No single "winner" database. Different
  Panjikar lines, scholarly editions, and family submissions are all
  sources; their assertions coexist with confidence weights.
- **Boring infrastructure.** Pick widely-supported tools that a volunteer
  maintainer can pick up in a weekend.

## The layered architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│ 1. Sources (physical & digitised)                                    │
│    Panji manuscripts · 2009 Thakur volumes · family vanśāvalīs ·     │
│    siddhānta papers · user submissions                               │
│    Read-only inputs. Originals stay with their custodians.           │
└──────────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────────┐
│ 2. Ingestion & transcription pipeline                                │
│    Image capture → OCR / manual transcription → structured parsing   │
│    (extract.py) → provenance-tagged records                          │
│    Object storage (S3 / B2) for images · Python parsers · review     │
│    queue                                                             │
└──────────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────┬───────────────────────────────────┐
│ 3a. Canonical graph store        │ 3b. Metadata & identity store     │
│     Neo4j (AuraDB Free or self-  │     PostgreSQL holding user       │
│     hosted) holding              │     accounts, contributor history,│
│     Person, Village, Mool, Gotra,│     moderation queues, audit log, │
│     Source nodes;                │     private-scope extensions,     │
│     CHILD_OF, SIBLING_OF,        │     access tokens, manuscript     │
│     FROM_VILLAGE, OF_GOTRA,      │     catalog.                      │
│     ATTESTED_BY edges            │                                   │
└──────────────────────────────────┴───────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────────┐
│ 4. API & search layer                                                │
│    GraphQL / REST · transliteration-aware fuzzy search (OpenSearch)  │
│    · ancestor-graft endpoints · provenance queries · rate-limited    │
│    public read                                                       │
└──────────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────┬───────────────────────────────────┐
│ 5a. Web / mobile family app      │ 5b. Panjikar & scholar console    │
│     Next.js + React · search,    │     Structured intake forms ·     │
│     graft, extend, view tree,    │     manuscript folio linker ·     │
│     export own GEDCOM / PDF.     │     conflict adjudication ·       │
│     Maithili / Hindi / English   │     bulk import. Low bandwidth    │
│     UI.                          │     assumed.                      │
└──────────────────────────────────┴───────────────────────────────────┘
```

## Layer-by-layer responsibilities

| Layer | Responsibility | Tech recommendation |
| --- | --- | --- |
| 1. Sources | Original Panji manuscripts, the 2009 Thakur / Jha / Jha volumes, family vanśāvalīs, user submissions. | Photographic capture; immutable originals stay with custodians. |
| 2. Ingestion | Convert source material into structured records with full provenance. | Python parser (`scripts/extract.py`), Tesseract / Google Vision OCR for handwritten material, manual transcription queue, S3-compatible object storage for folio images. |
| 3a. Canonical graph | The shared, queryable lineage graph. | **Neo4j** (community self-hosted, or **AuraDB Free** for the early years). Schema in [`SCHEMA.md`](SCHEMA.md). |
| 3b. Metadata store | User accounts, moderation state, private-scope family extensions, audit log, manuscript catalog. | **PostgreSQL**. |
| 4. API + search | External access surface; transliteration-aware fuzzy search; ancestor-graft; provenance queries. | FastAPI (Python); OpenSearch (or Postgres pg_trgm to start) for fuzzy search. |
| 5a. Family app | Search, graft, view, extend, export. | Next.js + React. |
| 5b. Curator console | Structured intake for Panjikars and scholars. | Same Next.js codebase, gated by role. |

## Data flow

A new lineage record passes through five stages, each persisting and
verifiable:

1. **Capture.** A Panjikar or volunteer photographs a folio, or a family
   submits a *vanśāvalī*. The image lands in object storage with a
   generated `source_id`.
2. **Transcribe.** OCR produces a draft, or a Maithili-literate volunteer
   transcribes by hand. Output is structured (the same record format
   that `extract.py` consumes).
3. **Parse.** The parser turns structured text into Person / Marriage /
   Mool / Village records, each carrying an `ATTESTED_BY` pointer to the
   `source_id`.
4. **Review.** A two-reviewer pass in the curator console: at least one
   Maithili-literate scholar and one technical maintainer confirm before
   records enter the canonical graph.
5. **Publish.** Records become visible in the public API. Conflicts with
   existing assertions trigger an open *conflict* record visible to all
   readers — never silently overwritten.

## User-facing flows

### Search & graft

A user provides what they know — typically four to six ancestor names,
the family *gotra*, the family *mool*, and an ancestral village. The API
runs a fuzzy match across Devanagari, IAST, and common ad-hoc
romanisations (*Jha / Jhaa / Zha*, *Mishra / Misra*) and returns candidate
matches with confidence scores. If the user confirms a match, the API
attaches the user's known recent ancestors as new `CHILD_OF` edges
anchored on the matched canonical Person — extending the user's personal
tree, often by many generations, in a single action.

### Extend

The user can add ancestors, marriages, or descendants the graph does not
yet contain. Additions enter a moderation queue with the user recorded
as a `Source`. Once cross-attested by another submission or a scholar
review, they become part of the shared corpus.

### Private scope

Living individuals and descendants of women who married outside the
tracked community are stored only in the user's private scope by default.
The canonical graph contains references to private nodes but cannot read
them.

## Operational concerns

### Privacy

Three tiers:
- **Public** — deceased ancestors, names already in printed Panji volumes.
- **Family-scope** — living individuals, recent marriages — visible to
  the contributing family by default.
- **Private** — extensions beyond a node where the canonical graph
  terminates (e.g. a daughter married outside the community).

### Moderation & conflict

Every change is auditable. Conflicting attestations are stored side by
side, each tied to its `Source`; the application surfaces the
disagreement rather than choosing for the user. A small editorial
committee — Panjikar representatives plus at least one Maithili scholar —
adjudicates structural conflicts (e.g. two manuscripts giving different
parents for the same person).

### Scale & cost

Order-of-magnitude back-of-the-envelope: the historical Maithil Brahmin
corpus is plausibly 200,000–500,000 distinct persons across seven
centuries. With cross-references, this implies under five million nodes
and under twenty million edges — comfortably within free-tier Neo4j
AuraDB during build-up, and a few hundred dollars a month at full scale.
Image storage is the larger long-run cost (~10 KB per folio × ~100,000
folios ≈ 1 TB), which fits S3-compatible object storage at well under
fifty dollars a month.

### Long-term custody

The corpus must outlive its founders. The architecture deliberately uses
only formats that have decade-plus stability: Cypher, GraphML, JSONL,
GEDCOM, plain images. A second pillar is institutional: the project
should migrate, within its first few years, into a non-profit trust
co-chaired by Panjikar and scholarly representatives, with the dataset
mirrored in at least two academic archives (Zenodo for a citable DOI;
one university library for a dark archive).

## The minimum-viable first release

For a first public release, the project does not need every layer above.
A defensible MVP looks like this:

- Layer 3a: Neo4j AuraDB Free populated with the gotra/mool seed graph
  plus the cleaned persons from the 2009 Thakur volumes (the artifacts
  already in `data/`).
- Layer 5a: a single-page web UI offering search, view-tree, and a
  contact form for source contributors. This is `docs/index.html`,
  published on GitHub Pages.
- No writes from the public yet; all extensions go through GitHub issues
  while moderation is being set up.

The full setup is in [`MVP_SETUP.md`](MVP_SETUP.md) — eight steps,
about 60–90 minutes total, no coding required from the operator.

## Cross-graph connects

The moment the seed graph and the cleaned persons are loaded together,
several queries that are difficult or impossible in conventional
genealogy software become trivial:

- Every gotra that shares a particular mool (e.g. *Brahmapurā* spans
  five gotras — Śāṇḍilya, Vatsa, Alāmbukākṣa, Garga, Gautama).
- For any given Person, the documented chain of descent and the
  cross-gotra mools that share the same ancestral village.
- Coverage gaps: which gotras and which mools are underrepresented in
  the present corpus, and therefore where to direct future
  source-collection effort.
- Marriage-time *siddhānta* assistance: given two candidate spouses, the
  closest documented common ancestor and the generation distance —
  directly automating what the Panjikars perform on paper.

See [`SCHEMA.md`](SCHEMA.md) for the Cypher snippets that run each of
these queries.
