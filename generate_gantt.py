#!/usr/bin/env python3
import csv,json,urllib.request,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
REPO="SamRB-dev/PrecisionFarming"
tasks=list(csv.DictReader((ROOT/"gantt_tasks.csv").open(encoding="utf-8")))
def gh(url):
 req=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json","User-Agent":"PrecisionFarming-Gantt"})
 with urllib.request.urlopen(req,timeout=20) as r:return json.loads(r.read())
try: commits=gh(f"https://api.github.com/repos/{REPO}/commits?per_page=15")
except Exception: commits=[]
out=["# Autonomous Systems B — Project Gantt","","> Automatically refreshed by GitHub Actions. Observed work and estimated future work are distinguished.","","\n","## Schedule",""]
out+=["| Task | Owner | Start | End | Status | Notes |","|---|---|---|---|---|"]
for t in tasks:out.append("| "+" | ".join(t[k] for k in ["Task","Owner","Start","End","Status","Evidence/notes"])+" |")
out+=["","## Recent commits",""]
for c in commits:
 msg=c["commit"]["message"].splitlines()[0]
 out.append(f"- {c['commit']['author']['date'][:10]} [{c['sha'][:7]}]({c['html_url']}) — {msg}")
out+=["","## Evidence and assumptions","- Task 1 dates/owners from the task log.","- Scenario progress dates from commit evidence reviewed.","- Future dates are estimates; update the CSV to confirm status.",""]
(ROOT/"GANTT.md").write_text("\n".join(out),encoding="utf-8")
