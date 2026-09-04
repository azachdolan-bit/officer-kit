# Officer Kit

A Marine officer's extension of himself. Built at The Basic School, designed to travel to the fleet.

Personal initiative. Not an official TBS or USMC product. Personal accounts and unclassified data only. The plugin carries method only: no course content, no findings, no personal identity. Those live in each user's own working folder and rules file.

## What is in this repo

```
.claude-plugin/marketplace.json     this repo is a plugin marketplace
plugins/officer-kit/           the plugin (skills, agents)
ROADMAP.md                          every planned skill as a build spec, hooks, sprints
LEARNINGS.md                        candidate lessons waiting for review
evals/                              golden cases per skill
scripts/package.sh                  builds the installable .plugin file
CHANGELOG.md
```

## The six functions

The plugin is organized around what an officer does every week, not around any one school or billet.

| Function | Skills | Reviewer |
|---|---|---|
| Produce from sources | capture-source, study-guide, print-card, topic-brief | source-fidelity-reviewer |
| Verify before signing | qc-gates | significance-reviewer, evidence-reviewer, visual-reviewer |
| Correspond to the standard | naval-letter, discrepancy-report, evidence-deck | all four gates |
| Plan and assess | order-critique, order-analysis, tactical-planning, call-for-fire, lo-audit | evidence-reviewer |
| Teach | walkthrough, quiz-builder, drill-builder | source-fidelity-reviewer |
| Share and learn | field-kit-start, security-check, rules-file, build-a-skill, fleet-transition, folder-triage, inbox-triage, week-ahead, share-method, peer-eval, aar, inspect | |

`ROADMAP.md` says which are built and which are planned.

## How it gets better

1. `aar` captures corrections, confirmations, gate failures, and build defects into `LEARNINGS.md` at the end of a task. It never edits a skill.
2. `inspect` turns the queue into diffs against the exact skill lines. A person approves or rejects. Anything that would soften a gate, reduce sourcing, or suppress a reviewer is refused.
3. The skill's evals run. A change that fails does not ship.
4. Version bump, commit with the why, push. Anyone who installed from this marketplace clicks Update. Git is the rollback.

## Install

**From this repo as a marketplace (gets updates):** in Cowork, Customize, Plugins, Add marketplace, enter `azachdolan-bit/officer-kit`, then install Officer Kit. Click Update on the marketplace to pull new versions.

**From a file:** run `scripts/package.sh` and upload `dist/officer-kit.plugin` on the Plugins page. No updates; reinstall to upgrade.

## Contributing a lesson

Append an entry to `LEARNINGS.md` in the format at the top of that file. Say what happened and what the skill should do differently. Do not edit a skill directly; the review step exists so a bad lesson cannot quietly weaken a gate.
