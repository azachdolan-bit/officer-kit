#!/usr/bin/env python3
"""Folder discipline check (Officer Kit, folder-triage). Copy to <working folder>/_build/.
Usage: python folder_check.py [folder ...]   no folder = the whole working folder (the parent of _build)
       python folder_check.py --root <working folder> [folder ...]
Config (optional): _build/folder_check_allow.txt, one directive per line:
  since: YYYY-MM-DD    version words in a current file name fail only for files changed on or after this date
  root: <name>         an allowed entry at the top of the working folder (any root line turns the root check on)
  skip: <rel path>     a folder not checked at all (a repo, issued sources, machinery)
  copy: <rel path>     a folder whose files may duplicate files elsewhere (an export, a sent record)
  <rel path>           a file allowed to look like a version of its neighbor (two different products)
A top level "Claude outputs" folder is where the desktop app drops files sent to chat: copies by design,
never a duplicate violation, emptied with the inbox (age warning after 7 days).
Exit 0 = no violations, 1 = violations."""
import os, re, sys, hashlib, subprocess, time, collections
args = sys.argv[1:]
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if '--root' in args:
    i = args.index('--root'); ROOT = os.path.abspath(args[i + 1]); del args[i:i + 2]
CFG = os.path.join(ROOT, '_build', 'folder_check_allow.txt')
since, roots, skips, copies, allow = 0.0, set(), [], [], set()
if os.path.exists(CFG):
    for l in open(CFG, encoding='utf-8'):
        l = l.strip().replace('\\', '/')
        if not l or l.startswith('#'): continue
        k, _, v = l.partition(':')
        if k in ('since', 'root', 'skip', 'copy') and v:
            v = v.strip().strip('/')
            if k == 'since': since = time.mktime(time.strptime(v, '%Y-%m-%d'))
            elif k == 'root': roots.add(v)
            elif k == 'skip': skips.append(v)
            else: copies.append(v)
        else: allow.add(l)
DEAD = re.compile(r'(?i)^(_?to[ _]?delete.*|_?superseded|_?old( docs)?|archive|old|backups?|.*backups|old versions?|previous versions?)$')
JUNK = re.compile(r'(^\.~lock|^~\$|\.tmp$|\.bak\d*$|^Thumbs\.db$|^desktop\.ini$|^\.DS_Store$)')
VER = re.compile(r'(?i)(?:^|[ _\-(])+(draft|rev|v|iter)[ _]?\d+(?:\.\d+)?\)?(?=$|[ _\-.)(])|\bfinal\b|\bcopy\b|\(\d\)$|\)-\d$')
DATE = re.compile(r'(?i)\s*\(?\b\d{1,2} (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]* ?\d{0,2}\)?')
SENT = re.compile(r'(?i)(^|/)(to|sent to) [^/]+(/|$)')
PRINT_OK = {'.pdf', '.docx', '.png', '.jpg', '.jpeg'}
def rel(p): return os.path.relpath(p, ROOT).replace(os.sep, '/')
def under(r, prefixes): return any(r == p or r.startswith(p + '/') for p in prefixes)
def is_copy_ok(r): return r.lower().startswith('claude outputs/') or under(r, copies) or bool(SENT.search(os.path.dirname(r))) or r.split('/')[0].lower().startswith('reference') or '/_source/' in '/' + r
def norm(stem):
    s = re.sub(r'\([^)]*\)', '', stem) if VER.search(stem) else stem
    s = VER.sub('', s); s = DATE.sub('', s)
    return re.sub(r'[\s_\-]+', ' ', s).strip().lower()
fails, warns, files = [], [], []
targets = [os.path.abspath(a) for a in args] or [ROOT]
for t in targets:
    for dp, dn, fn in os.walk(t):
        r = rel(dp); r = '' if r == '.' else r
        for d in dn:
            rd = (r + '/' + d).lstrip('/')
            if DEAD.match(d) and not under(rd, skips): fails.append(f'DEAD FOLDER  {rd}  -> rename to _archive')
        keep = []
        for d in dn:
            rd = (r + '/' + d).lstrip('/')
            if d.startswith('.') or d.startswith('_') or d in ('node_modules', '__pycache__') or under(rd, skips): continue
            if os.path.isdir(os.path.join(dp, d, '.git')): continue
            if r == '' and d.lower().startswith('reference'): continue
            keep.append(d)
        dn[:] = keep
        files += [os.path.join(dp, f) for f in fn]
