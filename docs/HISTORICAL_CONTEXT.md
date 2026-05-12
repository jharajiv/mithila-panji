# Historical context

*This document is intended as the project's plain-language explainer of
the Panji tradition: where it came from, how it worked, and why it
matters. It complements the formal article in `article.md` (which is
academic in register) by being approachable for readers new to Mithila.*

**Status: placeholder.** This draft contains the structure and the facts
the project has already gathered. The owner of this repository plans to
expand it with additional historical detail; sections marked **[FILL IN]**
are open invitations.

---

## 1. Mithila and its Brahmins — a quick orientation

Mithila is the cultural region of north Bihar (chiefly the districts of
Madhubani, Darbhanga, Saharsa, Samastipur, Sitamarhi, Madhepura,
Supaul, Begusarai) and the contiguous Tarai of Nepal. It takes its
name from King Mithi, son of Nimi, whose dynasty — the Videhas — ruled
from the city of Mithila and to whom King Janaka (foster father of Sita)
also belonged. The region thus carries a continuous self-identification
running back into the Vedic period.

The Brahmin communities of Mithila are conventionally divided into the
**Maithil Brahmins** (the focus of this project), the **Karna Kayasthas**
(traditionally treated alongside Brahmins for genealogical purposes in
the Panji system), and a smaller number of **Kshatriya** lineages
(notably the Gandhavariya Rajputs) who in the early Panji period were
also covered. The Panji system has weakened or lapsed for the latter two
communities; for Maithil Brahmins it survives in fragmentary but real
form to the present.

**[FILL IN — more on the geographic and political setting of Mithila in
the medieval period; the Karnata dynasty, the Sena interludes, the
Oinwar dynasty, and the eventual Mughal-period status.]**

---

## 2. Before Panji — how Maithils tracked themselves

Long before any formal institution, Maithil families kept their own
genealogical memory orally and in private writings. The **Tantra-Vārtika**
of Kumārila Bhaṭṭa (~7th century CE) records that *"great families
preserve their lineage with special effort … kings and Brahmins
introduced lineage-records (samūha-lekhya) precisely so that the line of
fathers and grandfathers would not be forgotten."*

Marriage-time consultation of these private records was the norm: bride
and groom each presented their *yāvato paricaya* — "all I know of my
ancestry" — to demonstrate that the proposed union did not violate the
*sapinda* prohibition on consanguinity within seven patrilineal
generations and five matrilineal generations.

By the thirteenth century this individual practice was visibly
weakening. The source records the case of **Pandit Harinath
Upadhyaya**, the eminent author of *Smṛti-sāra*, who in a moment of
inadequate genealogical care contracted a marriage with his own
paternal-cousin's grand-daughter — a *sapinda* violation. The episode
is cited as a precipitating cause for what came next.

---

## 3. The founding of the Panji system — 1326 CE

In the Śaka year 1248, corresponding to 1326 CE, **Maharaj Harisimhadeva**
of the Karnata dynasty of Mithila convened a sabha of the leading
pandits of his realm. His proposal: lineage-keeping should no longer be
the private duty of each family but a public office. Specific learned
individuals would be appointed, by royal authority, to maintain
registers of every family's lineage and to issue, at the time of every
marriage, a written *siddhānta* certifying that the proposed union did
not violate the sapinda rule.

Three founding panjikars were appointed:

- **Pandit Guṇākara Jhā**, of the mool *Mahindrapur Paṇḍuā*, gotra
  *Kāśyapa* — for the Maithil Brahmins.
- **Pandit Śaṅkaradatta** — for the Karna Kayasthas.
- **Pandit Vijayadatta** — for the Kshatriyas (the Gandhavariya
  Rajputs).

The registers they maintained were called *panji* (literally: register);
those whose names entered the registers were called *panjībaddha* — "bound
into the register." Marriages of those whose lineage could not be
verified or who declined to register were treated as *aśāstrīya* —
contrary to scripture — and the offspring were not formally received
into the patrilineal record.

**[FILL IN — the Sanskrit invocation verses (śloka 1–4 at record 080 of
the source) describe the founding poetically; this section could expand
into a more literary retelling.]**

---

## 4. The architecture of the Panji register

Each Maithil Brahmin family is identified — uniquely, in the Panji
system — by three coordinates:

- **Gotra**: the patrilineal Vedic clan. Twenty are recognised:
  *Śāṇḍilya, Vatsa, Kāśyapa, Sāvarṇa, Parāśara, Bhāradvāja, Kātyāyana,
  Alāmbukākṣa, Garga, Kauśika, Kṛṣṇātreya, Maudgalya, Gautama,
  Vaśiṣṭha, Kauṇḍilya, Jātukarṇa, Taṇḍi, Viṣṇuvṛddhi, Upamanyu,
  Kapila.*
- **Mool**: the specific Maithil sub-lineage village from which the
  family is said to originate — *Khauwāl, Sodarpur, Karmahā, Pālī,
  Brahmapurā,* and ~160 others. A mool is not always exclusive to one
  gotra; *Brahmapurā*, for example, appears under Śāṇḍilya, Vatsa,
  Alāmbukākṣa, Garga, and Gautama.
- **Pravara / Adhikārī status / shrotriya tier** — finer distinctions
  used in marriage qualification. The Maithil Brahmin community is
  internally graded into Śrotriya (8 sub-grades), Yogya, and Pañjībaddha,
  with parallel grading among the Karna Kayasthas.

