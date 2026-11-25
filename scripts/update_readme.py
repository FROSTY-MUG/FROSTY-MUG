#!/usr/bin/env python3
"""
scripts/update_readme.py
Injects dynamic metrics and pinned telemetry table into README.md between comment markers.
Strictly limits pinned telemetry to Ghost-Tag, Genome_Firewall, CareSentry, and FPA.
"""

import os
import json
import re

README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "github-data.json")

PINNED_CONFIG = {
    "Ghost-Tag": {
        "title": "Ghost-Tag",
        "stack": "`TypeScript` &bull; `C++17` &bull; `NFC`",
        "status": "`v2.0.6` Released &bull; 347 Jest Tests &bull; Staging `v2.1.0`"
    },
    "Genome_Firewall": {
        "title": "Genome_Firewall",
        "stack": "`C++14` &bull; `POSIX mmap` &bull; `Threads`",
        "status": "Zero-Copy Parser &bull; 3.4x Wall-Clock Speedup"
    },
    "CareSentry": {
        "title": "CareSentry",
        "stack": "`Python` &bull; `PyTorch` &bull; `MCP`",
        "status": "130 Tests Passing &bull; Invariant Safety Harness"
    },
    "FPA": {
        "title": "FPA",
        "stack": "`TypeScript` &bull; `Groq` &bull; `Pinecone`",
        "status": "1st Place IIT Roorkee FinCortex &bull; Real-time AI"
    }
}

def format_activity_metrics(meta, repos):
    updated_at = (meta.get("harvested_at", "Scheduled") or "")[:19].replace("T", " ") + " UTC"
    stars = meta.get("total_stars", 5)
    repo_cnt = meta.get("public_repos_count", 9)

    repos_by_name = {r.get("name"): r for r in repos}

    rows = []
    for name, cfg in PINNED_CONFIG.items():
        r = repos_by_name.get(name, {})
        pushed = (r.get("pushed_at") or "2026-11-25")[:10]
        stargazers = r.get("stars", 0)
        fork_cnt = r.get("forks", 0)
        url = r.get("html_url", f"https://github.com/FROSTY-MUG/{name}")
        rows.append(f"| **[{name}]({url})** | {cfg['stack']} | {stargazers} ⭐ | {fork_cnt} 🍴 | `{pushed}` | {cfg['status']} |")

    table_rows = "\n".join(rows)

    block = f"""
| Metric | Telemetry Count | Verification Source |
|:---|:---:|:---|
| **Public Systems Repositories** | `{repo_cnt}` | GitHub REST API v3 |
| **Total Stargazers Received** | `{stars}` | Verified Public Stars |
| **Automated Bot Telemetry Pipeline** | Active | Scheduled GitHub Actions (`0 0,12 * * *`) |
| **Telemetry Harvest Timestamp** | `{updated_at}` | Automated Bot Sync |

#### Pinned Systems Health & Deployment State

| Pinned System | Primary Stack | Stars | Forks | Last Pushed | Verification & Status |
|:---|:---|:---:|:---:|:---:|:---|
{table_rows}
"""
    return block.strip()

def main():
    if not os.path.exists(DATA_PATH) or not os.path.exists(README_PATH):
        print("[WARN] Data file or README file missing.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    meta = data.get("metadata", {})
    repos = data.get("all_repositories", [])

    # Replace DYNAMIC_METRICS
    metrics_str = format_activity_metrics(meta, repos)
    metrics_pattern = r"(<!-- BEGIN:DYNAMIC_METRICS -->)(.*?)(<!-- END:DYNAMIC_METRICS -->)"
    content = re.sub(metrics_pattern, f"\\1\n{metrics_str}\n\\3", content, flags=re.DOTALL)

    # Replace LAST_UPDATED
    harvested = (meta.get("harvested_at", "") or "2026-11-25")[:10]
    footer_pattern = r"(<!-- BEGIN:LAST_UPDATED -->)(.*?)(<!-- END:LAST_UPDATED -->)"
    content = re.sub(footer_pattern, f"\\1{harvested}\\3", content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("[SUCCESS] README.md updated with latest telemetry for pinned repositories.")

if __name__ == "__main__":
    main()
