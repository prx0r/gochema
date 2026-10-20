"""Unit tests for argue-extract.py — run: python3 -m pytest tools/test_argue_extract.py"""
import json
import os
import subprocess
import sys
import tempfile

TOOL = os.path.join(os.path.dirname(__file__), 'argue-extract.py')


def run(md: str):
    with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False) as f:
        f.write(md)
        src = f.name
    out = src + '.json'
    r = subprocess.run([sys.executable, TOOL, src, out], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    with open(out) as fh:
        return json.load(fh)


def kinds(doc):
    from collections import Counter
    return Counter(n['kind'] for n in doc['nodes'])


def test_objection_shape():
    doc = run('''# Session title here

## OBJECTION 1 — why play?

**The objection:** Why would Siva play when people suffer?

**The text's answer (TA 1.1):**
> "Play is the free becoming of consciousness."

**The resolution:** Play means free becoming, not fun.

**The honest remainder:** Why call it play at all remains open.

> **PENETRATION 1:** Play is structural, not emotional.
''')
    k = kinds(doc)
    assert k['question'] == 1, k
    assert k['quote'] == 1, k  # penetration excluded (own node)
    assert k['resolution'] >= 2, k
    assert k['gap'] == 1, k
    assert all(n['source']['line'] > 0 for n in doc['nodes'])
    rels = {e['rel'] for e in doc['edges']}
    assert {'answers', 'supports', 'resolves', 'leaves-open'} <= rels, rels


def test_round_shape():
    doc = run('''# Session

## ROUND 0 — the mechanism

Some mechanism prose here that runs long enough to be a claim paragraph
about how the three impurities drive transmigration forward step by step.

> "Transmigratory existence is due to impurity."

## ROUND 4 — the frontier that survives

What remains unresolved about freedom versus law is left open here.
''')
    k = kinds(doc)
    assert k['question'] == 2, k
    assert k['quote'] == 1, k
    assert k['gap'] == 1, k


def test_h1_not_a_node():
    doc = run('# Just a title\n\n## OBJECTION 1 — x?\n\n**The objection:** Why?\n')
    texts = [n['text'] for n in doc['nodes']]
    assert not any('Just a title' in t for t in texts)


def test_empty_doc():
    doc = run('No headings here, just prose.\n')
    assert doc == {'nodes': [], 'edges': []}
