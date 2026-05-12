# Mithila-Panji — MVP Setup Guide

A 60-to-90-minute, click-through bring-up of the live demo. Assumes you
have:

- A computer with internet access (Windows / Mac / Linux all fine).
- A GitHub account (free).
- A Python 3.10+ installation. On Windows, download from
  https://python.org and tick "Add Python to PATH" during install.
- **No coding skill is required.** All commands are copy-paste.

The end result is a publicly accessible URL —
`https://<your-github-username>.github.io/mithila-panji/` — that lets
anyone search the lineage graph.

---

## Step 1 — Sign up for Neo4j AuraDB Free  (10 minutes)

Neo4j AuraDB is the cloud version of the Neo4j graph database. The Free
tier holds up to ~200,000 nodes and ~400,000 edges — more than enough for
the current corpus.

1. Open **https://console.neo4j.io/** in your browser.
2. Sign in (or create an account; Google login is fine).
3. Click **"New instance"** → choose **"AuraDB Free"** → **"Create Free
   instance"**.
4. Give it a name: `mithila-panji`.
5. **VERY IMPORTANT** — you will be shown a username (`neo4j`) and a
   **generated password**. Copy both into a safe place and tick "I have
   stored the password". You cannot recover it later; you can only reset.
6. Note the **Connection URI**: it looks like
   `neo4j+s://abc123de.databases.neo4j.io`. Copy it too.
7. Wait ~3 minutes for the instance to come up (it shows a green dot when
   ready).

You now have a cloud Neo4j database. Click **"Open"** to launch the
**Neo4j Browser** in a new tab — this is the web UI you will use to load
data and run queries.

---

## Step 2 — Load the seed graph  (5 minutes)

In the Neo4j Browser:

1. Open the file `data/seed/panji_seed_gotras_mools.cypher` from this
   repository in any text editor (Notepad, VS Code, etc.).
2. Select all the text (Ctrl-A) and copy (Ctrl-C).
3. In Neo4j Browser, click the **":"** input bar at the top, paste the
   Cypher (Ctrl-V), and click the blue ▶ button on the right.
4. Wait a few seconds; you should see "Added 155 nodes, set 465
   properties, created 165 relationships" or similar.
5. Repeat for `data/seed/panji_founding_history.cypher`.

Quick sanity check — run this single query in the browser:

```cypher
MATCH (g:Gotra)<-[:IN_GOTRA]-(m:Mool)
RETURN g.name_roman, count(m) AS mool_count
ORDER BY mool_count DESC;
```

You should see the 18 gotras that have mools, with *śāṇḍilya* topping the
list at 43.

---

## Step 3 — Generate the person-records export  (15 minutes, one-time)

This step processes the 2009 volumes' extracted `persons.json` (already
done by `scripts/extract.py`) into the load-ready Cypher / GraphML /
JSONL / CSV / GEDCOM exports.

Open a terminal (PowerShell on Windows, Terminal on Mac/Linux):

```powershell
# Navigate into the scripts folder
cd "C:\path\to\mithila-panji\scripts"

# Install the two Python libraries the script needs
pip install indic_transliteration python-docx

# Run the cleaner / exporter
python build_lineage_exports.py
```

You will see output like:

```
Loaded 6,796 raw person records.
After noise filtering: ~4,000 persons.
Surviving relationships: ~2,500
Writing Cypher / JSONL / GraphML / CSV / GEDCOM...
Connected components ≥2 persons: ~1,200
Largest tree: <root name> of <village> — N persons, depth D
```

The exact numbers depend on the upstream data; what matters is that
**five files** appear in `data/extracted/`:

- `panji_lineage_persons.cypher`
- `panji_lineage_persons.jsonl`
- `panji_lineage.graphml`
- `panji_trees_summary.csv`
- `panji.ged`

Open `panji_trees_summary.csv` in Excel or LibreOffice — this is your
coverage map. Each row is one family tree.

---

## Step 4 — Load the persons into AuraDB  (5 minutes)

Same procedure as Step 2:

1. Open `data/extracted/panji_lineage_persons.cypher` in a text editor.
2. **If the file is very large (over 5 MB)**, split it in half at any
   `MERGE (` line — Neo4j Browser has a paste limit. Loading 2,000 lines at a
   time works comfortably.
