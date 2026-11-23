# Project Gantt automation

Copy the files to the repository root. The workflow refreshes recent commit activity daily and updates GANTT.md.

## Enable
1. Commit/push these files.
2. GitHub Settings → Actions → General → workflow permissions; allow write access if necessary.
3. Actions → Refresh project Gantt → Run workflow.

Link GANTT.md from the root README. Update gantt_tasks.csv manually when task completion is confirmed; commits are not automatically interpreted as task completion.
