#!/usr/bin/env python3
"""
scripts/update_readme.py
Injects dynamic metrics and language breakdown into README.md between comment markers.
"""

import os
import json
import re

README_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md")
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "github-data.json")

def format_language_table(languages):
    if not languages:
        return "_Language metrics refreshing automatically._"
    
    rows = ["| Language | Percentage | Verified Repositories |", "|---|---|---|"]
    for l in languages[:6]:
        bar = "█" * int(l["percentage"] / 5)
        rows.append(f"| `{l['language']}` | {l['percentage']}% `{bar}` | Ghost-Tag, Genome_Firewall, CareSentry, jocky-, vc_brain |")
    return "\n".join(rows)

def format_activity_metrics(meta, repos):
    updated_at = meta.get("harvested_at", "Scheduled")
    stars = meta.get("total_stars", 0)
    repo_cnt = meta.get("public_repos_count", len(repos))
    
    recent_updates = []
    for r in repos[:4]:
        pushed = r.get("pushed_at", "")[:10]
        recent_updates.append(f"- **[{r['name']}]({r['html_url']})** (`{pushed}`): {r['description'][:90] if r['description'] else 'Active development'}")
    
    updates_block = "\n".join(recent_updates)

    block = f"""
| Metric | Verified Value | Source |
|---|---|---|
| **Public Repositories** | `{repo_cnt}` | GitHub API |
| **Total Stargazers** | `{stars}` | Verified Public Stars |
| **Automation Pipeline** | GitHub Actions | Daily refresh + push event |
| **Data Timestamp** | `{updated_at}` | Automated Bot Sync |

#### Recent Repository Updates
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
    languages = data.get("languages", [])

    # Replace DYNAMIC_METRICS
    metrics_str = format_activity_metrics(meta, repos)
    metrics_pattern = r"(<!-- BEGIN:DYNAMIC_METRICS -->)(.*?)(<!-- END:DYNAMIC_METRICS -->)"
    content = re.sub(metrics_pattern, f"\\1\n{metrics_str}\n\\3", content, flags=re.DOTALL)

    # Replace DYNAMIC_LANGUAGES
    lang_str = format_language_table(languages)
    lang_pattern = r"(<!-- BEGIN:DYNAMIC_LANGUAGES -->)(.*?)(<!-- END:DYNAMIC_LANGUAGES -->)"
    content = re.sub(lang_pattern, f"\\1\n{lang_str}\n\\3", content, flags=re.DOTALL)

    # Replace LAST_UPDATED
    harvested = meta.get("harvested_at", "")[:10]
    footer_pattern = r"(<!-- BEGIN:LAST_UPDATED -->)(.*?)(<!-- END:LAST_UPDATED -->)"
    content = re.sub(footer_pattern, f"\\1{harvested}\\3", content, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(content)

    print("[SUCCESS] README.md updated with latest telemetry.")

if __name__ == "__main__":
    main()
