#!/usr/bin/env python3
"""Save a product the one right way (Officer Kit, folder-triage). Copy to <working folder>/_build/.
Usage: python save_product.py <file> <topic folder> [--name "Plain Name.ext"] [--version "draft 3"] [--move] [--new]
  <topic folder>  relative to the working folder: "Exercises/FEX 3", "print/WARFEX"
  --name          the plain name to save under (default: the file's own name)
  --version       how to label the copy it replaces in _archive (default: "previous")
  --move          move the file instead of copying it
  --new           allow the topic folder to be created (its parent must exist)
Does, in order: refuses a version word in the name (draft, rev, v2, final, copy, (1)); refuses the root
of the working folder, the root of print, an underscore folder, and replacing an issued source in a
Reference folder; moves the file it replaces to _archive in the same folder as
"<name> (<version>, <DD Mon YY>)<ext>"; writes the new file; rebuilds the catalog; runs folder_check
on that folder; prints SAVED and the path as notes spell it. An identical file is left alone.
Exit 0 = saved and the folder passes, 1 = refused, 2 = saved but the folder check found violations."""
import os, re, sys, shutil, hashlib, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
args = sys.argv[1:]
def opt(k, default=None):
    if k in args:
        i = args.index(k); v = args[i + 1]; del args[i:i + 2]; return v
    return default
def flag(k):
    if k in args: args.remove(k); return True
    return False
ROOT = os.path.abspath(opt('--root', ROOT)); name = opt('--name'); version = opt('--version', 'previous')
move, new = flag('--move'), flag('--new')
if len(args) != 2: print(__doc__); sys.exit(1)
src, folder = os.path.abspath(args[0]), args[1].replace('\\', '/').strip('/')
VER = re.compile(r'(?i)(?:^|[ _\-(])+(draft|rev|v|iter)[ _]?\d+(?:\.\d+)?\)?(?=$|[ _\-.)(])|\bfinal\b|\bcopy\b|\(\d\)$|\)-\d$')
alias = None
cfg = os.path.join(ROOT, '_build', 'folder_check_allow.txt')
if os.path.exists(cfg):
    for l in open(cfg, encoding='utf-8'):
        k, _, v = l.strip().partition(':')
        if k == 'alias' and v.strip() and not alias: alias = v.strip()
def show(r):
    if not alias: return os.path.join(ROOT, r)
    sep = '\\' if '\\' in alias or re.match(r'^[A-Za-z]:', alias) else '/'
    return alias.rstrip('\\/') + sep + r.replace('/', sep)
def refuse(msg): print('REFUSED  ' + msg); sys.exit(1)

name = name or os.path.basename(src); stem, ext = os.path.splitext(name)
if not os.path.isfile(src): refuse(f'no such file: {src}')
if VER.search(stem): refuse(f'"{name}" carries a version word; save it under its plain name and let the old one go to _archive (--version labels the archived copy)')
segs = folder.split('/') if folder else []
if not segs: refuse('nothing is saved at the root of the working folder; name its topic folder')
if segs[0].lower() == 'print' and len(segs) == 1: refuse('print files go in an event or topic subfolder: print/<event>')
if any(s.startswith('_') for s in segs): refuse('underscore folders hold machinery, not products')
dest_dir = os.path.join(ROOT, *segs)
if not os.path.isdir(dest_dir):
    if new and os.path.isdir(os.path.dirname(dest_dir)): os.makedirs(dest_dir)
    elif new: refuse(f'{folder}: its parent folder does not exist either')
    else: refuse(f'{folder} does not exist; check the catalog for the topic folder, or pass --new to create it')
dest = os.path.join(dest_dir, name); r = os.path.relpath(dest, ROOT).replace(os.sep, '/')
def md5(p):
    with open(p, 'rb') as fh: return hashlib.md5(fh.read()).hexdigest()
if os.path.exists(dest):
    if os.path.abspath(dest) == src or md5(dest) == md5(src):
        print(f'UNCHANGED  {show(r)}'); sys.exit(0)
    if segs[0].lower().startswith('reference'): refuse(f'{r} is an issued source; sources are never replaced or archived')
    stamp = time.strftime('%d %b %y', time.localtime(os.path.getmtime(dest)))
    arch = os.path.join(dest_dir, '_archive'); os.makedirs(arch, exist_ok=True)
    a = os.path.join(arch, f'{stem} ({version}, {stamp}){ext}'); i = 2
    while os.path.exists(a): a = os.path.join(arch, f'{stem} ({version} {i}, {stamp}){ext}'); i += 1
    os.rename(dest, a); print(f'ARCHIVED {os.path.relpath(a, ROOT).replace(os.sep, "/")}')
(shutil.move if move else shutil.copy2)(src, dest)
print(f'SAVED    {show(r)}')
code = 0
for tool, extra in (('make_index.py', []), ('folder_check.py', ['--no-index', dest_dir])):
    t = os.path.join(HERE, tool)
    if os.path.exists(t):
        out = subprocess.run([sys.executable, t, '--root', ROOT] + extra, capture_output=True, text=True)
        lines = [l for l in out.stdout.splitlines() if l.strip()]
        if tool == 'folder_check.py':
            for l in lines[:-1]: print('  ' + l)
            if out.returncode: code = 2
        if lines: print('  ' + lines[-1])
sys.exit(code)
