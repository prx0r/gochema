# Hillside Hermitage — talk archive (refs + transcripts)

Ajahn Ñāṇamoli Thero / Hillside Hermitage (Early Buddhist suttas, Middle Way).
Source: `archive.hillsidehermitage.org` (Internet Archive).

- `index.json` — all **499 talks**: code (NNNhh), title, date, duration,
  `youtube` id + `mp3` url (references only — **no media vendored**, per the
  repo's no-binaries rule). `transcript_file` points at the extracted text.
- `transcripts/*.txt` — **129 talks** with a transcript PDF on the archive.
  Text extracted from the archive.org PDFs; each file's header carries the
  date, duration, and YouTube id so a clip window can be cut later.

## Why this is here
The essay `essays/rebirth-explained/` needs a canonical **early-Buddhism**
voice. Hillside Hermitage is it. Key rebirth talks:
- **244hh "Is Belief in Rebirth Necessary?"** (MN 60 — the burden-of-proof
  sutta) `sVc45SXDrEQ`, 10:58. YT+MP3 only (no transcript PDF).
- **04hh "Do we live only once?"** `QXdTop65GTQ`, 8:33 (transcript present).
- **319hh "What exists after death?"** (SN 22.85) `6QvCj_YmUWE`, 51:51.

## Working with transcripts (bypasses the YouTube IP block)
`index.json` + the transcript texts live on archive.org / in this dir — none
of it is YouTube, so they fetch fine from this box. To find an exact clip
moment: grep a transcript, then cut the matching `t=` window from the linked
YouTube id (duration is in the header). The transcripts are condensed text,
not word-timed, so a precise `t=` still needs the video's caption track
(see CLIPS.md — blocked from this box without cookies/egress).
