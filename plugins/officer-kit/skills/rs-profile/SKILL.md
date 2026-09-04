---
name: rs-profile
description: >
  Helps a reporting senior manage their fitness report profile per MCO 1610.7B chapter 8: keeps
  a private ledger of the reports they have written by grade, computes each report's fitness
  report average, the RS average, high, and low per grade, and the relative value of any report
  or proposed set of marks on the 80 to 100 scale, and flags a profile that is compressing.
  Use when the user says "my profile", "RS profile", "relative value", "where would these marks
  land", "am I marking consistently", "what does this report do to my average", or "MBS".
metadata:
  version: "0.1.0"
---

# Reporting senior profile

The profile is a record of the RS's marking philosophy, and the manual is blunt about the two ways to damage it: marking everyone the same, so no report carries relative value, and changing philosophy midstream, which silently re values every report already written. This tool exists so an RS can see the consequence of a set of marks before signing, not so they can "write to a profile." The manual says attribute comparison is a check on one's own work, not a target.

Read `references/pes-manual-chapter-8-extract.md` once per session for the manual's own words on the profile, the averaging rule, and relative value.

## What the manual gives, and what this tool computes

- Fitness report average: each observed attribute A=1 through G=7; H (not observed) excluded; sum divided by the number of observed attributes, rounded to the nearest hundredth.
- The profile is per grade and excludes academic, EN, and N/O reports.
- The RS average of all reports on Marines of that grade is a relative value of 90. The RS high is a relative value of 100. Relative value is shown on an 80 to 100 scale: 93.34 to 100 upper third, 86.67 to 93.33 middle third, 80 to 86.66 bottom third; anything below 80 shows as 80.
- The manual states the two anchors and the scale, not a formula. This tool interpolates linearly between the anchors (relative value = 90 + 10 × (report average minus RS average) divided by (RS high minus RS average)) and says so in every output. Relative value is a boardroom metric; the authoritative number is the one on the Marine's MBS.

## The ledger

A CSV the user keeps in their own folder, never in the plugin, at `Admin/Fitreps/rs_profile.csv`:

```
grade,label,occasion,date,D1,D2,E1,E2,E3,E4,F1,F2,F3,F4,F5,G1,G2,H1
Capt,MRO-07,AN,2026-05-31,D,D,C,D,C,D,C,C,D,C,D,C,D,H
```

`label` is whatever the user chooses; it need not be a name. The 14 columns are the attributes in report order (Section D performance and proficiency; E courage, effectiveness under stress, initiative; F leading, developing, setting the example, ensuring well being, communication; G PME, decision making, judgment; H evaluations). Letters A to G, or H for not observed. Reports that do not belong in the profile (academic, EN, N/O) are left out of the ledger or marked with occasion `AC`, `EN`, or `NO`, which the script skips.

The RS can also view the official profile on the My OMPF tab on MOL; the ledger is a working copy for what if questions, not a substitute.

## Workflow

```
Profile question:
- [ ] 1. Ledger located or created (Admin/Fitreps/rs_profile.csv); grades present listed
- [ ] 2. python3 scripts/rs_profile.py rs_profile.csv --grade <grade> for the current picture
- [ ] 3. For a proposed report: --propose D,D,C,... shows its average, relative value, and third, and the new RS average if it were added
- [ ] 4. Compression check read: share of reports within 0.10 of the RS average, and the spread high minus low
- [ ] 5. Findings stated plainly; no recommendation to change marks to hit a number
```

## What to say and not say

- Say where a proposed report lands and what it does to the average. Do not suggest moving marks to land somewhere else; the manual forbids marking to a profile.
- If the profile is small (fewer than five reports at that grade), say that every new report moves the anchors a lot and that a follow on report can be understated, which is exactly what the manual tells the RS to explain in Section I.
- If most reports sit within a tenth of the average, say the profile is compressing and quote the manual's line about reports that lack relative value.
- Never store names, EDIPIs, or SSNs in the ledger. A label the user picks is enough.

## Utility script

- `scripts/rs_profile.py <ledger.csv> [--grade Capt] [--propose D,D,C,D,C,D,C,C,D,C,D,C,D,H]`: prints each report's average and relative value, the RS average, high, low, count, compression measures, and the proposed report's placement. Exit 0 always.
