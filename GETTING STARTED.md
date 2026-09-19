# Getting started, from zero

For an officer who has never opened Claude Cowork. Thirty minutes, no technical background needed. If you already use Cowork, skip to "The five things you set up."

## What Cowork is

Claude is an assistant you talk to in plain language. **Cowork** is the version of Claude that can work with files on your computer: it can read a folder you give it, write documents into that folder, and run tools. The regular chat app cannot touch your files; Cowork can, but only the folder you connect.

## The one idea that matters

**Claude only knows what you give it.** It does not have your unit's SOP, the current awards manual, the order you received this morning, or your boss's preferences unless those things are in a folder you connected or in a file you handed it. Everything in this kit is built on that idea: the tools work from your sources, cite them, and refuse to fill gaps from general knowledge. So the setup below is mostly about giving Claude the right things to work from.

## What is safe to give it

Personal account, personal data, personal device. Nothing marked CUI, FOUO, or classified; nothing with other people's personal data (SSNs, DoD IDs, medical); nothing pulled off a .mil system you would not email to a personal address. Published doctrine and orders from marines.mil, school handouts issued to you, your own notes, and your own drafts are fine. When unsure, treat it as red and leave it out. The kit's `security-check` tool will scan a folder before you connect it.

## The five things you set up

| # | Thing | What it is | Time |
|---|---|---|---|
| 1 | **The Cowork app** | Claude's desktop app, signed in to your personal account | 5 min |
| 2 | **A working folder** | One folder on your computer that Claude can see. Everything you make lands there. | 2 min |
| 3 | **The Officer Kit plugin** | The tools. One file, installed from the Plugins page. | 2 min |
| 4 | **Your rules file** | A short file that tells Claude who you are and how you want things written. You choose how much to include. | 10 min |
| 5 | **Your library** | The manuals and orders your work is built to, saved in your folder so the tools can cite them. The starter library zip on the releases page does this in two minutes. | 2 min with the zip |

## The thirty minute path

**1. Install Cowork.** Download the Claude desktop app, sign in with a personal account. In the app, choose Cowork. Cowork works on a Pro or Max plan; on a free account you can still attach files to a chat, and the tools will work on what you attach, but you lose the folder.

**2. Make your working folder.** Anywhere you like, for example `Documents\Officer Kit`. Leave it empty; the kit will build the structure.

**3. Install the plugin.** In Cowork, open Customize, then Plugins. Either add the marketplace `azachdolan-bit/officer-kit` and install Officer Kit (you get updates), or upload the `officer-kit.plugin` file someone sent you (no updates).

**4. Connect the folder and say "start the officer kit."** Use Add folder in the Cowork sidebar to connect the folder you made. Then type "start the officer kit." Claude walks you through the rest one step at a time: it asks what most of your week is, builds the folder structure for those modules, runs the rules file interview, helps you build your library, and does one real task from your own work so you see it working.

**5. Get the starter library.** Download `Officer-Kit-Starter-Library.zip` from https://github.com/azachdolan-bit/officer-kit/releases/latest and unzip it into your working folder. Fifteen public Marine Corps publications land in `Reference/`, and the tools cite from them. Add anything your school or unit issued you to the same folder.

**6. Use it.** From then on, say what you need in plain language: "draft a letter requesting...", "write up a NAM for Sgt Smith from these bullets", "analyze this order", "make a quiz from this handout". The right tool fires, works from your sources, checks itself, and saves the result in your folder.

## Words you will see

- **Skill**: a tool. A set of instructions Claude follows the same way every time, with scripts and the standard built in.
- **Reviewer**: a separate check that runs before something you sign leaves your desk. It sees only the draft and the sources, not the reasoning.
- **Rules file** (`CLAUDE.md`): the file at the top of your folder that Claude reads at the start of every session. Who you are, how you want drafts written, what it must never do. Optional identity block for letters.
- **Library**: the manuals, orders, and handouts in your Reference folder. The tools cite from it and nothing else.
- **Module**: a group of tools for one kind of work: Correspondence, Admin, Planning, Training and teaching, Verify, Share and improve.
- **Lessons queue**: where corrections go so the tools improve. You never have to touch it.

## If something goes wrong

- **Claude cannot see my files.** The folder has to be connected in the Cowork sidebar. In the web or phone app, attach the file to the chat instead.
- **It ignored my rules.** The file must be named `CLAUDE.md` and sit at the top of the connected folder. Start a new session after adding it.
- **A tool did not fire.** Use a phrase from `MODULES.md`, or name it: "run naval-letter."
- **It made something up.** It will, occasionally. Ask "where did that come from?" It will point to the source or admit it has none. That is why nothing ships without a source and a check.
- **It sent something.** It should not have; every tool is draft only. Check your connector permissions and tell whoever gave you the kit.
