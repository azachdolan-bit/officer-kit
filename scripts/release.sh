#!/usr/bin/env bash
# Prepare a release of the Officer Kit so the marketplace syncs it to everyone.
# Usage: scripts/release.sh 0.10.1
# Does: bump the version in both plugin.json and marketplace.json, run the install check,
# build dist/officer-kit.plugin, commit on a branch release/v<version>.
# You then: push and Create pull request in GitHub Desktop, Merge on GitHub, and attach
# dist/officer-kit.plugin to a GitHub release tagged v<version>.
set -euo pipefail
VER="${1:?usage: scripts/release.sh <version>}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python3 - "$VER" <<'PY'
import json,sys,re
v=sys.argv[1]
assert re.fullmatch(r"\d+\.\d+\.\d+",v), "version must look like 0.10.1"
for p,keys in (("plugins/officer-kit/.claude-plugin/plugin.json",[["version"]]),
               (".claude-plugin/marketplace.json",[["metadata","version"],["plugins",0,"version"]])):
    d=json.load(open(p,encoding="utf-8"))
    for k in keys:
        o=d
        for kk in k[:-1]: o=o[kk]
        o[k[-1]]=v
    json.dump(d,open(p,"w",encoding="utf-8"),indent=2); open(p,"a").write("\n")
print("versions set to",v)
PY
python3 evals/install_check.py
python3 evals/standards_check.py
python3 evals/study_guide_check.py
python3 evals/quiz_builder_check.py
bash scripts/package.sh
git checkout -b "release/v$VER"
git add -A
git commit -m "Release $VER"
echo
echo "Branch release/v$VER is committed. Now, in GitHub Desktop: Push origin, then Create pull request."
echo "On GitHub: Merge the pull request. Then publish a release tagged v$VER with dist/officer-kit.plugin attached,"
echo "and put this line in its notes: Starter library: https://github.com/azachdolan-bit/officer-kit/releases/download/v0.10.0/Officer-Kit-Starter-Library.zip"
