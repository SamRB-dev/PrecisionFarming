#!/usr/bin/env python3
"""Build project Gantt directly from TASK_LOG.md and milestones.csv."""
import csv, json, urllib.request, re
from pathlib import Path
from datetime import datetime

ROOT=Path(__file__).resolve().parents[2]
LOG=ROOT/"documentation"/"TASK_LOG.md"
PLAN=ROOT/"documentation"/"project_management"/"milestones.csv"
OUT=ROOT/"documentation"/"project_management"/"GANTT.md"
REPO="SamRB-dev/PrecisionFarming"

def parse_date(s):
    s=s.strip()
    for fmt in ("%d %b %Y","%d %B %Y","%Y-%m-%d"):
        try:return datetime.strptime(s,fmt).date().isoformat()
        except ValueError:pass
    return ""

def read_task_log():
    rows=[]
    section=""
    for line in LOG.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Task "): section=line.lstrip("# ").strip()
        if not line.strip().startswith("|"):continue
        cols=[c.strip() for c in line.strip().strip("|").split("|")]
        if not cols or cols[0]=="Name" or all(re.fullmatch(r":?-{2,}:?",c or "-") for c in cols):continue
        if len(cols)<4:continue
        owner,task,completed,deadline=cols[:4]
        start=parse_date(completed)
        if not start: continue
        rows.append((task,owner,start,start,"done",section+" — Task log"))
    return rows

def recent_commits():
    req=urllib.request.Request("https://api.github.com/repos/"+REPO+"/commits?per_page=12",headers={"Accept":"application/vnd.github+json","User-Agent":"ASB-Gantt"})
    try:
        with urllib.request.urlopen(req,timeout=15) as r:return json.loads(r.read())
    except Exception:return []

def clean_mermaid(s):
    return re.sub(r"[^A-Za-z0-9 _.-]","",s).replace("  "," ").strip()[:70]

def main():
    rows=read_task_log()
    with PLAN.open(encoding="utf-8",newline="") as f:
        for m in csv.DictReader(f):
            rows.append((m["Task"],m["Owner"],m["Start"],m["End"],m["Status"],m["Notes"]))
    lines=["# Autonomous Systems B — Project Gantt","","> Generated from documentation/TASK_LOG.md and milestones.csv. Completed work is read from the task log only; planned milestones are separate. No hardcoded scenario rows are added.","","## Schedule","","| Task | Owner | Start | End | Status | Notes |","|---|---|---|---|---|---|"]
    for task,owner,start,end,status,note in rows:
        lines.append("| "+ " | ".join([task,owner,start,end,status,note])+" |")
    fence="\x60"*3
    lines += ["","## Timeline","",fence+"mermaid","gantt","    title ASB project schedule","    dateFormat YYYY-MM-DD","    axisFormat %d %b"]
    for task,owner,start,end,status,note in rows:
        label=clean_mermaid(task+" - "+owner)
        state="done" if status.lower()=="done" else ("crit" if status.lower()=="official" else "")
        tag=state+", " if state else ""
        lines.append(f"    {label} :{tag}{start}, {end}")
    lines += ["",fence,"","## Recent commit activity",""]
    for c in recent_commits():
        msg=c.get("commit",{}).get("message","").splitlines()[0]
        lines.append(f"- {c['commit']['author']['date'][:10]} [{c['sha'][:7]}]({c['html_url']}) — {msg}")
    lines += ["","## Notes and evidence","- Completed entries and contributor names are parsed from the task tables in documentation/TASK_LOG.md.","- Task 3 rows with blank completion dates are intentionally excluded from the completed schedule.","- Planned milestones come from milestones.csv and are not represented as completed.","- Scenario work appears once only; no hardcoded scenario dates are appended.","- GitHub Actions regenerates this file.",""]
    OUT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__":main()
