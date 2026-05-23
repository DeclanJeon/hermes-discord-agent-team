# Kanban Notify Subscriptions

## Problem
Tasks created via CLI may not automatically register Discord notification subscriptions. If `kanban_notify_subs` is empty, task updates can be silent.

## Fix approach
1. Add `kanban.notify_channels` to the CEO profile config.
2. Patch the gateway dispatcher so spawned tasks are auto-subscribed to the assignee's Discord channel.
3. For existing tasks, backfill subscriptions in the kanban DB.

## Example config
```yaml
kanban:
  notify_channels:
    ceo: "<channel-id>"
    cto: "<channel-id>"
    pm: "<channel-id>"
    swa: "<channel-id>"
    devlead: "<channel-id>"
    dev: "<channel-id>"
    qa: "<channel-id>"
```

## Verification
- Create a task on the board.
- Confirm a row appears in `kanban_notify_subs` for the task.
- Finish the task and verify the channel receives the terminal event.
