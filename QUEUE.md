# QUEUE — every video, in working order (2026-10-20)

> Each row = one quill pack (File → Video packs…). Pack slug in `pack:`.
> Statuses: WRITING (script in progress) · BUILD (spec/core done, expand next)
> · SCAFFOLD (concept + acquire list) · PARKED (idea only).

| # | Video | Pack | Status | Next action |
|---|---|---|---|---|
| 1 | Buddhist Reincarnation, Actually Explained (30-min v1) | `rebirth` | WRITING (v1.2 citation-verified) | Owner voice review: 4 decisions in FINISH-IN-QUILL.md |
| 2 | Śaiva: Recognition, Not Rebirth (TEMPLATE film) | `film-saiva` | BUILD (full script + storyboard) | Expand per v1 recipe; mirror-merge money shot defines the standard |
| 3 | What Actually Happens When You Pray (NEW) | `prayer` | SCAFFOLD (2 stops banked, 6 to acquire) | Thesis pick A/B/C + ACQUIRE stops 3–8 |
| 4 | Why Karma Governs Your Life (NEW — owner brief verbatim) | `karma` | SCAFFOLD (ladder + unfairness anchor banked, 8 extracts) | Owner: cold-open + unfairness-charge words; bank ālaya/Abhidhammattha; ACQUIRE theodicy voice |
| 5 | What Actually Is Transmission? (NEW — diksha/Tibetan/wang) | `transmission` | SCAFFOLD (Paramārthasāra banked, Dyczkowski insight) | ACQUIRE: Dyczkowski clip, Tibetan wang sources, Zen/Theravāda positions |
| 6 | What If the Guru Doesn't Find You? (NEW — trope deconstruction) | `guru-finds-you` | SCAFFOLD (Theosophy origin + Nachiketa + Eklavya banked) | ACQUIRE: primary sources for Katha/Eklavya; owner cold-open + close |
| 7–18 | 12 remaining tradition films (Hindu → Astral) | `film-<tradition>` | BUILD (core + movie spec each) | Roster order; buddhist-v1 recipe per film (MOVIE.md = beats+cine+READs) |
| 19 | Enter Another Body At Will (special) | `special-enter-another-body` | BUILD (script written) | Cross-tradition trope chapter; rights gates still open |
| 20 | How to Leave Your Body (gateway special) | `special-gateway` | BUILD (spec written) | Wikisource memo fetch; sources in SPEC |
| 21 | Daimon Companion (seed film) | `daimon` | BUILD (102-shot storyboard, audited) | Render path per BUILD-PIPELINE |
| 22 | Fire Simile | `fire-simile` | BUILD (v1 reading + v2 analysis) | Voice synth decision (Louis vs old-man take on R2) |
| 23 | Dependent Origination | `dependent-origination` | SCAFFOLD (source + structure) | Essay draft (v2 stream-entry spine) |
| 24 | Fundamental Structure (Ñāṇavīra) | `fundamental-structure` | SCAFFOLD (extracts + structure) | Time-doctrine video spec (feeds rebirth ch.9) |

## Parked (no pack yet — say the word and they get scaffolded like prayer)
- **Recognition Actually Explained** (Utpaladeva proof — argument map exists in pushing-tantraloka + Ratié shelf)
- **Theurgy** (3×10min or 1×30min; needs R2 goldfiles verify)
- **Levin Taken to Absurdism** (needs substack + paper pulls)
- **Science of Rebirth** (standalone follow-up; science cut from v1 lives here)
- **Stream Entry v2 / Nirvāṇa v3** (trilogy shelf), **TBOTD-animated spin-off**

## How the queue works in quill
One film at a time: load its pack, attach 1–3 of ITS sources in chat, write.
Don't cross-attach packs — the compiler prompt checks against attached
sources only. When a film wraps, its pack rebuilds from the repo
(`deploy/build-packs.sh`) and the new version is one click away.
