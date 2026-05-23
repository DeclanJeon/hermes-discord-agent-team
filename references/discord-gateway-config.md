# Discord Gateway Configuration Reference

## Required environment variables
- DISCORD_BOT_TOKEN: Discord bot token. Use this exact name; DISCORD_TOKEN is ignored.
- GATEWAY_ALLOW_ALL_USERS=true: allow any user to interact with the gateway.

## Discord Developer Portal requirements
Enable both privileged intents:
- Message Content Intent
- Server Members Intent

Without them, the gateway typically times out or throws PrivilegedIntentsRequired.

## Recommended channel config per profile
```yaml
discord:
  require_mention: false
  free_response_channels: <primary-channel-id>
  allowed_channels: <comma-separated-channel-ids>
  auto_thread: true
```

## Discord invite permissions
Minimum invite permission sum used by this team:
- 311385246800

## Gateway commands
```bash
hermes gateway status
hermes gateway start
hermes gateway stop
hermes gateway restart
hermes -p ceo gateway install
```

## Common pitfalls
- DISCORD_TOKEN does not work; use DISCORD_BOT_TOKEN.
- Profile .env files do not inherit later changes from the root .env.
- One Discord bot token should be connected to only one active gateway.
