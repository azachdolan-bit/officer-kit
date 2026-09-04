# Officer Kit

A suite of tools that helps a Marine officer do the things the job asks every week: read and review orders, write awards and fitness reports, manage a reporting senior profile, plan, analyze, teach, and correspond to the standard. Built by an officer, for officers, and designed to get better the longer you use it.

Personal initiative. Not an official USMC product. Personal accounts and unclassified data only.

## What you are installing

One plugin file. Installing it gives Claude:

- **Skills**: things Claude knows how to do to a standard, such as draft a naval letter, review an order, build a quiz from a handout, write an award citation to the manual.
- **Reviewers**: separate checks that run before anything you sign leaves your desk. They are blind to how the draft was written; they only see the draft and the sources.

The plugin contains no personal information and no unit content. Everything about you lives in a folder on your own computer, which you control, and in a short rules file you write at whatever level of detail you want. Uninstalling the plugin removes the tools and touches nothing of yours.

## First run: ten minutes

Say **"start the officer kit"** and Claude walks you through it one step at a time:

1. Confirm the plugin is installed.
2. Make a working folder on your computer. Claude proposes a structure (Correspondence, Admin, Planning, Training, Reference, Print) and adjusts it to your job.
3. Connect that folder in Cowork so Claude can read and save there.
4. Write your rules file. Every question is optional. Light, Standard, or Full depth; you decide how much of yourself to record.
5. Run one real task from your own work so you see the difference.

That is the whole setup. From then on, you describe what you need in plain language and the right tool fires.

## The modules

Use the ones that match your job. Ignore the rest.

| Module | What it does for you | Status |
|---|---|---|
| **Correspondence** | Naval letters, memos, requests, endorsements, built to the correspondence manual and measured on the page before they go out | Available |
| **Admin** | Award recommendations (summary of action and citation to the awards manual), fitness report drafts from your notes (to the PES manual), reporting senior profile management, counselings, weekly updates, after action reports, training schedules | Building |
| **Planning** | Read and analyze an order (METT-TC, contradictions, map and grid checks), critique a five paragraph order, planning playbooks, call for fire | Partly available |
| **Training and teaching** | Study guides, interactive walkthroughs, quizzes, drills, print cards, and briefs from issued material only | Partly available |
| **Verify** | The reviewers and the gate stack: significance, evidence, document, visual, source fidelity | Available |
| **Share and improve** | Build your own skill, share a method without sharing content, the lessons queue, taking the kit to your next unit | Partly available |

`MODULES.md` lists every tool in every module, what it needs from you, and what it produces.

## How it gets better

Every correction you make, and every defect a reviewer catches, is written to a lessons queue. On review, an accepted lesson becomes a change to the tool that should have prevented it, the tool's tests run, and the change ships to everyone who installed from this repo. Git keeps every version, so a bad change rolls back in one step.

## Install

**From this repo, so you get updates:** in Cowork, open Customize, then Plugins, then Add marketplace, and enter `azachdolan-bit/officer-kit`. Install Officer Kit. Click Update on the marketplace when a new version is announced.

**From a file:** upload `officer-kit.plugin` on the Plugins page. No automatic updates; reinstall to upgrade.

## Contributing a lesson

Append an entry to `LEARNINGS.md` in the format at the top of that file: what happened and what the tool should do differently. Do not edit a tool directly; the review step exists so a bad lesson cannot quietly weaken a check.

## Repo layout

```
.claude-plugin/marketplace.json     this repo is a plugin marketplace
plugins/officer-kit/                the plugin (skills, agents)
MODULES.md                          every tool by module, built and planned
LEARNINGS.md                        lessons waiting for review
evals/                              tests per tool
scripts/package.sh                  builds the installable .plugin file
CHANGELOG.md                        what changed in each version
```
