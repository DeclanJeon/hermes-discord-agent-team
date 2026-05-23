# Workspace Strategy

## When to use scratch vs worktree
- scratch: docs, research, single-file config changes, fast iteration
- worktree: code implementation, parallel development, review branches

## Important setup
Set the board default workdir to the project git repository:
```bash
hermes kanban boards set-default-workdir agent-team /absolute/path/to/repo
```

## Common pitfalls
- Worktree tasks fail if default_workdir is missing.
- The base repo must be a git repository.
- Worktree branch names should be descriptive and unique.
