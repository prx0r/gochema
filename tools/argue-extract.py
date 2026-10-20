#!/usr/bin/env python3
"""Extract argument graphs from pushing-tantraloka logicvid sessions.

Session files already ARE argument maps (objection → answer+quotes →
resolution → honest-remainder). This script makes the structure explicit:

  nodes: [{id, kind, text, source:{file,line}}]
    kind ∈ question | claim | quote | resolution | gap
  edges: [{from, to, rel}]
    rel ∈ answers | supports | resolves | leaves-open | follows

Shapes:
  objection — "## OBJECTION n …" + **The objection:** / answer / resolution /
    remainder blocks + PENETRATION summaries.
  round     — "## ROUND n …" sections; blockquotes become quote nodes;
    frontier/crux/unresolved sections become gap nodes.
  generic   — ## headers → claim nodes (child of previous = follows);
    blockquotes → quote nodes on nearest claim; lines matching
    unresolved|remainder|open question|don't know|left open → gap nodes.

Every node carries file+line provenance (ClaimGraph principle: no node
without a source). Steal-safe: output shape mirrors reasons.js
({id,text} + {from,to,type}) and maps to AIF (I-nodes/C-nodes).

Usage: argue-extract.py IN.md [OUT.json]  (stdout if no OUT)
"""
import json
import re
import sys


def _lines(text):
    return text.splitlines()


def _quotes(block, fname, base):
    """Yield quote nodes for markdown quote lines in block (with line nos)."""
    out, cur, start = [], [], None
    for i, ln in block:
        s = ln.strip()
        if s.startswith('>'):
            if cur == [] or True:
                if not cur:
                    start = base + i
                cur.append(s.lstrip('> ').strip())
        else:
            if cur:
                txt = ' '.join(c for c in cur if c).strip()
                if len(txt) > 20:
                    out.append(('quote', txt, start))
                cur, start = [], None
    if cur:
        txt = ' '.join(c for c in cur if c).strip()
        if len(txt) > 20:
            out.append(('quote', txt, start))
    return out


class Graph:
    def __init__(self, fname):
        self.fname = fname
        self.nodes = []
        self.edges = []
        self.n = 0

    def add(self, kind, text, line):
        self.n += 1
        nid = f'n{self.n}'
        self.nodes.append({'id': nid, 'kind': kind,
                           'text': text.strip()[:2000],
                           'source': {'file': self.fname, 'line': line}})
        return nid

    def link(self, a, b, rel):
        self.edges.append({'from': a, 'to': b, 'rel': rel})

    def doc(self):
        return {'nodes': self.nodes, 'edges': self.edges}


def _clean(text):
    """Strip quote/table markup from prose nodes (quotes keep their own)."""
    lines = [re.sub(r'^\s*>\s?', '', ln) for ln in text.splitlines()]
    text = '\n'.join(lines)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    return re.sub(r'[ \t]+', ' ', text).strip()


def _split_sections(lines):
    """[(level, title, lineno, [(lineno, line), ...])] for ##/### sections.
    H1 is the doc title, not a node — unless the doc has no H2 at all."""
    secs, cur = [], None
    has_h2 = any(re.match(r'^##(?!#)\s', ln) for ln in lines)
    for i, ln in enumerate(lines, 1):
        m = re.match(r'^(#{1,3})\s+(.+?)\s*$', ln)
        if m and '|' not in ln and (len(m.group(1)) > 1 or not has_h2):
            if cur:
                secs.append(cur)
            cur = {'level': len(m.group(1)), 'title': m.group(2).strip(),
                   'line': i, 'body': []}
        elif cur is not None:
            cur['body'].append((i, ln))
    if cur:
        secs.append(cur)
    return secs


def _shape_of(title):
    t = title.upper()
    if 'OBJECTION' in t:
        return 'objection'
    if re.search(r'\bROUND\b', t):
        return 'round'
    return None


def extract(text, fname):
    lines = _lines(text)
    g = Graph(fname)
    secs = _split_sections(lines)
    if not secs:
        return g.doc()
    shapes = {_shape_of(s['title']) for s in secs}
    if 'objection' in shapes:
        return _extract_objection(g, secs)
    if 'round' in shapes:
        return _extract_round(g, secs)
    return _extract_generic(g, secs, lines)


def _block_text(body):
    return '\n'.join(ln for _, ln in body)


