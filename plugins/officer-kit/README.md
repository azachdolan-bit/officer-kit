# Officer Kit

A starter kit for new Marine officers learning the full Claude toolset. Built for The Basic School, designed to travel to the fleet.

Personal initiative. Not an official TBS or USMC product. Personal accounts and unclassified data only.

## The rule

Personal account, personal data, personal device. Nothing CUI, PII, FOUO, or from a .mil system. When unsure, treat it as red. The `security-check` skill has the full green / yellow / red card.

## Start here

Say **"start the field kit."** It picks your first task, then builds your rules file. Your rules file is the one thing in this kit that makes every future task better. Do not skip it.

## Skills

| Say this | What happens | Teaches |
|----------|--------------|---------|
| "start the field kit" | Orientation and the seven day plan | The whole map |
| "is this safe to share" / "check this folder" | Green / yellow / red card, folder scan before linking | Security |
| "build my rules file" | Interview at the depth you choose (Light, Standard, Full), then a CLAUDE.md; Full adds the lines that print on a letter you sign | Rules, memory, privacy |
| "draft a naval letter" | Letter built on the 13.8 pt grid from your rules file identity, then Gate 2 measured on the rendered PDF | Correspondence |
| "QC this before I sign" | The gate stack by product type, run by blind reviewers until clean | Verification |
| "capture this lesson" / "transcribe these photos" | Complete capture saved the same session, completeness check, read back gate for photos | Sources first |
| "triage this folder" | Inventory, structure, move, rollup | Cowork and linked folders |
| "make a study guide" / "quiz me" | Lesson packet to guide, quiz, flashcards | Files in, files out |
| "critique my order" | Five paragraph order review | Structured feedback |
| "triage my inbox" | Four buckets, drafted replies, never sends | Connectors |
| "week ahead" | One screen brief, then make it recurring | Scheduled tasks |
| "build a skill" | Interview, then a working skill for your repeat task | Skills and plugins |
| "fleet transition" | Day one and week one checklist for your first unit | Taking it with you |

## Prompt library

Study: "Turn this packet into a one page guide and a 20 question quiz." "Quiz me on this one question at a time." "What in this lesson gets tested by numbers?"

Admin: "Inventory this folder and tell me what's in it." "Draft a weekly update from these bullets, BLUF first, under 200 words." "Turn these range notes into an after action: what happened, what worked, what to fix." "Build a training schedule from this list of events, Monday to Friday, with prep items."

Email and calendar: "What needs a reply this week? Draft them, don't send." "What does my week look like and where are the conflicts?" "Find the last three docs I edited and summarize each in two lines."

Browser: "Pull the schedule off this page into a table." "Compare these two pages and tell me the differences."

Voice: Brief it like you would brief a Marine. Situation, what you need, format, deadline. Then let it work.

Personal: "Build a four week PT plan from this baseline." "Sort my receipts by month." "Draft the message to my landlord about the lease."

## Troubleshooting

**Claude can't see my files.** In Cowork, the folder has to be linked in the desktop app first. In the web app, attach the file to the chat. Claude only sees what you give it.

**It didn't follow my rules.** Check the rules file is named `CLAUDE.md` and sits at the top of the linked folder. Restart the session after adding it.

**A skill didn't trigger.** Use one of the phrases in the table above, or name it: "run folder-triage."

**The connector isn't there.** Connect it in the app settings on a personal account. Never a .mil account.

**It made something up.** It will, occasionally. That is why everything is a draft. Ask "where did that number come from?" and it will tell you or admit it doesn't know. Never paste a Claude reference or citation into anything without checking it.

**It sent something.** It should not have. Every skill in this kit is draft only. If it did, review your connector permissions and tell the facilitator.

**I'm on the free tier.** Everything here works by attaching files instead of linking a folder. You lose the folder automation, you keep everything else.

## Reviewers (v0.2)

Five subagents the skills call for verification. They are blind: each gets the draft and the sources, never the drafting session's reasoning.

| Agent | Gate | Returns |
|-------|------|---------|
| `significance-reviewer` | Gate 0 on findings | KILL / DEMOTE / SURVIVES per finding, with baseline and consequence |
| `evidence-reviewer` | Gate 1 on any claims against sources | SUBSTANTIVE / THIN / REACHING / WRONG per claim, plus what the draft missed |
| `visual-reviewer` | Gate 3 on anything rendered | SHIP / NO SHIP with an ordered defect list |
| `source-fidelity-reviewer` | teaching products and shared builders | PASS / FAIL on sourcing, coverage, quiz traceability, zero content |
| `researcher` | wide read only research | a structured table, nothing invented |

## Sharing

Send the `.plugin` file to another Marine. They install it the same way you did. Encourage them to run `build-a-skill` and send you what they made.

## Version

0.2.0. Skeleton of the consolidated kit: v0.1.0 skills plus the five reviewer agents. Roadmap and changelog in the repo. Feedback to the facilitator.
