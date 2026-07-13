# Mithila-Panji — Deployment Guide

The Mithila-Panji viewer is a static GitHub Pages application — no database
subscription required. It uses CSV data from the `data/` folder, converts
it to JSON on every data change, and serves the lineage explorer as a
single-page application.

**Quick summary:** push your CSVs to GitHub, the build workflow auto-generates
the JSON files, and the viewer is live at `https://<your-username>.github.io/mithila-panji/`.

## Prerequisites

- A GitHub account (free).
- A computer with Git installed (to push changes).
- **No database setup, no backend, no server cost.**

---

## Step 1 — Upload your repository to GitHub  (5 minutes)

1. Create a new GitHub repository named `mithila-panji` (or your preferred name).
2. Push the contents of this folder to `main` branch.
   - If you're new to GitHub, use [GitHub Desktop](https://desktop.github.com/) or the web UI's drag-and-drop.

Once pushed, GitHub Actions will automatically run the build workflow and
generate `docs/data/persons.json` and `docs/data/edges.json` from your CSVs.

---

## Step 2 — Enable GitHub Pages  (2 minutes)

1. Go to your repository **Settings → Pages**.
2. Under **Source**, select **Deploy from a branch**.
3. Choose **Branch: main** and **Folder: /docs**.
4. Click **Save**.

GitHub will assign you a URL: `https://<your-username>.github.io/mithila-panji/`

---

## Step 3 — Test the live viewer  (2 minutes)

Visit `https://<your-username>.github.io/mithila-panji/`.

You should see:
- A search box that works with partial names (try "vidyapati", "narahari", "mishra").
- Search results show gotra, mool, and village information.
- Click "View lineage" on any result to see the full family tree in both
  directions (ancestors and descendants) rendered as an interactive graph.
- The Cytoscape graph displays relationships with color-coded nodes:
  - **Dark red** = the selected person
  - **Orange** = ancestors
  - **Blue** = descendants
  - **Green** = siblings

---

## Updating the data

When you add new person records or relationships to `data/*.csv`:

1. Push the changes to GitHub.
2. The build workflow runs automatically and regenerates `docs/data/persons.json`
   and `docs/data/edges.json`.
3. The live viewer updates within ~30 seconds.

No manual steps, no database migrations, no credentials to manage.

---

## Total cost

| Item | Cost |
| --- | --- |
| GitHub Pages hosting | ₹0 / month |
| Domain name (optional) | ~₹500 / year |
| **Total recurring** | **₹0 / month** |

**No database subscription required.** The entire application runs as static files
on GitHub Pages.
