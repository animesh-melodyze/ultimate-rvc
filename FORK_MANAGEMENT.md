# Fork Management

How to keep this fork (`animesh-melodyze/ultimate-rvc`) in sync with upstream
(`JackismyShephard/ultimate-rvc`) while carrying local customizations.

## Remote setup

This repository uses two remotes:

| Remote     | URL                                                | Purpose                                  |
| ---------- | -------------------------------------------------- | ---------------------------------------- |
| `origin`   | https://github.com/animesh-melodyze/ultimate-rvc   | Your fork — `git push` goes here         |
| `upstream` | https://github.com/JackismyShephard/ultimate-rvc   | Original project — read-only source      |

Verify with:

```bash
git remote -v
```

### One-time setup (already done on this machine)

If you ever clone this fork fresh on a new machine, re-add upstream:

```bash
git clone https://github.com/animesh-melodyze/ultimate-rvc.git
cd ultimate-rvc
git remote add upstream https://github.com/JackismyShephard/ultimate-rvc.git
```

## Daily workflow

### Push your local work to your fork

```bash
git push
```

`main` already tracks `origin/main`, so no flags needed.

### Check how far you've diverged from upstream

```bash
git fetch upstream
git rev-list --left-right --count main...upstream/main
# Output: <ahead>  <behind>
#   ahead  = commits in your main not yet in upstream
#   behind = commits in upstream not yet in your main
```

## Syncing with upstream

Run this periodically (weekly is a good cadence; before starting a new feature
is even better).

### Step 1 — Fetch the latest upstream commits

```bash
git fetch upstream
```

This downloads upstream's history but does **not** modify your branches.

### Step 2 — See what changed

```bash
# Summary of new upstream commits
git log --oneline main..upstream/main

# Full diff
git diff main..upstream/main
```

### Step 3 — Merge upstream into your main

Pick one of the two strategies below.

#### Option A — Merge (preserves both histories)

```bash
git checkout main
git merge upstream/main
```

Creates a merge commit. Safest if you've already pushed your changes to your
fork (no history rewriting). Recommended default.

#### Option B — Rebase (linear history)

```bash
git checkout main
git rebase upstream/main
```

Replays your commits on top of upstream. Cleaner history but rewrites your
commits — only use if your changes haven't been shared / merged into other
branches.

### Step 4 — Resolve conflicts (if any)

Git will pause on any file where your changes and upstream's overlap.

```bash
# See which files conflict
git status

# Edit each conflicted file, look for <<<<<<< / ======= / >>>>>>> markers
# Keep the right version, then:
git add <file>

# For merge:
git commit          # finishes the merge

# For rebase:
git rebase --continue
```

If a conflict gets out of hand:

```bash
git merge --abort       # cancels the merge
git rebase --abort      # cancels the rebase
```

### Step 5 — Push the synced main to your fork

```bash
git push
# If you rebased and had already pushed before:
git push --force-with-lease     # safer than --force
```

## Reducing future conflicts

A few habits make upstream syncing painless:

1. **Add new code in new files** rather than editing existing ones. New files
   never conflict.
2. **Feature-flag customizations** instead of deleting upstream code. A
   disabled feature merges cleanly; a deleted file fights with every upstream
   edit to it.
3. **Keep custom changes on a separate branch** if they're large — only merge
   to `main` when you're ready. See "Branch strategy" below.
4. **Sync frequently.** Small merges every week are easier than one giant
   merge after six months.

## Branch strategy (recommended)

```
main            ← tracks upstream + your stable customizations
└── feature/*   ← work in progress
└── custom/*    ← long-running customization branches (optional)
```

- `main` should always work. Don't commit broken code here.
- Develop on `feature/<name>` branches, merge to `main` when ready.
- For invasive changes you want to keep isolated, use `custom/<name>`
  branches that you periodically rebase on top of `main`.

## Quick reference

```bash
# Sync from upstream (most common)
git fetch upstream && git merge upstream/main && git push

# Check divergence
git rev-list --left-right --count main...upstream/main

# List upstream commits not in your fork
git log --oneline main..upstream/main

# Cherry-pick a single upstream commit instead of merging everything
git cherry-pick <commit-sha>

# Inspect a specific upstream file without merging
git show upstream/main:path/to/file.py
```

## Troubleshooting

**"Your branch is behind upstream/main"** — run `git fetch upstream` then
`git merge upstream/main`.

**"Cannot push: rejected (non-fast-forward)"** — your local main rewrote
history (rebase). Use `git push --force-with-lease`.

**Conflicts in a file you haven't touched** — upstream renamed or moved
something. Use `git log --follow <file>` to trace the history.

**Want to throw away local changes and match upstream exactly** — destructive,
ask before running:

```bash
git fetch upstream
git reset --hard upstream/main
git push --force-with-lease
```
