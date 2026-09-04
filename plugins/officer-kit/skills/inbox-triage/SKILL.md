---
name: inbox-triage
description: >
  This skill should be used when the user says "triage my inbox", "what needs a reply",
  "clean up my email", "what did I miss", "draft replies", "go through my email",
  or wants a pass over Gmail or another connected mailbox.
metadata:
  version: "0.1.0"
---

# Inbox Triage

Find what matters in the mailbox, draft the replies, and never send anything.

## Requires

A connected email account (Gmail in the workshop; Outlook at a unit if the command allows it). Personal accounts only. If the connector is not present, say what to connect and stop.

## Sequence

**1. Scope.** Default to the last seven days, unread plus anything with a question mark or a deadline in it. Ask only if the user wants a different window.

**2. Sort into four buckets.** Needs a reply from me. Needs an action but no reply. Read and file. Ignore or unsubscribe. Present as four short lists, sender and one line gist each. Cap each list at ten; say "and N more" beyond that.

**3. Draft replies** for the first bucket. Match the user's rules file tone if one exists; otherwise brief and courteous. One draft per thread, saved as a Gmail draft when the connector allows, otherwise shown inline. Never send.

**4. Actions.** For the second bucket, offer to create calendar entries or a task list. Do it only on a go.

**5. Housekeeping.** Offer labels or archiving for bucket three and unsubscribes for bucket four. Do nothing destructive without a go. Never delete.

## Rules

- Drafts only. State this once at the start: "I'll draft, you send."
- Do not summarize anything that looks like it came from a .mil address or carries a marking; flag it and skip it.
- Skip the personal or sensitive stuff unless the user asks: medical, legal, financial, family. List the sender only.
- Weekly cadence suggestion: run this Sunday evening alongside `week-ahead`.
