#!/usr/bin/env python3
"""Generate readable project Gantt using task log, scenario assignments, and milestone plan."""
import csv, json, urllib.request, re
from pathlib import Path
from datetime import datetime

ROOT=Path(__file__).resolve().parents[2]
PM=ROOT/"documentation"/"project_management"
LOG=ROOT/"documentation"/"TASK_LOG.md"
PLAN=PM/"milestones.csv"
OUT=PM/"GANTT.md"
REPO="SamRB-dev/PrecisionFarming"

def github_commits():
    req=urllib.request.Request(f"https://api.github.com/repos/{REPO}/commits?per_page=20",
      headers={"Accept":"application/vnd.github+json","User-Agent":"PrecisionFarming-Gantt"})
    try:
      with urllib.request.urlopen(req,timeout=20) as r:return json.loads(r.read())
    except Exception:return []

def date_parse(value):
    value=value.strip()
    for fmt in ("%d %b %Y","%d %B %Y","%d %b %Y"):
      try:return datetime.strptime(value,fmt).date().isoformat()
      except ValueError:pass
    return None

def parse_task_log():
    rows=[]
    text=LOG.read_text(encoding="utf-8")
    for line in text.splitlines():
      if not line.strip().startswith("|") or "Name" in line or "---" in line:continue
      cols=[x.strip() for x in line.strip().strip("|").split("|")]
      if len(cols)<4:continue
      name,task,completed,deadline=cols[:4]
      d=date_parse(completed)
      if d:rows.append((task,name,d,d,"done","Task log"))
    # Scenario assignments have no confirmed completion dates in the task log.
    # Dates below are commit-evidence windows, not official completion dates.
    assignments=[
      ("SC-01: Field Survey and Weed Detection using a Drone","Sadim Rahman Badhan","2026-11-23","2026-11-23","evidence","Commit evidence on 23 Nov; completion date not confirmed in task log"),
      ("SC-02: Task Coordination and Weed Removal","Oyemade Oluwasholape Daniel","2026-11-12","2026-11-20","evidence","Scenario-model/UPPAAL commit evidence; completion date not confirmed in task log"),
      ("SC-03: Communication Failure","Md Arman Zaid Efty","2026-11-09","2026-11-12","evidence","Scenario-model/UPPAAL commit evidence; completion date not confirmed in task log"),
    ]
    rows.extend(assignments)
    return rows

def main():
    rows=parse_task_log()
    with PLAN.open(encoding="utf-8",newline="") as f:
      for t in csv.DictReader(f):rows.append((t["Task"],t["Owner"],t["Start"],t["End"],t["Status"],t["Notes"]))
    commits=github_commits()
    lines=["# Autonomous Systems B — Project Gantt","","> Generated from the task log, scenario assignment/commit evidence, milestones.csv, and recent commit history. Forward-looking dates are estimates unless identified as official.","","## Schedule","","| Task | Owner | Start | End | Status | Notes |","|---|---|---|---|---|---|"]
    for task,owner,start,end,status,note in rows:
      lines.append(f"| {task} | {owner} | {start} | {end} | {status} | {note} |")
    lines += ["","## Timeline","","```mermaid","gantt","    title ASB project schedule","    dateFormat YYYY-MM-DD","    axisFormat %d %b"]
    for task,owner,start,end,status,note in rows:
      label=re.sub(r"[#;]","",task).replace(":"," -")[:55]
      ownerlabel=re.sub(r"[#;]","",owner).replace(":"," -")[:40]
      # Explicit owner is visible in the task label in Mermaid.
      state="done" if status=="done" else ("crit" if status=="official" else "")
      tag=f"{state}, " if state else ""
      lines.append(f"    {label} ({ownerlabel}) :{tag}{start}, {end}")
    lines += ["","```","","## Recent commit activity",""]
    for c in commits:
      msg=c.get("commit",{}).get("message","").splitlines()[0]
      lines.append(f"- {c['commit']['author']['date'][:10]} [{c['sha'][:7]}]({c['html_url']}) — {msg}")
    lines += ["","## Evidence and assumptions","- Task 1 owners and completion dates are taken from documentation/TASK_LOG.md.","- Scenario owners are from the task log; displayed date ranges are commit-evidence windows, not confirmed completion dates.","- Planned milestone dates and status are maintained in milestones.csv.","- The daily GitHub Actions workflow regenerates this document.",""]
    OUT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__":main()
