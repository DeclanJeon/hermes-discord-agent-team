#!/usr/bin/env python3
"""Create the standard Discord channel layout for the Hermes agent team.

Usage:
  DISCORD_BOT_TOKEN=<token> [DISCORD_GUILD_ID=<id>] python3 create-discord-channels.py

This version uses only the Python standard library, so it does not require
third-party packages like discord.py.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from typing import Any

API_BASE = "https://discord.com/api/v10"
TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
GUILD_ID = os.environ.get("DISCORD_GUILD_ID", "").strip()
CATEGORY_NAME = "AGENT-TEAM"
CHANNELS = [
    ("ceo-요청", "CEO 요청 채널 — 사용자가 작업을 요청합니다"),
    ("작업현황", "Kanban 작업 현황 및 알림이 자동 게시됩니다"),
    ("cto", "CTO 에이전트 전용 채널"),
    ("pm", "PM 에이전트 전용 채널"),
    ("swa", "SWA 에이전트 전용 채널"),
    ("devlead", "DevLead 에이전트 전용 채널"),
    ("dev", "Dev 에이전트 전용 채널"),
    ("qa", "QA 에이전트 전용 채널"),
    ("tft-토론", "TFT 토론 및 회의 채널"),
    ("최종결과", "완성된 산출물이 게시됩니다"),
]


def die(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}")
    raise SystemExit(code)


def request_json(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bot {TOKEN}",
        "User-Agent": "HermesDiscordTeamSetup/1.0",
    }
    if body is not None:
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(API_BASE + path, data=body, headers=headers, method=method)

    while True:
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read().decode("utf-8")
                return json.loads(data) if data else None
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                err = json.loads(raw) if raw else {}
            except Exception:
                err = {"raw": raw}

            if exc.code == 429:
                retry_after = 1.0
                if isinstance(err, dict):
                    retry_after = float(err.get("retry_after", retry_after))
                print(f"Rate limited, retrying in {retry_after:.1f}s...")
                time.sleep(retry_after)
                continue

            raise RuntimeError(f"Discord API {exc.code} on {method} {path}: {err}") from exc


def get_guilds() -> list[dict[str, Any]]:
    guilds = request_json("GET", "/users/@me/guilds")
    if not isinstance(guilds, list):
        die(f"Unexpected guild list response: {guilds!r}")
    return guilds


def get_channels(guild_id: str) -> list[dict[str, Any]]:
    channels = request_json("GET", f"/guilds/{guild_id}/channels")
    if not isinstance(channels, list):
        die(f"Unexpected channel list response for guild {guild_id}: {channels!r}")
    return channels


def create_category(guild_id: str) -> dict[str, Any]:
    return request_json(
        "POST",
        f"/guilds/{guild_id}/channels",
        {"name": CATEGORY_NAME, "type": 4},
    )


def create_text_channel(guild_id: str, name: str, topic: str, parent_id: str | None) -> dict[str, Any]:
    payload: dict[str, Any] = {"name": name, "type": 0, "topic": topic}
    if parent_id:
        payload["parent_id"] = parent_id
    return request_json("POST", f"/guilds/{guild_id}/channels", payload)


def main() -> None:
    if not TOKEN:
        die("DISCORD_BOT_TOKEN is not set")

    guilds = get_guilds()
    if GUILD_ID:
        guilds = [g for g in guilds if str(g.get("id")) == GUILD_ID]
        if not guilds:
            die(f"Bot is not in guild {GUILD_ID} or GUILD_ID is incorrect")

    print(f"Found {len(guilds)} guild(s)")
    for guild in guilds:
        guild_id = str(guild["id"])
        guild_name = guild.get("name", guild_id)
        print(f"Server: {guild_name} ({guild_id})")

        channels = get_channels(guild_id)
        category = next((c for c in channels if c.get("type") == 4 and c.get("name") == CATEGORY_NAME), None)
        if category is None:
            category = create_category(guild_id)
            print(f"  Created category: {CATEGORY_NAME}")
        else:
            print(f"  Exists category: {CATEGORY_NAME} ({category.get('id')})")

        for name, topic in CHANNELS:
            existing = next((c for c in channels if c.get("type") == 0 and c.get("name") == name), None)
            if existing:
                print(f"  Exists: #{name} ({existing.get('id')})")
                continue
            ch = create_text_channel(guild_id, name, topic, str(category.get("id")))
            print(f"  Created: #{name} ({ch.get('id')})")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        print(f"ERROR: Discord HTTP {exc.code}: {detail}")
        raise SystemExit(1) from exc
