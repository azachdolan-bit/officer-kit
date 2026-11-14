#!/usr/bin/env python3
"""Inventory a folder and propose archive moves (Officer Kit, folder-triage). Moves nothing.
Usage: python triage_scan.py <working folder> [--out <dir>]   (default out: <working folder>/_build/triage)
Writes inventory.csv (every file: size, modified, path) and manifest.csv (action, from, to, reason):
  ARCHIVE  an older version beside a newer one, or an extra exact copy; goes to _archive in its own folder
  RENAME   a dead file folder (_to_delete, _old, Archive, ...) becomes _archive
  DECIDE   a copy whose keeper is a judgment call; the user picks before apply_moves runs
Never proposes a move inside a git repo, a Reference folder, a sent record, or an underscore folder."""
import os, re, sys, csv, hashlib, collections
args = sys.argv[1:]
ROOT = os.path.abspath(args[0]); OUT = os.path.join(ROOT, '_build', 'triage')
if '--out' in args: OUT = os.path.abspath(args[args.index('--out') + 1])
os.makedirs(OUT, exist_ok=True)
DEAD = re.compile(r'(?i)^(_?to[ _]?delete.*|_?superseded|_?old( docs)?|archive|old|backups?|.*backups|old versions?|previous versions?)$')
JUNK = re.compile(r'(^\.~lock|^~\$|\.tmp$|\.bak\d*$|^Thumbs\.db$|^desktop\.ini$|^\.DS_Store$)')
VER = re.compile(r'(?i)(?:^|[ _\-(])+(draft|rev|v|iter)[ _]?(\d+(?:\.\d+)?)\)?(?=$|[ _\-.)(])')
DATE = re.compile(r'(?i)\s*\(?\b\d{1,2} (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* ?\d{0,2}\)?')
COPY = re.compile(r'(?i)\s*\(\d\)$|\)-\d$|\bcopy\b')
SENT = re.compile(r'(?i)(^|/)(to|sent to) [^/]+(/|$)')
def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, '/')
def protected(r):
    top = r.split('/')[0].lower()
    return top.startswith('reference') or bool(SENT.search(os.path.dirname(r))) or any(seg.startswith('_') for seg in r.split('/')[:-1])
inv, rows, repos = [], [], []
for dp, dn, fn in os.walk(ROOT):
    if '.git' in dn: repos.append(dp); dn[:] = []; continue
    for d in list(dn):
        if DEAD.match(d) and d != '_archive':
            rows.append(['RENAME', rel(os.path.join(dp, d)), rel(os.path.join(dp, '_archive')), 'dead file folder; one archive name only'])
    dn[:] = [d for d in dn if not d.startswith('.') and d not in ('node_modules', '__pycache__', '_archive') and not DEAD.match(d)]
    for f in fn:
        p = os.path.join(dp, f)
        try: st = os.stat(p)
        except OSError: continue
        inv.append((rel(p), st.st_size, st.st_mtime))
w = csv.writer(open(os.path.join(OUT, 'inventory.csv'), 'w', newline='', encoding='utf-8'))
w.writerow(['path', 'bytes', 'modified'])
import time
for r, s, m in inv: w.writerow([r, s, time.strftime('%Y-%m-%d', time.localtime(m))])
done = set()
def arch(r, why, action='ARCHIVE'):
    d, f = os.path.split(r); rows.append([action, r, (d + '/' if d else '') + '_archive/' + f, why]); done.add(r)
for r, s, m in inv:
    if JUNK.search(os.path.basename(r)) and not protected(r): arch(r, 'junk file')
groups = collections.defaultdict(list)
for r, s, m in inv:
    if protected(r) or r in done: continue
    d, f = os.path.split(r); stem, ext = os.path.splitext(f)
    v = VER.search(stem); ver = float(v.group(2)) if v else None
    n = re.sub(r'\([^)]*\)', '', stem) if v else stem
    n = VER.sub('', n); n = DATE.sub('', n); n = COPY.sub('', n)
    groups[(d, re.sub(r'[\s_\-]+', ' ', n).strip().lower(), ext.lower())].append((r, ver, m))
for k, g in groups.items():
    if len(g) < 2: continue
    marked = [x for x in g if x[1] is not None or DATE.search(os.path.basename(x[0])) or COPY.search(os.path.splitext(os.path.basename(x[0]))[0])]
    if not marked: continue
    g.sort(key=lambda x: (x[1] if x[1] is not None else -1, x[2]))
    for x in g[:-1]: arch(x[0], 'older version; current is ' + os.path.basename(g[-1][0]))
bysize = collections.defaultdict(list)
for r, s, m in inv:
    if s > 1024 and r not in done: bysize[s].append(r)
byhash = collections.defaultdict(list)
for s, rs in bysize.items():
    if len(rs) > 1:
        for r in rs:
            with open(os.path.join(ROOT, r), 'rb') as fh: byhash[hashlib.md5(fh.read()).hexdigest()].append(r)
for h, rs in byhash.items():
    movable = [r for r in rs if not protected(r)]
    if len(rs) < 2 or not movable: continue
    keepers = [r for r in rs if protected(r)]
    pdf_in_print = [r for r in movable if r.split('/')[0].lower() == 'print' and r.lower().endswith('.pdf')]
    if keepers and not pdf_in_print:
        for r in movable: arch(r, 'exact copy of ' + keepers[0], 'DECIDE')
        continue
    keep = pdf_in_print[0] if pdf_in_print else sorted(movable, key=lambda r: (r.split('/')[0].lower().startswith('00 inbox'), -r.count('/')))[0]
    for r in movable:
        if r != keep: arch(r, 'exact copy of ' + keep, 'DECIDE' if os.path.dirname(r) != os.path.dirname(keep) and not r.split('/')[0].lower().startswith('00 inbox') else 'ARCHIVE')
w = csv.writer(open(os.path.join(OUT, 'manifest.csv'), 'w', newline='', encoding='utf-8'))
w.writerow(['action', 'from', 'to', 'reason'])
for row in rows: w.writerow(row)
c = collections.Counter(r[0] for r in rows)
print(f'{len(inv)} files, {sum(s for _, s, _ in inv) / 1048576:.1f} MB; git repos left alone: {len(repos)}')
print('manifest: ' + ', '.join(f'{k} {v}' for k, v in sorted(c.items())) + f'  -> {os.path.join(OUT, "manifest.csv")}')
