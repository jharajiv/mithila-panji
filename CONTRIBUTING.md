# Contributing to Mithila-Panji

Thank you for your interest in the project. Mithila-Panji exists only
because contributors — families, scholars, Panjikars, and engineers — bring
to it what they hold. There are four distinct ways to contribute. Pick the
one that fits.

---

## 1. Source contributions (Panji manuscripts, family records)

**If you are:** a Panjikar with a register; a Maithil family with a
*vanśāvalī*; a custodian of *siddhānta* papers, wedding cards, or any
written record that names ancestors.

**How:**

1. Open a new issue on GitHub using the **"Contribute data"** template
   (or email rajiv.jha@myvyoma.io if GitHub is not convenient for you).
2. Describe what you have: rough page count, time period if known, family
   names if you can share them.
3. We will arrange photographic capture — at your location, on your terms.
   Originals **never** leave your possession. Only photographs and
   transcriptions enter the corpus.
4. Once the material is digitised and transcribed, it is added to the
   graph and credited to you as a Source.

There is no contribution too small. A single legible photograph of a
single folio, accurately captioned, is a permanent addition.

---

## 2. Scholar contributions (transcription, verification, editorial notes)

**If you are:** fluent in Mithilakshara, classical Maithili, Sanskrit, or
Maithili Brahmin genealogical convention; able to read, verify, or correct
transcribed records.

**How:**

1. Open an issue describing your background and which kind of work
   interests you (transcription of new captures, verification of existing
   transcriptions, editorial notes on disputed lineages, etc.).
2. We will pair you with material at your skill and bandwidth level.
3. Verified work is committed to `data/` with you credited as a reviewer
   in the commit message.

Academic affiliation is welcome but **not required**.

---

## 3. Code contributions (engineering, design)

**If you are:** a software engineer, designer, or product person who wants
to improve the system itself.

**How:**

1. Read [`docs/SCHEMA.md`](docs/SCHEMA.md) and
   [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
2. Look at the **open issues** — those tagged `good first issue`,
   `help wanted`, or `enhancement` are the obvious starting points.
3. Fork, branch, commit, open a pull request. We follow standard GitHub
   flow.
4. Run any tests we've shipped before opening the PR (`python -m pytest`
   in `scripts/` once we have a test suite — early days yet).

**Coding norms** (light):

- Python: PEP 8, type hints where reasonable, docstrings on public
  functions. No frameworks beyond what's already in `scripts/requirements.txt`.
- JavaScript / HTML in `docs/index.html`: vanilla JS preferred. No build
  step. Keep the demo viewer dependency-free so anyone can read it.
- Commit messages: imperative mood, scope-prefixed where applicable
  (`docs: …`, `extract: …`, `viewer: …`).

---

## 4. Governance, fundraising, outreach

**If you are:** willing to help establish a small editorial / trust
committee, identify grant opportunities, or organise community outreach in
Mithila or the diaspora.

**How:** open an issue tagged `governance` with what you have in mind, or
email rajiv.jha@myvyoma.io. This stream of work is at least as important
as the technical work and is currently the most under-resourced.

---

## Conduct

Be kind. Disagree on facts, never on people. The Maithil community is
diverse and dispersed; we will encounter genuinely conflicting
attestations and genuine differences of interpretation. Surface these
respectfully. Anyone making the project unwelcoming to women, to people of
any caste or community, to LGBTQ+ contributors, or to the religiously
unaffiliated will be removed.

The project's code of conduct is in
[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

---

## Recognition

All contributors are credited:

- Source contributors: as `Source` nodes in the graph and in
  `data/CONTRIBUTORS.md`.
- Scholar contributors: in commit history and in
  `data/CONTRIBUTORS.md`.
- Code contributors: in GitHub's standard contributors list, plus in
  `CONTRIBUTORS.md`.

If you would prefer to remain anonymous, say so when you open the issue;
we will record the contribution without your name.
