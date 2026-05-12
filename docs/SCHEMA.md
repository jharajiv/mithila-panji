# Schema reference

This is the graph schema used by Mithila-Panji. The same model is used in
the Neo4j Cypher loaders, the GraphML export, and the JSONL export.

## Nodes

| Label | Required properties | Optional properties |
| --- | --- | --- |
| `Person` | `id` (12-hex), `name_dev`, `name_roman` | `titles`, `source_ref`, `source_file`, `is_seed` (true for founding-history nodes) |
| `Village` | `id` (12-hex), `name_dev`, `name_roman` | — |
| `Mool` | `id` (lexical), `name_dev`, `name_roman` | `aka` (alternate spellings, e.g. *Kaṭāi / Kaṭāī*) |
| `Gotra` | `id` (`g01`–`g20`), `name_dev`, `name_roman`, `seq` | — |
| `Source` | `id`, `name`, `kind` | `year`, `isbn`, `custodian` |
| `Marriage` (planned) | `id` | `date_ce`, `place`, `siddhānta_ref` |
| `Community` (founding history) | `id`, `name_dev`, `name_roman` | — |

### ID conventions

- **Person**: `md5(name_dev + "|" + village_dev)[:12]`. Stable across
  re-extractions so the same person occurring as a child in one record
  and a parent in another merges to the same node.
- **Village**: `md5(name_dev)[:12]`.
- **Mool**: `m_<iast_name>`. Lexical for readability in Cypher.
- **Gotra**: `g01` through `g20` in the canonical order of the source.
- **Source**: `src_<short_slug>`.

## Edges

| Type | Direction | Meaning |
| --- | --- | --- |
| `CHILD_OF` | `Person → Person` | Patrilineal parent-child link, directed child → parent. |
| `SIBLING_OF` | `Person — Person` | Sibling relationship, undirected (stored once per pair). |
| `FROM_VILLAGE` | `Person → Village` | Person's ancestral village as recorded in the source. |
| `OF_MOOL` | `Person → Mool` | Person belongs to this mool (explicit attestation). |
| `OF_MOOL_GUESS` | `Person → Mool` | Inferred from `Village.name_roman` matching a known `Mool.name_roman`. Auto-created at load time. |
| `IN_GOTRA` | `Mool → Gotra` | This mool belongs to that gotra. Some mools have multiple. |
| `OF_GOTRA` | `Person → Gotra` | Person's gotra (explicit attestation). Currently rare in the corpus; usually inferred via `OF_MOOL_GUESS → IN_GOTRA`. |
| `ATTESTED_BY` (planned) | `* → Source` | Any node's provenance pointer. |
| `APPOINTED` (founding history) | `Person → Person` | E.g. Harisimhadeva APPOINTED Gunakar Jha. Carries `for_community`, `year_ce`. |
| `SERVED_AS_PANJIKAR_OF` (founding history) | `Person → Community` | The panjikar's beat. |

## Constraints and indexes

```cypher
CREATE CONSTRAINT person_id  IF NOT EXISTS FOR (p:Person)  REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT village_id IF NOT EXISTS FOR (v:Village) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT mool_id    IF NOT EXISTS FOR (m:Mool)    REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT gotra_id   IF NOT EXISTS FOR (g:Gotra)   REQUIRE g.id IS UNIQUE;

CREATE INDEX person_name_roman IF NOT EXISTS FOR (p:Person)  ON (p.name_roman);
CREATE INDEX person_name_dev   IF NOT EXISTS FOR (p:Person)  ON (p.name_dev);
CREATE INDEX village_name      IF NOT EXISTS FOR (v:Village) ON (v.name_roman);
CREATE INDEX mool_name_roman   IF NOT EXISTS FOR (m:Mool)    ON (m.name_roman);
CREATE INDEX gotra_name_roman  IF NOT EXISTS FOR (g:Gotra)   ON (g.name_roman);
```

## Sample queries

**Search by name (fuzzy contains, case-insensitive):**

```cypher
MATCH (p:Person)
WHERE toLower(p.name_roman) CONTAINS toLower($query)
RETURN p LIMIT 20;
```

**Trace ancestry to root (any person with no recorded parent):**

```cypher
MATCH path = (start:Person {id: $person_id})-[:CHILD_OF*0..15]->(ancestor:Person)
WHERE NOT (ancestor)-[:CHILD_OF]->(:Person)
RETURN [n IN nodes(path) | n.name_roman] AS chain
ORDER BY length(path) DESC
LIMIT 1;
```

**Find cross-gotra mools (mools belonging to >1 gotra):**

```cypher
MATCH (m:Mool)-[:IN_GOTRA]->(g:Gotra)
WITH m, count(g) AS gotras_count
WHERE gotras_count > 1
RETURN m.name_roman, gotras_count
ORDER BY gotras_count DESC;
```

**Coverage map — biggest family trees:**

```cypher
MATCH (root:Person)
WHERE NOT (root)-[:CHILD_OF]->(:Person)
WITH root, count{ (root)<-[:CHILD_OF*1..15]-(:Person) } AS descendants
WHERE descendants > 0
RETURN root.name_roman, root.id, descendants
ORDER BY descendants DESC LIMIT 20;
```

**Marriage compatibility (sapinda check — placeholder, will need Marriage nodes):**

```cypher
// Closest documented common ancestor between two persons
MATCH (a:Person {id: $a_id}), (b:Person {id: $b_id})
MATCH path = shortestPath((a)-[:CHILD_OF*..15]-(b))
RETURN [n IN nodes(path) | n.name_roman] AS chain, length(path) AS gens_apart;
```

## Provenance

Every fact in the graph should ultimately resolve to a `Source` node via
`ATTESTED_BY`. The current seed and 2009-extracted data all point to a
single Source (the Thakur/Jha/Jha 2009 publication) — future ingestion
should create one `Source` node per manuscript / volume / contribution.
