---
name: folder-triage
description: >
  This skill should be used when the user says "triage this folder", "organize my folder",
  "clean up this folder", "what's in here", "inventory this", "propose a structure",
  "sort these files", "we have a version control problem", or has just linked a folder in Cowork and wants it organized.
metadata:
  version: "0.2.0"
---

# Folder Triage

Turn a messy linked folder into a structure the user can find things in, without losing or altering originals, and leave a rule and a checker that keep it that way. A README rule alone is not enforcement; the checker is.

## Kit standards

Read `STANDARDS.md` at the root of this plugin (`../../STANDARDS.md` from this skill's folder) before producing anything. Its twelve standards apply to every product; where the user's rules file or an override says otherwise, say so once and do it the user's way.

## Sequence

Run the `security-check` folder scan first if the folder has not been checked this session. Stop if anything is red.

**1. Inventory.** `python3 scripts/triage_scan.py <folder>` writes `_build/triage/inventory.csv` and `manifest.csv` and moves nothing. Report one table: file count and size by top folder, then the problems with counts and sizes: older versions beside current ones, exact copies (by hash), dead file folders (`_to_delete`, `_old`, `Archive`, `Backups`), junk, a flat print folder, an inbox that holds copies, code versioned by file name instead of git. Then a two line read: what this folder is, and the habit that made the mess.

**2. Propose.** One structure, not three. If scripts or the rules file hardcode the top level folder names, keep them and say how many files would break. Default shape for a new folder:

```
00 Inbox            (files not yet sorted; emptied every Sunday)
01 Admin            (counselings, rosters scrubbed, trackers)
02 Training         (schedules, plans, ranges; one folder per event)
03 Academics        (lesson packets, study guides, quizzes)
04 Reference        (doctrine, orders, SOPs, published only; never archived)
05 Personal         (PT, finances, life admin)
print               (print ready files in event or topic subfolders)
_build              (folder_check.py and other machinery)
```

Ask the user only what changes the moves: which copy is the source of truth when two folders drifted, which builds to keep, which of several variants they printed. Save the plan as a file and ask for a go before moving anything.

**3. Execute.** `python3 scripts/apply_moves.py <folder> _build/triage/manifest.csv` is a dry run; read its count to the user. Then `--go`, which moves, never overwrites, never deletes, and writes `move_log.csv`; `--undo move_log.csv` reverses it. DECIDE rows are skipped until the user picks a keeper. Leave alone: git repos (commit their uncommitted work instead, as a revision), issued sources in Reference, sent records, and anything the user did not decide on (it goes to `00 Inbox`). Rename only when a name is useless ("Document (3).docx").

**4. Rule.** Write the Folder discipline block from `rules-file/references/template.md` into the rules file (show the diff). Copy `scripts/folder_check.py` to `_build/` and write `_build/folder_check_allow.txt` with `since: <today>`, a `root:` line per top level entry, `skip:` lines for repos and machinery folders, and `copy:` lines for exports and sent records.

A top level `Claude outputs` folder is where the desktop app drops a copy of every file sent to chat; it is not a second inbox. Copies there are not violations; it is emptied with `00 Inbox`.

**5. Verify.** `python3 _build/folder_check.py` exits 0 on the whole folder. A failure is fixed or, if the user says two files are different products, listed in the allow file.

**6. Rollup.** Write `README.md` at the folder root: what is here, the structure, the rule in three lines, the check command, and a "last triaged" date. Under 150 words. List every file written and the move log path.

## Naming and history

- The current file takes a plain name for what it is: `Defense Order.docx`. No draft, rev, v, iter, final, copy, or (1) in a current name.
- A date goes in a name only when it is part of what the file is (an event, a weather window, a version sent to someone), written (DD Mon YY).
- Before a file is overwritten with a new version, the old one moves to `_archive` in the same folder with its version and date appended: `_archive/Defense Order (draft 8, 2 Oct 26).docx`.
- One archive name only: `_archive`. Every `_to_delete`, `_superseded`, `_old`, `Archive`, or `Backups` folder is renamed `_archive`.
- Code and apps version in git, not in file names; a builds folder holds only the current build.

## Rules

- Originals are never edited during triage. Moves and renames only.
- Claude never deletes. The user empties an `_archive` when its event or phase closes.
- Exact copies are found by hash, not by name. Where the keeper is a judgment call, the row is DECIDE and the user picks.
- Folder size is not a reason to stop at a proposal. Over 200 files, the manifest, dry run, and move log carry the work; ask once, move once.
- Web lane (no Cowork): ask the user to attach or paste a file list, then do steps 1 and 2 and hand them the move plan as a checklist.
