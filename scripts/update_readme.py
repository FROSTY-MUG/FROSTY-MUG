#!/usr/bin/env python3
"""
scripts/update_readme.py
Injects dynamic metrics and language breakdown into README.md between comment markers.
Strictly limits pinned telemetry to Ghost-Tag, Genome_Firewall, CareSentry, and FPA.
"""

import os
import json
import re

README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "github-data.json")

PINNED_NAMES = ["Ghost-Tag", "Genome_Firewall", "CareSentry", "FPA"]

def format_activity_metrics(meta, repos):
    updated_at = meta.get("harvested_at", "Scheduled")
    stars = meta.get("total_stars", 0)
    repo_cnt = meta.get("public_repos_count", len(repos))
    
    pinned_repos = [r for r in repos if r.get("name") in PINNED_NAMES]
    if not pinned_repos:
        pinned_repos = repos[:4]

    recent_updates = []
    for r in pinned_repos:
        pushed = r.get("pushed_at", "")[:10]
        desc = r.get("description", "")
        if not desc:
            if r["name"] == "Genome_Firewall":
                desc = "High-throughput C++ antimicrobial-resistance screening and decision-support engine"
            elif r["name"] == "CareSentry":
                desc = "Deterministic attention-anchored context sentry and defense guard for medical models"
            elif r["name"] == "FPA":
                desc = "Financial Planning & Analysis Studio: real-time forecasting dashboard powered by Groq"
            else:
                desc = "Active systems development"
        recent_updates.append(f"- **[{r['name']}]({r['html_url']})** (`{pushed}`): {desc[:85]}")
    
    updates_block = "\n".join(recent_updates)

    block = f"""
| Metric | Verified Value | Source |
|---|---|---|
| **Public Repositories** | `{repo_cnt}` | GitHub API |
| **Total Stargazers** | `{stars}` | Verified Public Stars |
| **Automation Pipeline** | GitHub Actions | Daily refresh + push event |
| **Data Timestamp** | `{updated_at}` | Automated Bot Sync |

#### Pinned Repository Telemetry
{updates_block}
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
    harvested = meta.get("harvested_at", "")[:10]
    footer_pattern = r"(<!-- BEGIN:LAST_UPDATED -->)(.*?)(<!-- END:LAST_UPDATED -->)"
    content = re.sub(footer_pattern, f"\\1{harvested}\\3", content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("[SUCCESS] README.md updated with latest telemetry for pinned repositories.")

if __name__ == "__main__":
    main()
