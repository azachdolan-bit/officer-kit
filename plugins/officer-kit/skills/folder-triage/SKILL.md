---
name: folder-triage
description: >
  This skill should be used when the user says "triage this folder", "organize my folder",
  "clean up this folder", "what's in here", "inventory this", "propose a structure",
  "sort these files", or has just linked a folder in Cowork and wants it organized.
metadata:
  version: "0.1.0"
---

# Folder Triage

Turn a messy linked folder into a structure the user can find things in, without losing or altering originals.

## Sequence

Run the `security-check` folder scan first if the folder has not been checked this session. Stop if anything is red.

**1. Inventory.** List every file with type, size, and date. Group by obvious theme. Report in one table, then a two line read: what this folder is, and the biggest mess in it.

**2. Propose.** Offer one structure, not three. Default shape for a student or platoon folder:

```
00_Inbox            (new stuff lands here, gets sorted weekly)
01_Admin            (counselings, rosters scrubbed, trackers)
02_Training         (schedules, plans, ranges)
03_Academics        (lesson packets, study guides, quizzes)
04_Reference        (doctrine, orders, SOPs, published only)
05_Personal         (PT, finances, life admin)
99_Archive          (done, keep for record)
```

Adjust names to what is actually in the folder. Show which files go where. Ask for a go before moving anything.

**3. Execute.** Move files into the structure. Rename only when the name is useless ("Document (3).docx"). Naming convention: `YYYY-MM-DD_topic_version.ext`. Never delete. Anything the user did not decide on goes to `00_Inbox`.

**4. Rollup.** Write `README.md` at the folder root: what is here, the structure, the naming rule, and a "last triaged" date. Keep it under 150 words.

## Thinking (tier: running)

**Running estimate**, because it is routine, low consequence: one line naming the standard and the assumption that matters, then work. Run the estimate before drafting and the check before delivery: the `think` skill, `references/estimate.md` and `references/check.md`, `references/tripwires.md` for the named shortcuts. State the tier and its trigger in one line so the user can raise it.



## Rules

- Originals are never edited during triage. Moves and renames only.
- If two files look like duplicates, say so and let the user decide.
- If the folder is over 200 files, do steps 1 and 2 only and propose triaging by subfolder.
- Web lane (no Cowork): ask the user to attach or paste a file list, then do steps 1 and 2 and hand them the move plan as a checklist.
