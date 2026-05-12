# `data/` — what is in this directory

All files here are licensed under **CC-BY-SA 4.0** — see
[`LICENSE-DATA.md`](LICENSE-DATA.md). Code in the rest of the repository
remains MIT-licensed.

## Layout

```
data/
├── LICENSE-DATA.md
├── seed/                          ← curated reference graph
│   ├── panji_seed_gotras_mools.cypher
│   ├── panji_seed_gotras_mools.jsonl
│   └── panji_founding_history.cypher
└── extracted/                     ← person records from the 2009 volumes
    ├── persons.json               ← raw output of scripts/extract.py
    ├── panji_lineage_persons.cypher
    ├── panji_lineage_persons.jsonl
    ├── panji_lineage.graphml
    ├── panji_trees_summary.csv
    └── panji.ged
```

## What's in `seed/`

The Maithil Brahmin reference graph hand-built from the front-matter
"Gotra aa Mool" index of the 2009 publications:

- **20 Gotra nodes** — the canonical Maithil Brahmin gotras.
- **~135 Mool nodes** — deduplicated; some mools recur across multiple
  gotras (e.g. *Brahmapurā* in 5, *Jallakī* in 3, *Varevā* in 3).
- **165 IN_GOTRA edges** — these are the **cross-gotra connectors** that
  make queries like "what gotras share this mool?" trivial.
- **4 founding-history nodes** — Harisimhadeva (1326 CE) and the three
  first panjikars: Gunakar Jha (Maithil Brahmins), Shankaradatta (Karna
  Kayasthas), Vijayadatta (Kshatriyas).

This data is **stable** — it does not change unless the source publication
is corrected. Load it first.

## What's in `extracted/`

Person records parsed from the body of the 2009 volumes by
`scripts/extract.py`, then cleaned and re-exported in multiple formats by
`scripts/build_lineage_exports.py`.

The `panji_trees_summary.csv` is the project's **coverage map**: one row
per connected family-tree component, with the root ancestor's name, the
inferred village/mool, the person count, and the maximum generation
depth. Use it to identify which trees in the corpus are deepest and which
mools are still under-represented.

## Load order (for Neo4j)

```bash
# 1. Reference graph — gotras, mools, founding history
cypher-shell -f data/seed/panji_seed_gotras_mools.cypher
cypher-shell -f data/seed/panji_founding_history.cypher

# 2. Extracted person records from the 2009 volumes
cypher-shell -f data/extracted/panji_lineage_persons.cypher
```

After step 2 the file's trailing `MERGE (p)-[:OF_MOOL_GUESS]->(m)`
statement automatically cross-links every Person to its mool where the
village name matches a known mool from the seed.

See [`../docs/MVP_SETUP.md`](../docs/MVP_SETUP.md) for the full bring-up
sequence including AuraDB Free setup.