def _extract_objection(g, secs):
    prev_q = None
    for s in secs:
        if _shape_of(s['title']) != 'objection':
            continue
        body = _block_text(s['body'])
        m = re.search(r'\*\*The objection:\*\*\s*(.+?)(?=\n\*\*|\Z)', body, re.S)
        qtext = _clean(m.group(1).strip() if m else s['title'])
        q = g.add('question', qtext, s['line'])
        if prev_q:
            g.link(prev_q, q, 'follows')
        prev_q = q
        m = re.search(r'\*\*(?:The text.s answer|The answer)[^*]*\*\*\s*(.+?)(?=\n\*\*|\Z)', body, re.S)
        if m:
            a = g.add('claim', _clean(m.group(1).strip()), s['line'])
            g.link(a, q, 'answers')
            last = a
        else:
            last = q
        for kind, txt, ln in _quotes(s['body'], g.fname, 0):
            if txt.replace('*', '').upper().startswith('PENETRATION'):
                continue  # gets its own resolution node below
            qn = g.add('quote', txt, ln)
            g.link(qn, last, 'supports')
        m = re.search(r'\*\*(?:The resolution|Resolution)[^*]*\*\*\s*(.+?)(?=\n\*\*|\Z)', body, re.S)
        if m:
            r = g.add('resolution', _clean(m.group(1).strip()), s['line'])
            g.link(r, q, 'resolves')
            last = r
        m = re.search(r'\*\*(?:The honest remainder|Honest remainder|remainder)[^*]*\*\*\s*(.+?)(?=\n\*\*|\Z)', body, re.S | re.I)
        if m:
            gp = g.add('gap', _clean(m.group(1).strip()), s['line'])
            g.link(last, gp, 'leaves-open')
        for m in re.finditer(r'\*\*PENETRATION[^*]*\*\*\s*(.+?)(?=\n\*\*|\Z)', body, re.S):
            p = g.add('resolution', 'PENETRATION: ' + _clean(m.group(1).strip())[:1200], s['line'])
            g.link(p, q, 'resolves')
    return g.doc()


def _extract_round(g, secs):
    prev = None
    for s in secs:
        title = s['title']
        if 'BRANCH' in title.upper() or 'LESSON' in title.upper():
            continue
        q = g.add('question' if re.search(r'\bROUND\b', title, re.I) else 'claim',
                  title, s['line'])
        if prev:
            g.link(prev, q, 'follows')
        prev = q
        body = _block_text(s['body'])
        if re.search(r'frontier|crux|unresolved|left open|survives', title, re.I):
            gp = g.add('gap', _clean(body[:1200]), s['line'])
            g.link(q, gp, 'leaves-open')
            continue
        for kind, txt, ln in _quotes(s['body'], g.fname, 0):
            qn = g.add('quote', txt, ln)
            g.link(qn, q, 'supports')
        paras = [p.strip() for p in re.split(r'\n\s*\n', body) if len(p.strip()) > 120]
        paras = [p for p in paras if not p.strip().startswith('>')][:2]
        for p in paras:
            c = g.add('claim', _clean(re.sub(r'\s+', ' ', p))[:800], s['line'])
            g.link(c, q, 'answers')
    return g.doc()


GAP_RE = re.compile(r'unresolved|remainder|open question|don.t know|left open|not fully|tension', re.I)


def _extract_generic(g, secs, lines):
    prev = None
    for s in secs:
        q = g.add('claim', s['title'], s['line'])
        if prev:
            g.link(prev, q, 'follows')
        prev = q
        for kind, txt, ln in _quotes(s['body'], g.fname, 0):
            qn = g.add('quote', txt, ln)
            g.link(qn, q, 'supports')
        for i, ln in s['body']:
            if GAP_RE.search(ln) and len(ln.strip()) > 40:
                gp = g.add('gap', _clean(ln.strip())[:600], i)
                g.link(q, gp, 'leaves-open')
                break
    return g.doc()


def main():
    if len(sys.argv) < 2:
        print('usage: argue-extract.py IN.md [OUT.json]', file=sys.stderr)
        sys.exit(2)
    text = open(sys.argv[1], encoding='utf-8', errors='replace').read()
    fname = sys.argv[1].split('/')[-1]
    doc = extract(text, fname)
    out = json.dumps(doc, indent=1, ensure_ascii=False)
    if len(sys.argv) > 2:
        open(sys.argv[2], 'w').write(out)
        print(f'{len(doc["nodes"])} nodes, {len(doc["edges"])} edges -> {sys.argv[2]}')
    else:
        print(out)


if __name__ == '__main__':
    main()
