#!/usr/bin/env python3
"""Stale path audit (Officer Kit, folder-triage). Copy to <working folder>/_build/.
Usage: python path_audit.py                 report every path in a note that no longer exists, with its current home
       python path_audit.py --fix           rewrite each stale path that resolves to exactly one current file or folder
       python path_audit.py [--fix] <file or folder> ...   audit only these
Reads .md and .txt files (the rules file, SOPs, status notes). Never reads or edits issued sources
(Reference folders), _archive, git repos, 00 Inbox, Claude outputs, or anything named by a skip: or
noaudit: line (noaudit: a record that lists old paths on purpose, such as a cleanup report).
A path counts when it starts with the working folder as notes spell it: the absolute root, or any
alias: line in _build/folder_check_allow.txt (alias: C:\\TBS). The current home comes from the folder
itself, matched by name; a name found in two places is AMBIGUOUS and left for the user.
Exit 0 = no stale paths left, 1 = stale or ambiguous paths remain."""
import os, re, sys
args = sys.argv[1:]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if '--root' in args:
    i = args.index('--root'); ROOT = os.path.abspath(args[i + 1]); del args[i:i + 2]
FIX = '--fix' in args; args = [a for a in args if a != '--fix']

def config(root):
    c = {'skip': [], 'alias': [], 'noaudit': []}
    p = os.path.join(root, '_build', 'folder_check_allow.txt')
    if os.path.exists(p):
        for l in open(p, encoding='utf-8'):
            k, _, v = l.strip().partition(':')
            if k in c and v.strip(): c[k].append(v.strip() if k == 'alias' else v.strip().replace('\\', '/').strip('/'))
    return c
C = config(ROOT)
def under(r, prefixes): return any(r == p or r.startswith(p + '/') for p in prefixes)
def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, '/')

# every file and folder in the working folder, by name (archives and machinery included, so moved
# history still resolves; a hit inside _archive is used only when nothing outside matches)
names, dirnames = {}, set()
for dp, dn, fn in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in ('.git', 'node_modules', '__pycache__')]
    r = rel(dp)
    for n in dn + fn:
        names.setdefault(n.lower(), []).append(('' if r == '.' else r + '/') + n)
    dirnames.update(d.lower() for d in dn)

def resolve(old):
    """old: a stale path relative to the root, '/' separated. Returns (new, why)."""
    segs = [s for s in old.split('/') if s]
    if not segs: return None, 'empty'
    if any(x.lower() not in dirnames for x in segs[:-1]): return None, 'not a path'   # words, not folders
    cands = names.get(segs[-1].lower(), [])
    if not os.path.splitext(segs[-1])[1]:   # a folder name: it stays under the deepest folder that still exists
        anc = ''
        for i in range(len(segs) - 1, 0, -1):
            if os.path.isdir(os.path.join(ROOT, *segs[:i])): anc = '/'.join(segs[:i]); break
        if anc: cands = [c for c in cands if c.startswith(anc + '/')]
    live = [c for c in cands if '/_archive/' not in '/' + c + '/' and not c.startswith('_archive/')]
    cands = live or cands
    k = 2
    while len(cands) > 1 and k <= len(segs):   # use parent folder names to break a tie
        tail = '/'.join(segs[-k:]).lower()
        narrowed = [c for c in cands if c.lower().endswith(tail)]
        if not narrowed: break
        cands = narrowed; k += 1
    if len(cands) == 1: return cands[0], 'by name'
    return None, ('AMBIGUOUS: ' + ' | '.join(cands[:4])) if cands else 'NOT FOUND'

prefixes = [ROOT] + C['alias']
def rx(p): return ''.join(r'[\\/]' if ch in '\\/' else re.escape(ch) for ch in p.rstrip('\\/'))
pre = re.compile('(' + '|'.join(rx(p) for p in prefixes) + r')[\\/]', re.I)
BODY = re.compile(r'[^`"\'<>|*\n\r;]+')
CUT = set(' ,.;:)]\\/')

def scan_text(text):
    """Yield (start, end, rel_old, sep, new_or_None, why) for each stale path in text."""
    for m in pre.finditer(text):
        b = BODY.match(text, m.end())
        if not b: continue
        s = b.group(0); nxt = pre.search(s)
        if nxt: s = s[:nxt.start()]
        sep = text[m.end() - 1]
        if s.startswith(('<', '[')): continue
        cuts = sorted({i for i in range(1, len(s) + 1) if i == len(s) or s[i] in CUT}, reverse=True)
        found = None
        for cut in cuts:
            cand = s[:cut].rstrip('\\/ ')
            if not cand: continue
            r = cand.replace('\\', '/')
            if os.path.exists(os.path.join(ROOT, r)): found = ('ok',); break
            new, why = resolve(r)
            if new: found = ('stale', cand, new, why); break
        if not found:
            first = re.split(r'[,;)]|\.\s', s)[0].strip().rstrip('.')
            r = first.replace('\\', '/')
            if r and not os.path.exists(os.path.join(ROOT, r)):
                new, why = resolve(r)
                if why == 'not a path' and not os.path.splitext(r)[1]: continue   # prose, not a file
                yield (m.start(), m.end() + len(first), r, sep, None, why)
            continue
        if found[0] == 'stale':
            cand, new, why = found[1], found[2], found[3]
            yield (m.start(), m.end() + len(cand), cand.replace('\\', '/'), sep, new, why)

targets = [os.path.abspath(a) for a in args] or [ROOT]
docs = []
for t in targets:
    if os.path.isfile(t): docs.append(t); continue
    for dp, dn, fn in os.walk(t):
        r = rel(dp); r = '' if r == '.' else r
        keep = []
        for d in dn:
            rd = (r + '/' + d).lstrip('/')
            if d in ('.git', 'node_modules', '__pycache__', '_archive', 'triage') or d.startswith('.'): continue
            if os.path.isdir(os.path.join(dp, d, '.git')) or under(rd, C['skip']) or under(rd, C['noaudit']): continue
            if r == '' and (d.lower().startswith(('reference', '00 inbox')) or d.lower() == 'claude outputs'): continue
            keep.append(d)
        dn[:] = keep
        docs += [os.path.join(dp, f) for f in fn if f.lower().endswith(('.md', '.txt')) and f != 'INDEX.md' and not under((r + '/' + f).lstrip('/'), C['noaudit'])]

stale = fixed = unresolved = 0
for d in docs:
    try: text = open(d, encoding='utf-8').read()
    except (UnicodeDecodeError, OSError): continue
    hits = list(scan_text(text))
    if not hits: continue
    out, last = [], 0
    for a, b, old, sep, new, why in hits:
        stale += 1
        if new:
            print(f'STALE  {rel(d)}: {old}  -> {new}')
            if FIX:
                head = text[a:b][:len(text[a:b]) - len(old)]
                out.append(text[last:a] + head + new.replace('/', sep)); last = b; fixed += 1
        else:
            unresolved += 1; print(f'{"AMBIG " if why.startswith("AMBIG") else "LOST  "} {rel(d)}: {old}  ({why})')
    if FIX and out:
        out.append(text[last:]); open(d, 'w', encoding='utf-8').write(''.join(out))
print(f'\n{stale} stale paths in {len(docs)} notes; ' + (f'{fixed} rewritten; ' if FIX else f'{stale - unresolved} can be fixed with --fix; ') + f'{unresolved} need a person')
sys.exit(0 if stale - fixed == 0 else 1)
