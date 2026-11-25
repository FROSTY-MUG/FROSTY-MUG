import json
import os
import sys

data_path = "data/github-data.json"
assert os.path.exists(data_path), "missing data"
with open(data_path, "r", encoding="utf-8") as f:
    d = json.load(f)

assert "metadata" in d, "missing metadata"
assert "languages" in d, "missing languages"
assert "all_repositories" in d, "missing all_repositories"
assert len(d["all_repositories"]) > 0, "no repositories found"

assert os.path.exists("portfolio/index.html"), "missing portfolio/index.html"
assert os.path.exists("portfolio/styles.css"), "missing portfolio/styles.css"
assert os.path.exists("portfolio/app.js"), "missing portfolio/app.js"
assert os.path.exists("README.md"), "missing README.md"

print("All integrity and validation checks passed successfully!")
