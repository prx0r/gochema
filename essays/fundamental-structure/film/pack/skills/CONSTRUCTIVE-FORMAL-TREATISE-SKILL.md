---
name: constructive-formal-treatise
description: Convert a recursive formal construction into one continuous visual proof-state system without replacing its symbols or silently completing unfinished arguments.
version: 1.0
---

# Constructive Formal Treatise Skill

## Read the source as construction

For every numbered section record:

```json
{
  "currentRepresentation": "",
  "problem": "",
  "newOperation": "",
  "resultingRepresentation": "",
  "invariant": "",
  "unresolvedPoint": ""
}
```

## Persistent alphabet

Choose the smallest possible visual alphabet.

Do not replace symbols when the argument moves to a higher order. Recombine,
nest, weight, or transform the original symbols.

## Required scene types

- primitive introduction;
- failed representation;
- distinction;
- operation;
- pairing;
- group or transformation table;
- recursive construction;
- invariant-under-action scene;
- hierarchy;
- temporal transformation;
- weighting;
- incomplete frontier.

## Spatial warning

When the source explicitly distinguishes the structure of space from a structure
drawn in space, mark every spatial layout as representational convenience.

Do not imply that left/right placement is the formal distinction.

## Recursive warning

A recursive scene must visibly preserve the lower-order grammar.

A larger grid with unrelated content is not recursion.

## Dynamic warning

Distinguish:

- periodic change;
- accelerating change;
- replacement;
- reversible interchange;
- hierarchy of temporal order.

## Unfinished sources

Stop where the source stops.

Render the open variables or next questions. Never manufacture a conclusion.

## Review

Test every scene without narration:

- Which operation occurred?
- What stayed invariant?
- Which order of structure is visible?
- Could position be mistaken for identity?
- Is the recursion structurally legible?