3. Copy → paste → run in Neo4j Browser.
4. At the end, run the final `MERGE (p)-[:OF_MOOL_GUESS]->(m)` block — it
   cross-links every Person to a known Mool where the village name
   matches.

Sanity check:

```cypher
// Count loaded persons
MATCH (p:Person) RETURN count(p);
// Show one family tree, depth 3+
MATCH path = (root:Person)-[:CHILD_OF*1..6]->(ancestor:Person)
WHERE NOT (root)<-[:CHILD_OF]-(:Person)
RETURN root.name_roman, length(path) AS gens
ORDER BY gens DESC LIMIT 5;
```

---

## Step 5 — Create a read-only user for the public demo  (5 minutes)

The static viewer needs Neo4j credentials. **Never** ship the master
password publicly. Create a read-only user instead:

In Neo4j Browser, run:

```cypher
CREATE USER reader IF NOT EXISTS
  SET PASSWORD 'a-long-random-string-you-choose'
  SET PASSWORD CHANGE NOT REQUIRED;
GRANT ROLE reader TO reader;
```

The `reader` role is built into Neo4j and grants only `MATCH` /
`RETURN` — no `CREATE`, no `MERGE`, no `DELETE`. Even if the credentials
leak (which they will, since they go into a public HTML page), nobody can
modify or delete data.

> **Note:** AuraDB Free may have restrictions on role management. If the
> command above fails, an acceptable fallback for the demo is to use the
> default `neo4j` user — but **change its password to a long random
> string** afterwards so the leaked credential cannot be used for high-
> privilege actions.

---

## Step 6 — Configure the demo viewer  (5 minutes)

Open `docs/index.html` in a text editor. Near the top of the file you
will see:

```js
const NEO4J_QUERY_URL = "https://<your-instance>.databases.neo4j.io/db/neo4j/query/v2";
const NEO4J_USER      = "reader";
const NEO4J_PASSWORD  = "a-long-random-string-you-choose";
```

Replace these three values with what you noted down in Step 1 (the
**HTTPS** URL — convert `neo4j+s://` to `https://` and append
`/db/neo4j/query/v2`) and the credentials you created in Step 5.

Save the file.

---

## Step 7 — Publish via GitHub Pages  (5 minutes)

1. Push the entire `mithila-panji/` folder to a new GitHub repository
   named `mithila-panji`. (You can do this through the web UI: create
   the repo, then drag-drop the folder; or use GitHub Desktop.)
2. In your GitHub repo, click **Settings → Pages** (left sidebar).
3. Under **Source**, choose **Deploy from a branch**.
4. Under **Branch**, choose `main` and the `/docs` folder. Click **Save**.
5. Wait ~2 minutes. A green banner appears with your URL:
   `https://<your-username>.github.io/mithila-panji/`.

Visit the URL. You should see a search box. Type *vidyāpati* or *narahari*
and hit Enter. Matches from the corpus appear with their mool and gotra.

**You have a live, public, free, zero-server demo.** Share the URL.

---

## Step 8 — Verify everything works  (5 minutes)

Things to check on the live demo:

- [ ] Search returns matches for `vidyāpati`, `harinātha`, `narahari`.
- [ ] Clicking a match shows their mool and gotra.
- [ ] Clicking "show children" expands the tree downward.
- [ ] The page header links to the GitHub repo and the article.

If anything fails, open an issue in the repo with the browser console
output (F12 → Console tab in Chrome / Firefox).

---

## What to do next

- **Promote it.** Post the demo URL + article on LinkedIn, Maithili
  Facebook groups, Twitter/X, and any Mithila WhatsApp groups you are
  part of.
- **Watch the issues queue.** Source-contribution issues are the most
  important. Even one new manuscript scan is a meaningful corpus
  expansion.
- **Recurring rebuild.** When new data arrives, repeat Steps 3 and 4 to
  re-export and re-load. The seed graph (Step 2) only needs to be loaded
  once.

---

## Total cost

| Item | Cost |
| --- | --- |
| Neo4j AuraDB Free | ₹0 / month |
| GitHub Pages hosting | ₹0 / month |
| Domain name (if you add one) | optional, ~₹500 / year |
| **Total recurring** | **₹0 / month** |

The Free tier of AuraDB pauses if there are no queries for 72 hours; one
visit wakes it up again, with a ~30-second cold-start. For the early
months this is acceptable. If you outgrow the Free tier, AuraDB
Professional is ~$65 / month for the smallest size.
