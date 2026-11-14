#!/usr/bin/env python3
"""Apply an approved triage manifest (Officer Kit, folder-triage). Moves only; never deletes, never overwrites.
Usage: python apply_moves.py <working folder> <manifest.csv>          dry run: prints what would move
       python apply_moves.py <working folder> <manifest.csv> --go     moves, writes move_log.csv beside the manifest
       python apply_moves.py <working folder> --undo <move_log.csv>   moves every logged file back
Rows with action ARCHIVE, RENAME, or MOVE are applied. DECIDE rows are skipped until the user changes them."""
import os, sys, csv
args = sys.argv[1:]; ROOT = os.path.abspath(args[0])
def free(dst):
    if not os.path.exists(dst): return dst
    b, e = os.path.splitext(dst); i = 2
    while os.path.exists(f'{b} ({i}){e}'): i += 1
    return f'{b} ({i}){e}'
def move(src, dst, go):
    s, d = os.path.join(ROOT, src), os.path.join(ROOT, dst)
    if not os.path.exists(s): return ('MISSING', src, dst)
    if os.path.isdir(s) and os.path.isdir(d):
        out = []
        for n in os.listdir(s): out.append(move(src + '/' + n, dst + '/' + n, go))
        if go and not os.listdir(s): os.rmdir(s)
        return ('MERGED', src, dst, out)
    d = free(d)
    if go: os.makedirs(os.path.dirname(d), exist_ok=True); os.rename(s, d)
    return ('MOVE', src, os.path.relpath(d, ROOT).replace(os.sep, '/'))
def flat(res, acc):
    if res[0] == 'MERGED':
        for x in res[3]: flat(x, acc)
    else: acc.append(res)
if '--undo' in args:
    log = args[args.index('--undo') + 1]; rows = list(csv.DictReader(open(log, encoding='utf-8')))
    n = 0
    for r in reversed(rows):
        if r['status'] == 'MOVE' and os.path.exists(os.path.join(ROOT, r['to'])) and not os.path.exists(os.path.join(ROOT, r['from'])):
            os.makedirs(os.path.dirname(os.path.join(ROOT, r['from'])), exist_ok=True)
            os.rename(os.path.join(ROOT, r['to']), os.path.join(ROOT, r['from'])); n += 1
    print(f'undo: {n} files moved back'); sys.exit(0)
man = args[1]; go = '--go' in args
rows = list(csv.DictReader(open(man, encoding='utf-8')))
rows.sort(key=lambda r: r['action'] != 'RENAME')
acc, skipped = [], 0
for r in rows:
    if r['action'] not in ('ARCHIVE', 'RENAME', 'MOVE'): skipped += 1; continue
    flat(move(r['from'], r['to'], go), acc)
moved = [a for a in acc if a[0] == 'MOVE']; missing = [a for a in acc if a[0] == 'MISSING']
if go:
    w = csv.writer(open(os.path.join(os.path.dirname(os.path.abspath(man)), 'move_log.csv'), 'w', newline='', encoding='utf-8'))
    w.writerow(['status', 'from', 'to']); [w.writerow(a) for a in acc]
print(('MOVED ' if go else 'DRY RUN, would move ') + f'{len(moved)} files; {len(missing)} missing; {skipped} rows left for a decision')
for a in missing: print('  missing: ' + a[1])
