#!/usr/bin/env python3
"""Refresh the "Merged upstream" table and the fix counts in this profile.

Searches for merged pull requests authored by drakeo338, drops any PR opened
in a repo drakeo338 owns, fetches each remaining repo's star count, and
regenerates the "Merged upstream" table in README.md between the
<!-- merged:start --> / <!-- merged:end --> markers, sorted by star count
descending.

The hand-written "Fix" column text for each PR lives in data/fixes.json,
keyed "owner/repo#N". An existing entry is left alone. A PR that is not in
the file yet gets an initial fix text derived from its own title (any
conventional-commit prefix such as "fix(engine): " is stripped and the first
letter is capitalised), and that entry is written back to data/fixes.json so
it can be hand-edited afterwards.

The fix counts embedded in README.md's image alt text and in both card SVGs
("N open-source fixes merged into M projects" / "M projects (N PRs)") are
updated to match.

Usage:
    GH_TOKEN=... python3 scripts/refresh.py [--dry-run]

Reads a token from the GITHUB_TOKEN or GH_TOKEN environment variable. Public
data is reachable without one, just at a much lower rate limit, so a missing
token is a warning, not a hard failure.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
FIXES = ROOT / "data" / "fixes.json"
CARD_LIGHT = ROOT / "assets" / "card-light.svg"
CARD_DARK = ROOT / "assets" / "card-dark.svg"

OWNER = "drakeo338"
API = "https://api.github.com"
MARK_START = "<!-- merged:start -->"
MARK_END = "<!-- merged:end -->"

TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

CONVENTIONAL_TYPES = (
    r"(?:fix|feat|feature|chore|docs?|refactor|perf|test|tests|build|ci|"
    r"style|revert|improvement)"
)
PREFIX_RE = re.compile(rf"^{CONVENTIONAL_TYPES}(\([^)]*\))?!?:\s*", re.IGNORECASE)
COUNT_RE = re.compile(r"\d+ open-source fixes merged into \d+ projects")
PROJECTS_PRS_RE = re.compile(r"\d+ projects \(\d+ PRs\)")
PR_URL_RE = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/pull/(\d+)$")
README_ROW_RE = re.compile(
    r"^\|\s*\[([^/\]]+)/([^\]#]+?)\s*#(\d+)\]\([^)]*\)\s*\|\s*[^|]+\|\s*(.+?)\s*\|\s*$"
)
TABLE_BLOCK_RE = re.compile(
    r"(### Merged upstream\n\n)(\|.*\|\n)(\|[-: |]+\|\n)((?:\|.*\|\n?)*)"
)


def api_get(path, params=None):
    url = f"{API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "drakeo338-profile-refresh",
            **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
        },
    )
    backoff = 2.0
    last_err = None
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (403, 429, 502, 503) and attempt < 5:
                time.sleep(backoff)
                backoff *= 2
                continue
            raise
    raise RuntimeError(f"GET {path} failed after retries") from last_err


def search_merged_prs(login):
    """Return every merged PR authored by login, across all repos."""
    items = []
    page = 1
    while page <= 10:  # the search API caps results at 1000 (10 x 100)
        data = api_get(
            "/search/issues",
            {"q": f"is:pr is:merged author:{login}", "per_page": 100, "page": page},
        )
        batch = data.get("items", [])
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return items


def parse_pr_url(html_url):
    m = PR_URL_RE.match(html_url or "")
    if not m:
        return None
    owner, repo, num = m.groups()
    return owner, repo, int(num)


def format_stars(n):
    if n >= 1000:
        v = n / 1000.0
        s = f"{v:.1f}"
        if s.endswith(".0"):
            s = s[:-2]
        return f"{s}k"
    return str(n)


def strip_conventional_prefix(title):
    title = (title or "").strip()
    stripped = PREFIX_RE.sub("", title, count=1).strip()
    if stripped:
        title = stripped
    if title:
        title = title[0].upper() + title[1:]
    return title


def load_fixes():
    if FIXES.exists():
        return json.loads(FIXES.read_text())
    return {}


def save_fixes(fixes):
    FIXES.parent.mkdir(parents=True, exist_ok=True)
    FIXES.write_text(json.dumps(fixes, indent=2, sort_keys=True) + "\n")


def seed_fixes_from_readme(fixes):
    """First run only: pick up the hand-written fix text already in README.md."""
    if not README.exists():
        return fixes
    for line in README.read_text().splitlines():
        m = README_ROW_RE.match(line.strip())
        if not m:
            continue
        owner, repo, num, fix = m.groups()
        key = f"{owner}/{repo.strip()}#{num}"
        if key not in fixes:
            fixes[key] = fix.strip()
    return fixes


def build_table(rows):
    lines = ["| Project | Stars | Fix |", "|---|--:|---|"]
    for r in rows:
        full = f"{r['owner']}/{r['repo']}"
        link = f"https://github.com/{full}/pull/{r['num']}"
        lines.append(f"| [{full} #{r['num']}]({link}) | {format_stars(r['stars'])} | {r['fix']} |")
    return "\n".join(lines) + "\n"


def replace_between_markers(text, table_body):
    block = f"{MARK_START}\n{table_body}{MARK_END}"
    marker_re = re.compile(re.escape(MARK_START) + r".*?" + re.escape(MARK_END), re.S)
    if marker_re.search(text):
        return marker_re.sub(lambda _m: block, text, count=1)

    if TABLE_BLOCK_RE.search(text):
        return TABLE_BLOCK_RE.sub(lambda m: m.group(1) + block + "\n", text, count=1)

    # Neither markers nor an existing table: append a new section.
    sep = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
    return text + f"{sep}### Merged upstream\n\n{block}\n"


def update_counts(text, merged_count, project_count):
    text = COUNT_RE.sub(f"{merged_count} open-source fixes merged into {project_count} projects", text)
    text = PROJECTS_PRS_RE.sub(f"{project_count} projects ({merged_count} PRs)", text)
    return text


def main(argv):
    dry_run = "--dry-run" in argv

    if not TOKEN:
        print("warning: no GITHUB_TOKEN/GH_TOKEN set; using unauthenticated, rate-limited requests", file=sys.stderr)

    first_run = not FIXES.exists()
    fixes = load_fixes()
    if first_run:
        fixes = seed_fixes_from_readme(fixes)

    items = search_merged_prs(OWNER)

    rows_by_key = {}
    star_cache = {}
    for it in items:
        parsed = parse_pr_url(it.get("html_url"))
        if not parsed:
            continue
        owner, repo, num = parsed
        if owner.lower() == OWNER.lower():
            continue  # drop PRs in repos drakeo338 owns
        full = f"{owner}/{repo}"
        key = f"{full}#{num}"
        if full not in star_cache:
            repo_data = api_get(f"/repos/{full}")
            star_cache[full] = repo_data.get("stargazers_count", 0)
        stars = star_cache[full]
        if key in fixes:
            fix = fixes[key]
        else:
            fix = strip_conventional_prefix(it.get("title", "")) or it.get("title", "")
            fixes[key] = fix
        rows_by_key[key] = {"owner": owner, "repo": repo, "num": num, "stars": stars, "fix": fix}

    rows = sorted(
        rows_by_key.values(),
        key=lambda r: (-r["stars"], r["owner"].lower(), r["repo"].lower(), r["num"]),
    )

    merged_count = len(rows)
    project_count = len({f"{r['owner']}/{r['repo']}" for r in rows})
    table_body = build_table(rows)

    if dry_run:
        print(table_body)
        print(f"merged_count={merged_count} project_count={project_count}")
        return 0

    save_fixes(fixes)

    text = README.read_text()
    text = replace_between_markers(text, table_body)
    text = update_counts(text, merged_count, project_count)
    README.write_text(text)

    for path in (CARD_LIGHT, CARD_DARK):
        if not path.exists():
            continue
        svg = path.read_text()
        svg = update_counts(svg, merged_count, project_count)
        path.write_text(svg)

    print(f"merged_count={merged_count} project_count={project_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