Every entry in a panji is structured as:

> *[village/mool]* सँ *[titles]* *[name]* सुत *[child name]* ए सुत *[grandchild]* …
> (page-reference)

This compact format — village marker `सँ`, relationship markers
`सुत/सुता/सोदर`, page reference — is what the project's `extract.py` is
designed to parse.

---

## 5. The seven-century drift

For most of the period from Harisimhadeva's foundation to the late
nineteenth century, the system functioned. Panjikar families inherited
their charge from father to son; royal patronage from the Mithila
Maharajas of Darbhanga (the post-Karnata dynasty) sustained the
institution; every marriage in the covered communities produced a fresh
*siddhānta* that was archived and that itself became a new edge in the
record.

Several long-running pressures weakened the institution from within:

- **Generational attrition among Panjikars.** Few descendants of the
  scribal families have today the literacy in Mithilakshara, classical
  Maithili, and Sanskrit that the role requires.
- **Physical decay.** Panji manuscripts are paper or palm-leaf bundles
  held in private custody. Damp, fire, partition of inheritance among
  heirs, and ordinary neglect have already destroyed substantial
  portions.
- **Script and language access.** Even where manuscripts survive, the
  number of fluent readers of older Mithilakshara is now small.
- **Marriage-time consultation falling away.** Urban and diaspora
  Maithil families, particularly post-1947, increasingly conduct
  marriages without obtaining a *siddhānta*. The corresponding new
  marriage-edge therefore never enters the register, and the record
  silently goes out of date.

The single most important modern intervention came in **2009**, when
**Gajendra Thakur** in collaboration with **Nagendra Kumar Jha** and
**Panjikar Vidyanand Jha** published the three-volume *Genome Mapping*
(Shruti Publication, ISBN 978-81-907729-6-9) — a printed transcription of
a substantial portion of the Maithil Brahmin Panji material. This
project takes their published transcription as its initial seed corpus
and aims to make it queryable, extendable, and complementary to
continued manuscript-level work.

**[FILL IN — biographical / bibliographical notes on Gajendra Thakur,
N.K. Jha, and Vidyanand Jha; relationship of the 2009 volumes to
earlier 20th-century efforts (e.g. those in Maithili periodicals); any
post-2009 publications worth listing.]**

---

## 6. Glossary

| Term | Meaning |
| --- | --- |
| *Ādibīja* (आदिबीज) | "Root seed" — the originating ancestor of a lineage. |
| *Bījī* / *Bījī puruṣa* (बीजी / बीजी पुरुष) | The founding ancestor recorded for a particular family in a particular mool. The corpus is largely a list of *bījīs*. |
| *Mool* (मूल) | The ancestral village-identity of a Maithil Brahmin family. |
| *Gotra* (गोत्र) | The patrilineal Vedic clan. |
| *Panji* / *pañjī* (पञ्जी) | Register; the genealogical record itself. |
| *Panjikar* (पञ्जीकार) | The hereditary scribe who maintains a panji. |
| *Pañjībaddha* (पञ्जीबद्ध) | "Bound into the register" — a family whose lineage is recorded. |
| *Siddhānta* (सिद्धान्त) | The written marriage-clearance issued by a Panjikar certifying that the union does not violate sapinda. Sometimes also called *aswajan-patra*. |
| *Sapinda* (सपिण्ड) | The prohibition on marriage between persons sharing a recent common male ancestor (seven generations on the father's side, five on the mother's). |
| *Vanśāvalī* (वंशावली) | A household's own hand-kept genealogy, as distinct from the formal Panji register. |
| *Mithilakshara* (मिथिलाक्षर) | The traditional script of Mithila, used in older Panji manuscripts. Distinct from Devanagari. |

---

## 7. Further reading

*A working bibliography. Items marked __[verify]__ I have not personally
consulted.*

- Thakur, Gajendra; Jha, N.K.; Jha, Panjikar Vidyanand.
  *Genome Mapping (450 A.D. to 2009 A.D.) — Mithilak Panji Prabandh,
  Vol. I–III.* Shruti Publication, New Delhi, 2009.
  ISBN 978-81-907729-6-9.
- Mishra, Jayakanta. *A History of Maithili Literature.* Sahitya
  Akademi. **[verify]**
- Choudhary, Radhakrishna. *A Survey of Maithili Literature*; *Mithila
  in the Age of Vidyapati*. **[verify]**
- Jha, Shashinath. Essays on the Panji system. **[verify]**
- Robinson, I., and Webber, J. *Graph Databases.* O'Reilly. (Technical
  reference for the storage model.)
- Kumarila Bhatta, *Tantra-Vārtika*, on the institution of
  *samūha-lekhya* (community lineage records). **[verify edition]**

**[FILL IN — academic articles on Maithil Brahmin genealogy; Maithili
periodicals that have published Panji material; theses; webliography of
existing online Maithil genealogy efforts that this project should be
aware of.]**

---

## 8. Sections to be expanded

This document is deliberately a placeholder. Sections most worth
expanding next:

- **Section 1**: the political geography of medieval Mithila.
- **Section 3**: the founding narrative as told in the source's
  Sanskrit verses.
- **Section 5**: more on what the Karna Kayastha and Kshatriya panji
  traditions looked like, since this project plans eventual extension.
- **Section 7**: a properly cited bibliography.

Contributions to this document — corrections, additions, removed
inaccuracies — are particularly welcome from scholars of Mithila and
from descendants of Panjikar families with first-hand knowledge.
