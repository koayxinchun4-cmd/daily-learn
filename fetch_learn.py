#!/usr/bin/env python3
"""Daily curated learning recommendations based on user roadmap."""

import os, random
from datetime import datetime

today = datetime.utcnow().strftime("%Y-%m-%d")

# Curated pool organized by learning phase
POOL = {
    "algorithms": [
        ("krahets/hello-algo", "Algorithms in 11 languages — animated, interactive", 107000),
        ("TheAlgorithms/Python", "Every algorithm implemented in Python", 201000),
        ("trekhleb/javascript-algorithms", "Algorithms in JS with explanations", 191000),
    ],
    "python": [
        ("Asabeneh/30-Days-Of-Python", "Day-by-day Python, from print() to APIs", 44000),
        ("satwikkansal/wtfpython", "Python quirks explained — learn what NOT to do", 36000),
        ("faif/python-patterns", "Design patterns in Python", 41000),
        ("realpython/python-guide", "Best practices, packaging, deployment", 28000),
    ],
    "javascript": [
        ("Asabeneh/30-Days-Of-JavaScript", "Day-by-day JavaScript", 45000),
        ("getify/You-Dont-Know-JS", "Deep JS concepts, free book series", 182000),
        ("leonardomso/33-js-concepts", "33 core concepts every JS dev needs", 65000),
        ("ryanmcdermott/clean-code-javascript", "Clean code for JS", 93000),
    ],
    "sql": [
        ("NUKnightLab/sql-murder-mystery", "Learn SQL by solving a crime", 17000),
        ("mgramin/awesome-db-tools", "Everything database tools", 4000),
    ],
    "projects": [
        ("codecrafters-io/build-your-own-x", "Build your own DB, Git, bot, OS", 350000),
        ("practical-tutorials/project-based-learning", "Build real things by language", 216000),
        ("florinpop17/app-ideas", "Tiered project ideas beginner→advanced", 82000),
        ("donnemartin/system-design-primer", "Learn how big systems work", 293000),
    ],
    "tools": [
        ("public-apis/public-apis", "Free APIs for your next bot", 337000),
        ("jlevy/the-art-of-command-line", "Master the terminal in one page", 155000),
        ("kamranahmedse/developer-roadmap", "Interactive roadmap for every path", 312000),
        ("EbookFoundation/free-programming-books", "Largest free programming book collection", 355000),
    ],
    "ai_ml": [
        ("microsoft/ML-For-Beginners", "12-week ML curriculum by Microsoft", 72000),
        ("huggingface/transformers", "All state-of-the-art models", 145000),
    ],
}

# Pick 5 repos across phases (rotate daily)
phases = list(POOL.keys())
random.seed(today)  # deterministic per day
random.shuffle(phases)
picks = []
for phase in phases[:5]:
    repo = random.choice(POOL[phase])
    picks.append((repo[0], repo[1], repo[2]))

# Generate record
lines = [f"# Daily Learn — {today}\n"]
lines.append(f"| # | Repo | Why It Matches You | Stars |")
lines.append(f"|---|------|-------------------|-------|")
for i, (repo, reason, stars) in enumerate(picks, 1):
    lines.append(f"| {i} | [{repo}](https://github.com/{repo}) | {reason} | ⭐{stars} |")

# Save record
os.makedirs("records", exist_ok=True)
with open(f"records/{today}.md", "w") as f:
    f.write("\n".join(lines))

# Update README
with open("README.md", "r") as f:
    readme = f.read()

header_end = readme.find("## Today's Pick:")
archive_start = readme.find("## Archive")
new_section = f"## Today's Pick: {today}\n\n" + "\n".join(lines[1:]) + "\n\n"

new_archive_header = readme[archive_start:readme.find("|------", archive_start)+7]
new_entry = f"| [{today}](records/{today}.md) | {phases[0]} + {phases[1]} |\n"
rest = readme[readme.find("\n", readme.find("|------", archive_start)+7)+1:]

# Find where archive table actually is
archive_table_start = readme.find("| Date |", archive_start)
if archive_table_start < 0:
    archive_table_start = readme.find("| Date", archive_start)

final = new_section + "## Archive\n\n" + readme[archive_table_start:archive_table_start+readme[archive_table_start:].find("\n|")+1] + "\n" + new_entry + readme[archive_table_start+readme[archive_table_start:].find("\n|")+2:]

with open("README.md", "w") as f:
    f.write(final)

print(f"Updated for {today}")
