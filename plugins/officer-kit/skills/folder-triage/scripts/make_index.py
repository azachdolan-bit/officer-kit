#!/usr/bin/env python3
"""Catalog of a working folder (Officer Kit, folder-triage). Copy to <working folder>/_build/.
Usage: python make_index.py                    rebuild INDEX.md (root) and _build/index.tsv
       python make_index.py --find <words>      search the catalog; every word must match name, path, or title
       python make_index.py --root <folder> ... run against another working folder
One line per product a person opens: name, path, type, modified, open or closed, title (first heading of a
.md, first text of a .docx or .pptx). Left out: underscore and dot folders, git internals, node_modules,
code files, and every folder named by a skip: or noindex: line in _build/folder_check_allow.txt.
closed: <folder> lines mark finished events; --find lists open work first.
alias: <path> lines give the root as notes spell it (C:\\TBS); results print with the first alias."""
import os, re, sys, time, zipfile, html
args = sys.argv[1:]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if '--root' in args:
    i = args.index('--root'); ROOT = os.path.abspath(args[i + 1]); del args[i:i + 2]
TSV = os.path.join(ROOT, '_build', 'index.tsv'); MD = os.path.join(ROOT, 'INDEX.md')
CODE = {'.py', '.pyc', '.js', '.mjs', '.cjs', '.ts', '.css', '.sh', '.bat', '.ps1', '.map', '.lock', '.ini', '.db', '.log', '.tmp', '.crdownload'}
SKIPDIR = {'node_modules', '__pycache__', 'dist'}
JUNK = re.compile(r'(^\.~lock|^~\$|\.tmp$|\.bak\d*$|^Thumbs\.db$|^desktop\.ini$|^\.DS_Store$)')

def config(root):
    c = {'skip': [], 'noindex': [], 'closed': [], 'alias': []}
    p = os.path.join(root, '_build', 'folder_check_allow.txt')
    if os.path.exists(p):
        for l in open(p, encoding='utf-8'):
            l = l.strip()
            k, _, v = l.partition(':')
            if k in c and v.strip():
                v = v.strip()
                c[k].append(v if k == 'alias' else v.replace('\\', '/').strip('/'))
    return c

def under(r, prefixes): return any(r == p or r.startswith(p + '/') for p in prefixes)

def title_of(p, ext):
    try:
        if ext in ('.md', '.txt'):
            with open(p, encoding='utf-8', errors='ignore') as fh:
                for i, l in enumerate(fh):
                    if i > 40: break
                    l = l.strip()
                    if l.startswith('#'): return l.lstrip('#').strip()[:120]
                    if l and not l.startswith(('---', 'name:', 'description:')) and ext == '.txt': return l[:120]
        elif ext in ('.docx', '.pptx'):
            with zipfile.ZipFile(p) as z:
                part = 'word/document.xml' if ext == '.docx' else 'ppt/slides/slide1.xml'
                if part in z.namelist():
                    xml = z.read(part)[:400000].decode('utf-8', 'ignore')
                    tag = 'w:t' if ext == '.docx' else 'a:t'
                    words = re.findall(r'<%s(?: [^>]*)?>([^<]*)</%s>' % (tag, tag), xml)
                    t = html.unescape(' '.join(w for w in words if w.strip()))
                    return re.sub(r'\s+', ' ', t).strip()[:120]
    except Exception:
        pass
    return ''

def build(root):
    c = config(root); rows = []; cache = {}
    if os.path.exists(TSV):   # reuse titles of files that have not changed since the last build
        for l in open(TSV, encoding='utf-8').read().splitlines()[1:]:
            x = l.split('\t')
            if len(x) >= 7: cache[x[1]] = (x[6], x[5])
    for dp, dn, fn in os.walk(root):
        r = os.path.relpath(dp, root).replace(os.sep, '/'); r = '' if r == '.' else r
        keep = []
        for d in dn:
            rd = (r + '/' + d).lstrip('/')
            if d.startswith(('.', '_')) or d in SKIPDIR or under(rd, c['skip']) or under(rd, c['noindex']): continue
            keep.append(d)
        dn[:] = keep
        for f in fn:
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE or JUNK.search(f) or f.startswith('.'): continue
            rp = (r + '/' + f).lstrip('/')
            if rp == 'INDEX.md': continue
            p = os.path.join(dp, f)
            try: m = os.path.getmtime(p)
            except OSError: continue
            status = 'closed' if under(r, c['closed']) else 'open'
            key = f'{m:.3f}:{os.path.getsize(p)}'; t = cache[rp][1] if rp in cache and cache[rp][0] == key else title_of(p, ext)
            rows.append([f, rp, ext.lstrip('.'), time.strftime('%Y-%m-%d', time.localtime(m)), status, t, key])
    rows.sort(key=lambda x: (x[4] == 'closed', x[1].lower()))
    os.makedirs(os.path.dirname(TSV), exist_ok=True)
    with open(TSV, 'w', encoding='utf-8', newline='') as fh:
        fh.write('name\tpath\ttype\tmodified\tstatus\ttitle\tmtime\n')
        for x in rows: fh.write('\t'.join(v.replace('\t', ' ') for v in x) + '\n')
    a = c['alias'][0] if c['alias'] else root
    out = [f'# Catalog of {os.path.basename(root)}', '',
           f'Generated {time.strftime("%d %b %y %H%M")} by _build/make_index.py from {a}. Do not edit; run the script.',
           f'Find a file: search this page, or run `python _build/make_index.py --find <words>`, before walking the folder.',
           f'{len(rows)} products; {sum(1 for x in rows if x[4] == "closed")} in closed events.', '']
    last_status, last_dir = None, None
    for x in rows:
        if x[4] != last_status:
            out += ['', '# ' + ('Open' if x[4] == 'open' else 'Closed events'), '']; last_status = x[4]; last_dir = None
        d = os.path.dirname(x[1]) or '(root)'
        if d != last_dir: out += ['', f'## {d}', '']; last_dir = d
        out.append(f'- {x[0]}, {x[3]}' + (f'. {x[5]}' if x[5] and x[5].lower() not in x[0].lower() else ''))
    open(MD, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    return rows

def find(root, words):
    c = config(root); a = c['alias'][0] if c['alias'] else root
    sep = '\\' if '\\' in a or re.match(r'^[A-Za-z]:', a) else '/'
    if not os.path.exists(TSV): build(root)
    words = [w.lower() for w in words]; hits = []
    for l in open(TSV, encoding='utf-8').read().splitlines()[1:]:
        x = l.split('\t')
        if len(x) < 6: continue
        hay = (x[1] + ' ' + x[5]).lower()
        if all(w in hay for w in words): hits.append(x)
    for x in hits[:60]:
        print(('' if x[4] == 'open' else '[closed] ') + a.rstrip('\\/') + sep + x[1].replace('/', sep) + (f'   ({x[5][:70]})' if x[5] else ''))
    print(f'{len(hits)} match' + ('' if len(hits) == 1 else 'es') + (', first 60 shown' if len(hits) > 60 else ''))
    return hits

if __name__ == '__main__':
    if '--find' in args:
        i = args.index('--find'); hits = find(ROOT, args[i + 1:]); sys.exit(0 if hits else 1)
    t = time.time(); rows = build(ROOT)
    print(f'index: {len(rows)} products ({sum(1 for x in rows if x[4] == "closed")} closed) in {time.time() - t:.1f}s -> INDEX.md, _build/index.tsv')