if ROOT in targets and roots:
    for n in os.listdir(ROOT):
        if n not in roots and n.lower() != 'claude outputs' and not n.startswith('_') and not n.startswith('.'): fails.append(f'ROOT STRAY   {n}  -> file it in its topic folder or the inbox')
groups = collections.defaultdict(list)
for p in files:
    r, n = rel(p), os.path.basename(p)
    if JUNK.search(n): fails.append(f'JUNK         {r}'); continue
    stem, ext = os.path.splitext(n)
    if r in allow: continue
    groups[(os.path.dirname(p), norm(stem), ext.lower())].append(p)
    if since and os.path.getmtime(p) >= since and VER.search(stem) and 'sent to' not in stem.lower():
        fails.append(f'VERSION NAME {r}  -> the current file takes a plain name; history goes to _archive')
    top = r.split('/')[0]
    if top.lower() == 'print' and r.count('/') >= 1:
        if r.count('/') == 1: fails.append(f'PRINT ROOT   {r}  -> print files go in an event or topic subfolder')
        elif ext.lower() not in PRINT_OK: fails.append(f'PRINT SOURCE {r}  -> the source lives in its topic folder; print holds the print ready file')
    if (top.lower().startswith('00 inbox') or top.lower() == 'claude outputs') and r.count('/') == 1 and time.time() - os.path.getmtime(p) > 7 * 86400:
        warns.append(f'INBOX AGE    {r}  -> file it (older than 7 days)')
for (d, s, e), ps in groups.items():
    if len(ps) > 1 and any(VER.search(os.path.splitext(os.path.basename(x))[0]) or DATE.search(os.path.basename(x)) for x in ps):
        fails.append('VERSIONS     ' + (rel(d) if rel(d) != '.' else '(root)') + ': ' + ' | '.join(sorted(os.path.basename(x) for x in ps)) + '  -> keep the current one, older to _archive')
bysize = collections.defaultdict(list)
for p in files:
    try:
        if os.path.getsize(p) > 1024: bysize[os.path.getsize(p)].append(p)
    except OSError: pass
byhash = collections.defaultdict(list)
for s, ps in bysize.items():
    if len(ps) > 1:
        for p in ps:
            with open(p, 'rb') as fh: byhash[hashlib.md5(fh.read()).hexdigest()].append(p)
for h, ps in byhash.items():
    live = [p for p in ps if not is_copy_ok(rel(p)) and rel(p) not in allow]
    if len(live) >= 2:
        line = ' == '.join(rel(p) for p in live)
        if all(p.endswith(('.py', '.js', '.mjs')) for p in live): warns.append('CODE COPY    ' + line + '  -> one shared copy when convenient')
        else: fails.append('DUPLICATE    ' + line + '  -> one home per file')
for dp, dn, fn in os.walk(ROOT):
    if '.git' in dn:
        r = rel(dp)
        if any(dp.startswith(t) or t.startswith(dp) for t in targets):
            try:
                out = subprocess.run(['git', '-C', dp, 'status', '--porcelain'], capture_output=True, text=True, timeout=60).stdout
                n = len([l for l in out.splitlines() if l.strip()])
                if n: warns.append(f'UNCOMMITTED  {r}: {n} changed files  -> commit the revision in git')
            except Exception: pass
        dn[:] = []
    else:
        dn[:] = [d for d in dn if not d.startswith('.') and d not in ('node_modules', '_archive')]
for l in fails: print('FAIL ' + l)
for l in warns: print('WARN ' + l)
print(f'\n{len(fails)} violations, {len(warns)} warnings, {len(files)} files checked')
sys.exit(1 if fails else 0)
