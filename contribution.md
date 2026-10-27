# Contributing to PrecisionFarming

This guide explains how to create your own Git branch, add your work, and submit it for review using a **Pull Request (PR)**.

Repository: https://github.com/SamRB-dev/PrecisionFarming

> **Golden rule:** Do your work on your own branch. Do not commit directly to `main`. Open a PR when your work is ready so the team can review it before merging.

## 1. Before you start

You need:
- A GitHub account with access to this repository.
- Git installed on your computer.
- The repository cloned to your computer.

If you have not cloned the repository yet, open the repository on GitHub, click **Code**, copy the HTTPS URL, then run:

```bash
git clone https://github.com/SamRB-dev/PrecisionFarming.git
cd PrecisionFarming
```

If you already have it, open a terminal in the repository folder.

## 2. Get the latest changes

Before starting a task, update your local `main` branch:

```bash
git switch main
git pull origin main
```

If Git says you have local changes, save or commit those changes before switching branches. Do not discard work you need.

## 3. Create your own branch

Choose a short, descriptive branch name. Use lowercase words separated by hyphens.

Examples:
- `task/manifest-review`
- `task/annotation-tool-comparison`
- `docs/work-package-a`
- `fix/image-paths`

Create and switch to your branch:

```bash
git switch -c task/your-task-name
```

Replace `task/your-task-name` with a name that describes your work.

Check which branch you are on:

```bash
git branch --show-current
```

The command should print your new branch name. Keep working on this branch for the task.

## 4. Add and commit your work

Edit or create the files you are responsible for. Then inspect what changed:

```bash
git status
git diff
```

Stage only the files that belong to your task. For example:

```bash
git add README.md
```

Or stage a specific folder/file:

```bash
git add path/to/your-file
```

Avoid `git add .` if your folder contains large images, temporary files, credentials, or unrelated work. Never commit passwords, API keys, private data, or dataset images that the team has not been permitted to publish.

Commit your changes with a short message describing what you did:

```bash
git commit -m "Add initial image manifest"
```

Use a message that matches your work, for example:
- `Document image selection criteria`
- `Add annotation tool comparison`
- `Fix manifest source paths`

If Git asks you to configure your identity, set your name and email using the instructions from Git or your team lead. Do not use someone else's identity.

## 5. Push your branch to GitHub

The first time you push this branch, run:

```bash
git push -u origin task/your-task-name
```

Use your actual branch name. The `-u` option links your local branch to the remote branch, so future updates can usually be pushed with:

```bash
git push
```

## 6. Open a Pull Request (PR)

### Option A: Use GitHub's prompt

After pushing, open the repository on GitHub. You may see a **Compare & pull request** button for your branch. Click it.

### Option B: Open the PR manually

1. Open the repository on GitHub.
2. Select the **Pull requests** tab.
3. Click **New pull request**.
4. Set the **base** branch to `main`.
5. Set the **compare** branch to your task branch.
6. Check the changed files and confirm that only your intended work is included.
7. Click **Create pull request**.

Use a clear PR title, such as `Add initial image manifest`.

Include a short description:
- **What changed:** Summarize your contribution.
- **Why:** Explain which task or requirement it supports.
- **How to review:** Mention anything the reviewer should check.
- **Evidence/testing:** Include checks performed or screenshots/results, if relevant.

Example PR description:

```text
What changed:
- Added image metadata to the initial manifest.

Why:
- Supports Work Package A data inspection.

How to review:
- Check that filenames, dimensions, and source paths are traceable.

Checks:
- Verified the entries against the local image files.
```

## 7. If the reviewer requests changes

Keep using the same branch. Make the requested edits, then run:

```bash
git status
git add path/to/changed-file
git commit -m "Address PR review feedback"
git push
```

The existing PR updates automatically when you push to its branch. You do not need to create a second PR for the same task.

## 8. After the PR is merged

Once the team lead or reviewer confirms that the PR has been merged, update your local `main` branch:

```bash
git switch main
git pull origin main
```

Then create a new branch for your next task:

```bash
git switch -c task/next-task-name
```

Do not reuse an old branch for an unrelated task.

## 9. If your branch gets behind `main`

If other teammates merge work while you are working, first commit or otherwise safely save your current changes. Then you can update your branch with:

```bash
git fetch origin
git switch task/your-task-name
git merge origin/main
```

If Git reports merge conflicts, stop and resolve them carefully before committing. If you are unsure, ask the team lead for help rather than deleting or overwriting another person's work.

## 10. Important project rules

- **Do not commit directly to `main`.** Submit changes through a PR.
- Keep each branch focused on one task where possible.
- Review the list of changed files before committing and before opening a PR.
- Do not upload the full original image dataset to GitHub unless the team has confirmed that redistribution is permitted. Keep restricted or large source images in the designated storage location.
- Do not commit credentials, private information, temporary files, or unrelated changes.
- Keep your work traceable: use clear commits and describe your contribution in the PR.
- Coordinate with the team if two people need to edit the same file.

## Quick reference

```bash
# Update main
git switch main
git pull origin main

# Create a task branch
git switch -c task/your-task-name

# Review changes
git status
git diff

# Stage and commit
git add path/to/your-file
git commit -m "Describe your change"

# Push branch (first push)
git push -u origin task/your-task-name

# After PR is merged
git switch main
git pull origin main
```

Then open a Pull Request on GitHub from your task branch into `main`.

If you get stuck, share the exact command and error message with the team—do not paste passwords or access tokens.
