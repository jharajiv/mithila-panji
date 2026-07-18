# Toward a Graph-Based Lineage Database for Maithil Brahmins
### Digitizing the Panji Tradition to Trace Every Family Back to Its Ādibīja

**Rajiv Jha** · *Independent researcher* · rajiv.jha@myvyoma.io
*Project: [Mithila-Panji](https://github.com/jharajiv/mithila-panji) — public release, May 2026*

---

**Abstract.** The Panji Prabandh of Mithila is among the oldest continuous lineage-recording traditions in South Asia. Maintained for nearly seven centuries by hereditary scribes known as *Panjikars*, it has documented the genealogies of Maithil Brahmins and Karna Kayasthas across the Mithila region of present-day Bihar and the Tarai of Nepal. Today, most of this corpus survives in fragile, locally-held manuscripts, increasingly cut off from the families it once served. This paper proposes — and accompanies, in the form of an open-source repository and a working demo — the construction of a community-stewarded **graph database** that ingests existing Panji records, beginning with the 2009 publications of Sri Gajendra Thakur, Nagendra Kumar Jha, and Panjikar Vidyanand Jha, and exposes them through a user-facing application that lets any Maithil family search by ancestor name, *gotra*, and *mool*, graft their known lineage onto the existing graph, and trace their line back, ideally, to its *Ādibīja* — the originating ancestor. The article sets out the cultural rationale, sketches the data model and the layered architecture, reports the corpus state at first public release, and issues an explicit call for collaborators: source contributors, technologists, and Maithili-literate scholars.

**Keywords:** *Panji Prabandh, Mithila, Maithil Brahmins, genealogy, graph database, cultural preservation, Ādibīja, gotra, mool.*

---

## 1. Introduction

Every Maithil Brahmin household carries, in some form, the memory of a few generations: a grandfather's name remembered in death rites, a great-grandfather invoked at the wedding fire, a village from which the family is said to have come. Beyond that horizon, memory usually fails. Yet for nearly seven hundred years, a parallel record has run alongside ordinary family memory — written, audited, and updated at every marriage — in the form of the Panji Prabandh of Mithila.

The Panji system is unusual in world terms. It is not only that lineages were recorded; it is that they were recorded *systematically*, *by hereditary specialists*, *for an entire endogamous community*, and updated at the precise life-event — marriage — where lineage information mattered most. The two communities historically subject to this registration are the Maithil Brahmins and the Karna (Maithil) Kayasthas; a parallel system once covered the Gandhavariya Rajputs as well. In strict practice, no marriage between two Maithil Brahmin families was permitted to proceed without the *siddhānta* — the formal genealogical clearance issued by the Panjikars to confirm that the union did not violate the *sapinda* prohibition on consanguinity within seven generations.

The result, over centuries, is a vast distributed archive: tens of thousands of manuscript volumes, written in a mixture of Maithili, Sanskrit, and the Mithilakshara script, held in private custody by a handful of scribal families across the districts of Madhubani, Darbhanga, Saharsa, Samastipur, Sitamarhi, and adjacent regions of Nepal. The Panji Prabandh is, in effect, a **seven-century, community-scale genealogical census** — and one of the very few non-state genealogical institutions of comparable depth anywhere in the world.

This paper argues that the Panji corpus, in its present state, is one generation away from irreversible loss; that the right technical response is not a digital archive in the conventional sense but a graph database; and that the right social response is an open, community-stewarded project that invites Maithil families themselves to extend, verify, and inhabit the record. It sets out a preliminary design, names what exists today, and names what is needed. A working open-source repository — *Mithila-Panji* — accompanies this article, with the seed data, the schema, the ingestion code, and a small viewer application already in place.

A companion document, [`HISTORICAL_CONTEXT.md`](HISTORICAL_CONTEXT.md), provides a plain-language history of the Panji tradition for readers new to the subject; the present article assumes that history as background.

## 2. The Panji Tradition: A Brief Historical Overview

The Panji Prabandh is conventionally traced to the reign of King Harisimhadeva of the Karnata dynasty of Mithila, who is said to have ordered the formal codification of genealogies in or around **1326 CE** (Śaka 1248). Whatever the precise origin, by the fourteenth century a corps of specialist scribes — the Panjikars — had been institutionalised, drawn from particular Maithil Brahmin families and supported by patronage from the Mithila Maharajas of Darbhanga in later centuries. Three founding panjikars are named in the tradition: **Guṇākara Jhā** of Mahindrapur Paṇḍuā (Kāśyapa gotra) for the Maithil Brahmins, **Śaṅkaradatta** for the Karna Kayasthas, and **Vijayadatta** for the Kshatriyas.

Each Panjikar maintained a *panji* (literally, register) for the families whose *mool* (ancestral village-identity) he was responsible for. A Maithil Brahmin family is identified by the conjunction of:

- **Gotra** — the patrilineal Vedic clan (*Śāṇḍilya, Kāśyapa, Vātsya, Bhāradvāja*, etc.). Twenty are canonically recognised.
- **Mool** — the specific Maithil sub-lineage village from which the family is said to originate, e.g. *Khauwāl, Sodarpur, Karmahā, Pālī, Sakraurh*. About 167 are recorded in the source corpus.
- **Pravara**, *Adhikārī* status, and *śrotriya* sub-grading — finer distinctions used in marriage qualification.

At each marriage, the Panjikars of both sides would produce a written *siddhānta* tracing both bride and groom back, typically seven generations, to demonstrate that the proposed union was outside the prohibited degrees. The *siddhānta* was archived; the new union became a fresh edge in the record, and any children would themselves enter the register at their own marriages, decades later.

Over time, an enormous structure accumulated: not merely lists of names, but a connected web of marriages, descents, and cross-references across the entire Maithil Brahmin and Karna Kayastha population. In modern computer-science vocabulary, the Panjikars were maintaining — by hand, in ink, in Mithilakshara — a distributed, eventually-consistent, write-once-per-life-event property graph.

## 3. The Present Crisis: Fragmentation, Decay, and Loss

The Panji system has weakened, but not collapsed. Several pressures converge:

- **Generational attrition among Panjikars.** The hereditary scribal lines, traditionally passed father to son, are no longer reliably reproduced. Few younger members of these families have the literacy in Mithilakshara, Maithili, and Sanskrit, or the patience for what is effectively unpaid traditional service, that the role demands.
- **Physical fragility of the manuscripts.** The Panjis are paper or palm-leaf bundles held in private homes across rural Mithila. Damp, fire, neglect, and partition of inheritance among heirs have already destroyed substantial portions of the corpus that existed in living memory.
- **Script and language access.** Even where manuscripts survive, the number of people who can fluently read older Mithilakshara is small and declining. The corpus is therefore not just at physical risk; it is increasingly unreadable to its own community.
- **Disruption of marriage-time consultation.** Modern Maithil families, particularly in diaspora and urban contexts, no longer routinely seek the *siddhānta* before marriage. With each generation that does not consult the Panjikar, a fresh marriage edge fails to enter the record, and the graph silently goes out of date.

Against this backdrop, the publication efforts of **Sri Gajendra Thakur, Sri Nagendra Kumar Jha, and Panjikar Sri Vidyanand Jha** in 2009 — *Genome Mapping (450 A.D. to 2009 A.D.) — Mithilak Panji Prabandh,* Volumes I–III, Shruti Publication, ISBN 978-81-907729-6-9 — represent the single most important modern intervention to preserve this corpus. They demonstrate that disciplined transcription is possible, that it produces usable lineage data, and that there is a public appetite for the result. Their work is the natural seed corpus for any digital project; this paper takes it as a starting point.

What remains untouched, however, is the much larger body of manuscripts still in private custody, and the connective, queryable layer that would let any Maithil household locate itself within the corpus and extend it.

## 4. A Graph Database Approach

### 4.1 Why a graph, not a spreadsheet or a relational table

Kinship is intrinsically graph-structured. A person has two parents, possibly multiple marriages, an arbitrary number of children, and may appear in the genealogical chains of countless descendants. Forcing this into rows and columns produces brittle, lossy representations; the natural form is a network of nodes and edges. Graph databases (Neo4j, Memgraph, ArangoDB, or an RDF triple store) make the natural form first-class: kinship questions become path queries.

More importantly, graph storage allows what genealogists call *collateral* queries — "who is my closest documented common ancestor with this person?", "how are these two *mools* connected?", "which families share the Panjikar attestation of this manuscript?" — to be expressed in a handful of lines. None of these are convenient in tabular form.

### 4.2 A preliminary data model

The full schema is documented in [`SCHEMA.md`](SCHEMA.md); the core is sketched here.

**Node types.** *Person, Marriage, Mool, Gotra, Village, Place, Source* — plus *Ādibīja* as a distinguished Person, marked where the originating ancestor of a line has been documented.

**Edge types.** *PARENT_OF / CHILD_OF* (the patrilineal backbone), *SPOUSE_IN* (Person → Marriage), *BELONGS_TO_MOOL*, *BELONGS_TO_GOTRA*, *ATTESTED_BY* (any node → Source — the provenance backbone), *DERIVES_FROM* (Person → Ādibīja, materialised when the chain is complete).

### 4.3 Boundary conditions

Two boundary cases deserve explicit treatment, because they are normatively charged and easy to get wrong:

- **Exogamous marriage of women.** In the traditional Panji frame, a woman who marries outside the Maithil Brahmin community is recorded up to her marriage but her descendants are not tracked further within the canonical corpus. The graph database honours this only as a *default*: her node terminates in the tracked corpus, but a user building a private family tree may extend the line beyond her using the same application. Those extensions live in the user's personal scope and do not enter the shared canonical graph unless and until community policy revises the convention.
- **Conflicting attestations.** Manuscripts disagree. Two Panjikars in different villages may give different fathers or different *mools* for the same person. The graph never silently resolves such conflicts: both claims are stored, each with its own Source, and the application surfaces the disagreement to the user rather than picking a winner.

### 4.4 Provenance and trust

Every assertion in the graph is tied to a Source node. A casual user-submitted family declaration, a printed entry from the 2009 Thakur / Jha / Jha volumes, and a photographed manuscript folio are all Sources, but they carry different trust weights, made visible in the interface. The aim is not to hide uncertainty; it is to expose it in a form that scholars and families can both reason about.

## 5. The Companion Application

The graph database is only useful if ordinary Maithil families can interact with it. The proposed application has three core flows:

- **Search.** A user enters what they know — typically the names of three or four recent ancestors, the family *gotra* and *mool*, an ancestral village. The application performs fuzzy search across transliterations and orthographic variants and returns candidate matches in the graph.
- **Graft.** Where a confident match exists, the user can attach their known recent ancestors onto an existing chain in the graph, immediately extending their personal tree backwards — sometimes by many generations — and surfacing the canonical *Ādibīja* of their line.
- **Extend.** The user can add information the graph does not yet have: living family members, recent marriages, names recovered from family memory. These contributions enter a moderation queue and, once cross-attested, become part of the shared corpus, with the contributor recorded as a Source.

A secondary mode of the application supports the Panjikars themselves: a structured intake tool that lets a scribe — with or without manuscript scanning — enter records in the same schema, so that ongoing traditional work and the digital corpus stay aligned rather than diverging.

Privacy is treated seriously. Living individuals' details are scoped: visible to the contributing family by default, exposed in aggregate to the wider corpus only with consent. Deceased ancestors are public, since their names already circulate in death rites and existing Panji volumes.

## 6. Architecture

The architecture is deliberately conventional, so that no part of the project depends on any one engineer or any one funder. Five layers carry the work — sources, ingestion, canonical graph + metadata store, API, applications — with the technology stack chosen for breadth of support rather than novelty: Neo4j for the graph store, PostgreSQL for user accounts and moderation queues, Python (FastAPI) for the API, Next.js for the family-facing application, and S3-compatible object storage for manuscript images. A minimum viable release — the canonical graph populated with the seed corpus and a read-only search-and-view UI — is achievable in roughly eight to twelve weeks of part-time work, and the present repository already provides the seed graph, the ingestion scripts, and a working static-page viewer that talks to a Neo4j AuraDB Free instance.

The full architecture document, including the layered diagram, per-layer responsibilities, data flow, privacy tiers, scale estimates, and long-term-custody recommendations, is at [`ARCHITECTURE.md`](ARCHITECTURE.md). The setup guide for bringing up the demo locally, end-to-end and without writing any new code, is at [`MVP_SETUP.md`](MVP_SETUP.md).

## 7. Current corpus state — what the project ships at first release

This article accompanies the first public release of *Mithila-Panji*. The graph at release time contains:

- **20 Gotra nodes** — the canonical Maithil Brahmin gotras.
- **~135 Mool nodes** — deduplicated; the most-shared mools (*Brahmapurā* across 5 gotras; *Jallakī* and *Varevā* across 3) account for the bulk of the cross-gotra connectivity.
- **165 *IN_GOTRA* edges** — the mool–gotra membership graph that makes cross-gotra queries possible.
- **4 founding-history nodes** — Maharaj Harisimhadeva and the three first panjikars he appointed in 1326 CE.
- **Approximately 6,000 cleaned Person nodes**, parsed from the 2009 Thakur / Jha / Jha volumes (4,074 records from Volume I + 2,728 from Volume II, deduplicated and noise-filtered).
- Of these, roughly half carry at least one relationship edge; the remainder are recorded primarily as *bījī* — founding ancestors of their *mool*, with no further descent listed in the source. The 2009 volumes are best understood as **a comprehensive index of founding ancestors per mool** rather than as a complete generational atlas; the deep-tree population of the graph is therefore deliberately treated as the work to come, not the work already done.

The connected-component structure of the cleaned graph yields a handful of multi-generation chains of meaningful depth. The familiar lineage of the poet *Vidyāpati* — *viśvanātha → bhavānīnātha → keśava → vidyāpati* — appears among them, as do several Karnata-era ancestral chains. A complete per-tree summary, with root names, mools, sizes, and depths, is in `data/extracted/panji_trees_summary.csv` and is regenerated whenever the corpus changes.

These numbers should be read both as evidence that the model works and as evidence that the work has barely begun. The next thousand manuscript folios captured and transcribed will, on present trajectory, roughly double the depth and triple the connectivity of the graph.

## 8. Sources Known and Sources Sought

The initial seed of the database is the 2009 publication. Beyond it, the project actively seeks:

- Privately held Panji manuscripts of any Panjikar family of Mithila, in any condition, for photographic digitisation. Originals stay with the holders; only images and transcriptions enter the corpus.
- Earlier published Panji material — the partial publications of the twentieth century, dispersed across Maithili periodicals and small presses, that have never been collected in one place.
- Family *vanśāvalīs* — the hand-written household genealogies kept by individual Maithil families, which often capture branches not formally registered with a Panjikar.
- Diaspora records — wedding cards, *siddhāntas*, and printed family histories produced in the second half of the twentieth century, which document the modern boundary of the corpus.

No contribution is too small. A single photograph of a single folio, accurately captioned, is already a permanent addition. The repository's [`CONTRIBUTING.md`](../CONTRIBUTING.md) describes how to offer material — through a GitHub issue or by email — without ever parting with the original.

## 9. Long-Term Vision: As Many Trees as Ādibījas

The long-term ambition of this project is simple to state and serious to attempt: **every Maithil Brahmin family branch should be connected, through documented ancestry, to its Ādibīja** — the originating ancestor of its line in the Mithila record. When that is achieved across the community, the number of distinct surviving family trees should equal the number of distinct Ādibījas, and not more.

This is a multi-decade goal and will not be reached by any single contributor. It is, however, a coherent goal: the Panji tradition itself is structured around precisely this idea, that families are not isolated atoms but branches of a finite, namable set of ancestral lines. The database simply makes that structure computable.

Once the Maithil Brahmin corpus is meaningfully populated, the same schema and tooling extend naturally to the **Karna Kayasthas of Mithila**, whose registration is governed by a parallel Panjikar system. Further out, the platform is open enough that other lineage-recording traditions of South Asia — the Pandas of Haridwar, the Bhats of Rajasthan, parallel genealogical castes in Bengal and Gujarat — can adopt the same schema if they wish. The graph is not exclusive; it is simply rooted, for now, in Mithila.

## 10. A Call for Collaboration

This is not a project that one person can carry, and it is not appropriate that one person should. The Panji corpus belongs to the Maithil community; the database should belong to the community as well. Contributors are sought in four registers, described in detail in [`CONTRIBUTING.md`](../CONTRIBUTING.md):

- **Source contributors** — families and Panjikars willing to allow photographic capture of material they hold.
- **Scholars** — readers fluent in Mithilakshara, classical Maithili, and Sanskrit, who can transcribe and verify.
- **Technologists** — engineers experienced with graph databases, transliteration-aware search, and front-end work suited to a non-technical audience.
- **Governance** — anyone willing to serve on a small founding committee that will eventually move the corpus into a non-profit trust.

## 11. Closing

The Panji Prabandh of Mithila is a quiet, almost invisible achievement of the Maithil community: seven centuries of disciplined record-keeping, sustained by hereditary scribes, recording the connections between families one marriage at a time. It is not yet lost. It is, however, well into the period of its life in which decisions taken now — to digitise, or not; to structure, or not; to invite the community in, or not — will determine whether the next seven centuries inherit the record or merely the memory of it.

The proposal of this paper is that the appropriate response is technical, communal, and unhurried in equal measure. A graph database, openly stewarded, ingesting the work of the Panjikars who have already begun the modern preservation effort and inviting the families themselves to extend it, is one form that response can take. The repository accompanying this article — at https://github.com/jharajiv/mithila-panji — is the first iteration of that response.

Readers willing to contribute material, time, or expertise are invited to write to the author at *rajiv.jha@myvyoma.io* or to open a GitHub issue in the repository.

## Acknowledgments

The author is grateful, in advance, to Sri Gajendra Thakur, Sri Nagendra Kumar Jha, and Panjikar Sri Vidyanand Jha for the 2009 publications that make any project of this kind imaginable, and to the Maithili scholarly community whose continuing work on the Panji tradition forms the intellectual ground on which this proposal stands. Errors of fact, framing, or emphasis in this release remain the author's own; corrections, particularly from descendants of Panjikar families with first-hand knowledge, are warmly invited.

## Selected References and Further Reading

- Thakur, Gajendra; Jha, Nagendra Kumar; Jha, Panjikar Vidyanand (eds.), 2009. *Genome Mapping (450 A.D. to 2009 A.D.) — Mithilak Panji Prabandh, Vol. I–III.* Shruti Publication, New Delhi. ISBN 978-81-907729-6-9.
- Mishra, Jayakanta. *A History of Maithili Literature.* Sahitya Akademi.
- Choudhary, Radhakrishna. *A Survey of Maithili Literature* and *Mithila in the Age of Vidyapati.* Historical context for the Karnata-era origin of Panji codification.
- Kumārila Bhaṭṭa. *Tantra-Vārtika*, on the institution of *samūha-lekhya* (community lineage records). 7th c. CE.
- Robinson, I., and Webber, J. *Graph Databases.* O'Reilly. Technical reference for the proposed storage model.

A working bibliography, with items marked for verification, is maintained in [`HISTORICAL_CONTEXT.md`](HISTORICAL_CONTEXT.md).
