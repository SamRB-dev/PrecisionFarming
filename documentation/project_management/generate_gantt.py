#!/usr/bin/env python3
"""Build project Gantt from documentation/TASK_LOG.md and milestones.csv, plus commit activity."""
import csv, json, urllib.request, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"documentation"
PM=DOC/"project_management"
LOG=DOC/"TASK_LOG.md"
PLAN=PM/"milestones.csv"
OUT=PM/"GANTT.md"
REPO="SamRB-dev/PrecisionFarming"

def github_commits():
    req=urllib.request.Request(f"https://api.github.com/repos/{REPO}/commits?per_page=20",
        headers={"Accept":"application/vnd.github+json","User-Agent":"PrecisionFarming-Gantt"})
    try:
        with urllib.request.urlopen(req,timeout=20) as response:return json.loads(response.read())
    except Exception:return []

def parse_task_log():
    rows=[]
    text=LOG.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.strip().startswith("|") or "Name" in line or "---" in line:continue
        cols=[x.strip() for x in line.strip().strip("|").split("|")]
        if len(cols)<4:continue
        name,task,completed,deadline=cols[:4]
        if completed and completed.lower() not in {""," "}:
            date=re.sub(r"[^0-9A-Za-z ]","",completed)
            try:
                from datetime import datetime
                d=datetime.strptime(date.strip(),"%d %b %Y").date().isoformat()
            except Exception:
                try:d=datetime.strptime(date.strip(),"%d %B %Y").date().isoformat()
                except Exception:continue
            rows.append((task,name,d,d,"done","Task log"))
    return rows

def main():
    rows=parse_task_log()
    with PLAN.open(encoding="utf-8",newline="") as f:
        for t in csv.DictReader(f):rows.append((t["Task"],t["Owner"],t["Start"],t["End"],t["Status"],t["Notes"]))
    commits=github_commits()
    scenario_terms={"SC-01":"SC-01","SC-02":"SC-02","SC-03":"SC-03"}
    for code,term in scenario_terms.items():
        matching=[c for c in commits if term in c["commit"]["message"] or term in c.get("commit",{}).get("message","")]
        if matching:
            date=min(c["commit"]["author"]["date"][:10] for c in matching)
            rows.append((f"{code}: scenario modelling and verification","Assigned scenario owner",date,date,"evidence","Commit-history evidence; task-log date unconfirmed"))
    lines=["# Autonomous Systems B — Project Gantt","","> Generated from TASK_LOG.md, milestones.csv, and recent GitHub commits. Planned dates are estimates unless marked official.","","## Schedule","","| Task | Owner | Start | End | Status | Notes |","|---|---|---|---|---|"]
    for r in rows:lines.append("| "+" | ".join(r)+" |")
    lines+=["","## Mermaid timeline","","```mermaid","gantt","    title ASB project schedule","    dateFormat YYYY-MM-DD","    axisFormat %d %b"]
    for task,owner,start,end,status,note in rows:
        safe=re.sub(r"[^A-Za-z0-9 ]","",task)[:45] or "Task"
        state="done" if status=="done" else ""
        lines.append(f"    {safe} :{state + ',' if state else ''} {start}, {end}")
    lines+=["","```","", "## Recent commit activity",""]
    for c in commits:
        msg=c["commit"]["message"].splitlines()[0]
        lines.append(f"- {c['commit']['author']['date'][:10]} [{c['sha'][:7]}]({c['html_url']}) — {msg}")
    lines+=["","## Data sources and limitations","- Task 1 completion dates and owners are parsed from the task log.","- Scenario progress dates are supported by commit-history evidence; they are not treated as official completion dates.","- Planned milestone dates are maintained in milestones.csv.","- This chart is regenerated daily and when source files change.",""]
    OUT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__":main()
