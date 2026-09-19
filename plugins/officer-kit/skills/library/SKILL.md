---
name: library
description: >
  Walks the user through building the reference library the kit's tools cite from: what a
  library is and why the tools need one, three ways to build it (a starter set of manuals by
  hand in ten minutes, the full Marine Corps publications library with one command, or their
  own unit's documents), which publications each module needs, how to get them onto the
  computer, and how to check what is there. Use when the user says "build my library", "set up
  my reference folder", "download the manuals", "which pubs do I need", "where do I get the
  awards manual", "the tool says the source is missing", or during first run after the rules
  file.
metadata:
  version: "0.1.0"
---

# Library

Claude only knows what the user gives it. Every tool in this kit works from sources in the user's folder and cites them; none of them fill gaps from general knowledge. So a user with no library has tools that can format a letter but cannot check it against the manual, and an awards tool that cannot verify the criteria. This skill fixes that in ten minutes for most people.

## The rule every tool follows

Read the order from the user's library first. `scripts/find_order.py <number>` searches the Library path and Reference folder named in the rules file and reports FOUND with the file, or NOT IN THE LIBRARY with the roots searched. Only after a NOT IN THE LIBRARY does any tool read a publication from the web, and then it says which publication came from the web. When the text of a page is a figure, `find_order.py <number> --page N --png out` renders it so it can be read as an image. `--grep <regex>` finds a paragraph. No tool cites a web copy of an order that is on disk, and no tool ships a caution about a figure that the library could settle.

## Say this once

"Your library is the set of manuals, orders, and handouts the tools are allowed to cite. It lives in the Reference folder inside your working folder. Nothing outside it is used as an authority. Four ways to build it; most people take the zip, add their own documents, and never need the rest."

## Step 1. Which modules do they use?

Read the rules file or ask. The starter set is per module; do not push publications they will not use.

## Step 2. Choose how to build it

| Option | Good for | Time | What happens |
|---|---|---|---|
| **0. Starter library zip** (fastest) | everyone | 2 minutes | Download `Officer-Kit-Starter-Library.zip` from the kit's releases page (https://github.com/azachdolan-bit/officer-kit/releases/latest) and unzip it into the working folder. It drops fifteen public publications into `Reference/`: MCDP 1, 1-0 and 7, MCRP 3-10A.2, 3-10A.3 and 3-10A.4, MCWP 3-01, MCTP 3-30A, MCO 1610.7B, 1650.19J, 5100.29C, 5215.1K, 5354.1G and 1616.1, and NAVMC 5239.1, with a README that names each one's marines.mil source page. |
| **A. Starter set by hand** | everyone | 10 minutes | The user downloads the handful of manuals their modules cite from marines.mil into `Reference/`. No code, no install. |
| **B. Full publications library** | anyone who wants "what does the order say about..." answers across every MCO, MCBul, MARADMIN, and doctrine pub | one command, then 30 to 90 minutes unattended | The companion `marine-regs` plugin downloads the whole library from marines.mil and builds a search index. Resumable; re-run to refresh. |
| **C. Your own documents** | everyone, always | as you go | Unit SOPs, school handouts you were issued, orders you received, your boss's guidance. These go in `Reference/` too and outrank the manual where the unit says so. |

A and C together are enough for every tool in the kit. B adds regulation search and, for anyone who has it, means `find_order.py` finds almost any MCO, MCBul, NAVMC, MARADMIN, or doctrine publication on disk. Record the library's path in the rules file under `Library path:` so every tool and every session reads from it.

## Step 3A. The starter set, by hand

Give the user only the rows for their modules. Walk them through the first one, then let them do the rest.

| Module | Publication | Where | Save as |
|---|---|---|---|
| Correspondence | SECNAV M-5216.5, Department of the Navy Correspondence Manual | secnav.navy.mil, DONI, SECNAV Manuals | `Reference/SECNAV M-5216.5 Correspondence Manual.pdf` |
| Correspondence | The correspondence handout your school issued, if any | your course materials | `Reference/<its title>.pdf` |
| Admin | MCO 1610.7, Performance Evaluation System | marines.mil MCPEL, search "1610.7" | `Reference/MCO 1610.7 PES Manual.pdf` |
| Admin | SECNAV M-1650.1, Navy and Marine Corps Awards Manual | marines.mil MCPEL, search "1650.1" | `Reference/SECNAV M-1650.1 Awards Manual.pdf` |
| Admin | MCO 1500.58, Marine Leader Development | marines.mil MCPEL, search "1500.58" | `Reference/MCO 1500.58 Marine Leader Development.pdf` |
| Admin | The fitness report and awards handouts your school issued, if any | your course materials | `Reference/<its title>.pdf` |
| Planning | MCDP 1, Warfighting | marines.mil MCPEL, search "MCDP 1" | `Reference/MCDP 1 Warfighting.pdf` |
| Planning | MCDP 1-0, Marine Corps Operations | marines.mil MCPEL, search "MCDP 1-0" | `Reference/MCDP 1-0 Marine Corps Operations.pdf` |
| Planning | MCTP 3-10A, Infantry Company Operations | marines.mil MCPEL, search "3-10A" | `Reference/MCTP 3-10A Infantry Company Operations.pdf` |
| Planning | The tactical planning handouts your school issued | your course materials | `Reference/<its title>.pdf` |
| Training and teaching | MCDP 7, Learning | marines.mil MCPEL, search "MCDP 7" | `Reference/MCDP 7 Learning.pdf` |
| Training and teaching | The handouts and lessons you are studying | your course materials | `Training/` (captured with `capture-source`) |

**How to download from MCPEL, said once:** open `https://www.marines.mil/News/Publications/MCPEL/Search/<what you are looking for>/` in a browser, for example `.../MCPEL/Search/1610.7/`. Click the publication, then the download link on its page. Save the PDF into your Reference folder with the name in the table. If a search returns several versions, take the one with the latest date or the highest change number ("w/ CH 1-3").

**The DONI site** (secnav.navy.mil/doni) holds SECNAV instructions and manuals. Open SECNAV Manuals, find 5216.5, download.

If the user has a browser connector attached and directs it, Claude can open the search page for them; the download itself is theirs to click, and it lands in their Downloads folder, so the last step is moving it into Reference.

## Step 3B. The full library

Tell them plainly what it is: a companion plugin, `marine-regs`, that crawls marines.mil, saves every publication into `C:\Marine_Corps_Regulations` (or a folder they choose), and builds a searchable index so "what's the policy on..." questions come back with the verbatim paragraph and citation. It needs Python on the computer and about an hour unattended. Then:

1. Install `marine-regs` from the same place they installed Officer Kit.
2. Say "set up the regulations library." The plugin checks Python, installs what it needs, downloads, and indexes. It reports progress and can be re-run later to pick up new orders.
3. Afterwards, the Officer Kit tools still read from `Reference/` for their governing manual; regulation questions go to `marine-regs`.

Do not oversell it. A platoon commander who writes two letters a month does not need it. An adjutant or a company XO probably does.

## Step 3C. Your own documents

Anything the unit or the school issued that the tools should treat as authority: SOPs, the CO's guidance, orders received, school handouts. Save them in `Reference/` with their real titles. Remind the user of the rule: school and unit documents outrank the parent manual where they differ, and the newer one wins. Nothing from a .mil system they would not email to a personal address.

## Step 4. Check what is there

Run `python3 scripts/library_check.py "<working folder>/Reference"` (or list the folder if the script is unavailable). It reports every PDF and document found, its size and page count, and which starter set publications for the user's modules are present or missing. Show the user the table. A missing publication is not an error; the tool that needs it will ask when the time comes.

## Step 5. Keep it current

- Publications change. When a tool cites a manual, it names the edition it read. If the user hears a new edition is out, they replace the file; nothing else changes.
- Option B users re-run the setup command; it only downloads what is new.

## Rules

- Never download or copy anything from a .mil system on the user's behalf. Public marines.mil and secnav.navy.mil pages are fine; anything behind a CAC login is not.
- Never tell a user a publication is current without checking the date on the file they have.
- Never pad a missing source from general knowledge. A missing manual means the tool asks for it.

## Utility script

- `scripts/library_check.py <Reference folder> [--modules correspondence,admin,planning,training]`: inventory and starter set coverage report.

## Utility scripts

- `scripts/library_check.py`: coverage report of the starter set against the Reference folder.
- `scripts/find_order.py <number> [--text | --grep <regex> | --page N --png <out>]`: finds a publication in the library and Reference, extracts its text, or renders a page as an image. Exit 1 with the roots searched when not found.
