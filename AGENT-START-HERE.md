# AGENT START HERE

```bash
git clone https://github.com/prx0r/gochema.git && cd gochema
bash tools/r2.sh ls renders/   # needs /root/.r2-env on the box
```

Read in order: `README.md` → `series/README.md` (the bible) →
`series/BUILD-PIPELINE.md` → `essays/daimon-companion/ANALYSIS.md`.

## What you get
- `essays/daimon-companion/` — source essay (1,449w), 102-shot storyboard
  (638.6s), narration, alignment + integrity reports from the volume build.
- `imports/` — volume manifest + R2 bucket map. Media referenced by path,
  never vendored.

## Rules
Additive changes only. No binaries in git. No creds in repo. No invented
citations — every quote carries its RO passage tag.
