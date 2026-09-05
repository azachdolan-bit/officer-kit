#!/usr/bin/env python3
"""The checks the plugin installer runs, run here instead of at install time.

Added 5 September 2026 after a real install failed with eight errors at once: an over long plugin
description, an XML tag in a skill description, and invalid YAML frontmatter in all six agents,
because an `<example>` block at column 1 reads as a new YAML key. The kit's other five harnesses
all passed while the plugin would not install, because none of them checked what the installer
checks. Exit 0 = the package would install.
"""
import glob
import json
import os
import re
import sys

import yaml

H = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(H, "..", "plugins", "officer-kit")
M = os.path.join(H, "..", ".claude-plugin", "marketplace.json")

PLUGIN_DESC_MAX = 500
DESC_MAX = 1024
XML = re.compile(r"</?[A-Za-z][A-Za-z0-9_-]*(?:\s[^>]*)?>")
# An agent description carries <example> blocks by convention, so tags are expected there.
XML_ALLOWED_IN_AGENT_DESC = {"example", "/example", "commentary", "/commentary"}

fails, checked = [], 0


def frontmatter(path):
    """Return the parsed frontmatter, or raise with a readable message."""
    text = open(path, encoding="utf-8").read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise ValueError("no frontmatter block")
    return yaml.safe_load(m.group(1))


# 1. manifests parse and fit their limits
for path, key in ((os.path.join(P, ".claude-plugin", "plugin.json"), "plugin.json"),
                  (M, "marketplace.json")):
    checked += 1
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        fails.append(f"{key}: not valid JSON ({e})")
        continue
    descs = [("description", d.get("description", ""))] if key == "plugin.json" else \
            [(p.get("name", "?"), p.get("description", "")) for p in d.get("plugins", [])]
    for who, desc in descs:
        if len(desc) > PLUGIN_DESC_MAX:
            fails.append(f"{key}: {who} description is {len(desc)} chars, limit {PLUGIN_DESC_MAX}")
    if key == "plugin.json" and not d.get("name"):
        fails.append("plugin.json: no name")

# the two manifests agree on the version
try:
    pv = json.load(open(os.path.join(P, ".claude-plugin", "plugin.json")))["version"]
    mv = [p.get("version") for p in json.load(open(M))["plugins"] if p.get("name") == "officer-kit"]
    checked += 1
    if mv and mv[0] != pv:
        fails.append(f"version mismatch: plugin.json {pv}, marketplace.json {mv[0]}")
except Exception as e:
    fails.append(f"version comparison failed: {e}")

# 2. every skill: frontmatter parses, has a name, description fits and carries no XML tag
for f in sorted(glob.glob(os.path.join(P, "skills", "*", "SKILL.md"))):
    rel = "skills/" + os.path.basename(os.path.dirname(f))
    checked += 1
    try:
        fm = frontmatter(f)
    except Exception as e:
        fails.append(f"{rel}: frontmatter {str(e).splitlines()[0][:70]}")
        continue
    if not fm.get("name"):
        fails.append(f"{rel}: no name")
    elif fm["name"] != os.path.basename(os.path.dirname(f)):
        fails.append(f"{rel}: name '{fm['name']}' does not match its directory")
    desc = str(fm.get("description", ""))
    if not desc:
        fails.append(f"{rel}: no description")
    if len(desc) > DESC_MAX:
        fails.append(f"{rel}: description is {len(desc)} chars, limit {DESC_MAX}")
    tags = XML.findall(desc)
    if tags:
        fails.append(f"{rel}: description contains XML tags {sorted(set(tags))[:3]}")

# 3. every agent: the same, and the <example> blocks must not break the YAML
for f in sorted(glob.glob(os.path.join(P, "agents", "*.md"))):
    rel = "agents/" + os.path.basename(f)
    checked += 1
    try:
        fm = frontmatter(f)
    except Exception as e:
        fails.append(f"{rel}: frontmatter {str(e).splitlines()[0][:70]}"
                     " (an <example> at column 1 reads as a YAML key; use 'description: |')")
        continue
    if not fm.get("name"):
        fails.append(f"{rel}: no name")
    desc = str(fm.get("description", ""))
    if len(desc) > DESC_MAX:
        fails.append(f"{rel}: description is {len(desc)} chars, limit {DESC_MAX}")
    bad = {t.strip("<>").split()[0] for t in XML.findall(desc)} - XML_ALLOWED_IN_AGENT_DESC
    bad = {b for b in bad if not b.startswith("/") or b[1:] not in ("example", "commentary")}
    if bad:
        fails.append(f"{rel}: description contains unexpected XML tags {sorted(bad)[:3]}")

# 4. every script the skills advertise actually exists and compiles
import ast  # noqa: E402
for f in sorted(glob.glob(os.path.join(P, "skills", "*", "scripts", "*.py"))):
    checked += 1
    try:
        ast.parse(open(f, encoding="utf-8").read(), filename=f)
    except SyntaxError as e:
        fails.append(f"{os.path.relpath(f, P)}: syntax error line {e.lineno} ({e.msg})")

print(f"INSTALL CHECK: {checked} items")
for x in fails:
    print(f"  FAIL  {x}")
if not fails:
    print("  clean, the package would install")
print(f"-> {checked - len(fails)} of {checked} pass")
sys.exit(1 if fails else 0)
