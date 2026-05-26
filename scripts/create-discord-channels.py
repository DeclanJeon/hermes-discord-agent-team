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
from typing import Any, TypedDict

API_BASE = "https://discord.com/api/v10"
TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "").strip()
GUILD_ID = os.environ.get("DISCORD_GUILD_ID", "").strip()
CATEGORY_NAME = "AGENT-TEAM"


class ChannelSpec(TypedDict):
    name: str
    emoji: str
    topic: str
    guide: str


CHANNELS: list[ChannelSpec] = [
    {
        "name": "ceo-요청",
        "emoji": "👑",
        "topic": "👑 CEO 요청 채널 — 사용자가 작업을 요청하고 CEO가 분석·분해·라우팅합니다",
        "guide": """👑 **CEO 요청 채널**

이 채널은 사용자가 AI 에이전트 팀에 작업을 요청하는 입구입니다.

**CEO의 역할**
- 사용자 요청을 목표/제약/완료 기준으로 정리합니다.
- 간단한 작업은 직접 처리하고, 복잡한 작업은 팀에 위임합니다.
- 필요한 경우 TFT를 열어 CTO/PM/SWA/DevLead/Dev/QA 의견을 모읍니다.
- Kanban 태스크를 만들고 담당자·의존성·검수 흐름을 관리합니다.

**사용자는 이렇게 요청하면 좋습니다**
- 원하는 결과물, 대상 저장소/서비스, 우선순위, 마감/제약을 함께 적어주세요.
- 예: “PDF 변환 오류를 고쳐줘. 로컬 테스트 후 pons-link에 배포해줘.”

**흐름**
요청 접수 → CEO 분석 → TFT/작업분해 → 담당자 배정 → 진행 보고 → 최종 결과 공유""",
    },
    {
        "name": "작업현황",
        "emoji": "📊",
        "topic": "📊 작업현황 — Kanban 진행 상황, 자동 알림, 스탠드업, 블로커 공유",
        "guide": """📊 **작업현황 채널**

이 채널은 전체 작업의 관제탑입니다.

**주요 내용**
- Kanban 태스크 생성/시작/완료/차단 알림
- 데일리 스탠드업 및 정체 태스크 경고
- PM·DevLead·QA의 진행/리스크/품질 상태 보고
- 사용자가 현재 어디까지 진행됐는지 확인하는 공개 상태판

**보고 원칙**
- 무엇이 완료됐는지, 다음 액션은 무엇인지, 누가 담당하는지 명확히 적습니다.
- 블로커가 있으면 원인·필요 결정·해결 요청을 함께 적습니다.
- 완료 보고에는 검증 방법과 결과를 포함합니다.""",
    },
    {
        "name": "cto",
        "emoji": "🧭",
        "topic": "🧭 CTO — 기술 전략, 아키텍처 방향, 기술 리스크와 트레이드오프 판단",
        "guide": """🧭 **CTO 채널**

CTO는 팀의 기술 방향과 주요 의사결정을 책임집니다.

**담당 역할**
- 기술 전략 및 스택 선택
- 아키텍처 방향성과 핵심 트레이드오프 판단
- 기술 리스크, 운영 비용, 확장성 검토
- SWA·DevLead에게 기술 가이드 제공
- 중요한 결정은 CEO에게 권고 또는 에스컬레이션

**이 채널에 올라오는 내용**
- 기술 검토 요청
- 아키텍처 의사결정 초안
- 성능/보안/운영 리스크 평가
- CTO 관점의 승인 또는 변경 요청""",
    },
    {
        "name": "pm",
        "emoji": "📅",
        "topic": "📅 PM — 일정, 범위, 우선순위, 리소스, 위험 관리",
        "guide": """📅 **PM 채널**

PM은 프로젝트가 현실적인 범위와 일정 안에서 끝나도록 조율합니다.

**담당 역할**
- 일정·마일스톤·우선순위 수립
- 범위 관리 및 리소스 배분
- 리스크/블로커 추적
- 진행 상황을 사용자 관점으로 정리
- QA 결과와 릴리스 준비 상태 확인

**이 채널에 올라오는 내용**
- 일정/범위 조정 요청
- 우선순위 판단
- 리스크 보고
- 사용자 커뮤니케이션 초안""",
    },
    {
        "name": "swa",
        "emoji": "🏗️",
        "topic": "🏗️ SWA — 시스템 아키텍처, 인터페이스, 데이터 흐름 설계",
        "guide": """🏗️ **SWA(System/Software Architect) 채널**

SWA는 구현 전에 시스템 구조와 인터페이스를 명확히 합니다.

**담당 역할**
- 시스템 아키텍처 설계
- 모듈 경계, API, 데이터 흐름 정의
- DevLead가 구현 가능한 설계로 변환할 수 있게 문서화
- CTO 전략을 실제 구조로 구체화
- 설계 리스크와 대안을 제시

**이 채널에 올라오는 내용**
- 설계 초안 및 다이어그램
- API/DB/모듈 인터페이스 정의
- 구현 전 확인해야 할 아키텍처 이슈""",
    },
    {
        "name": "devlead",
        "emoji": "🧑‍💻",
        "topic": "🧑‍💻 DevLead — 구현 계획, 코드 리뷰, 개발 품질 기준, Dev/QA 조율",
        "guide": """🧑‍💻 **DevLead 채널**

DevLead는 설계를 실행 가능한 개발 작업으로 쪼개고 품질을 책임집니다.

**담당 역할**
- 구현 계획 수립 및 Dev에게 작업 할당
- 코드 리뷰와 기술 품질 기준 관리
- CTO/SWA 설계를 실제 코드 작업으로 변환
- Dev와 QA 사이의 수정 루프 조율
- 병목이 생기면 CEO/PM에게 즉시 공유

**이 채널에 올라오는 내용**
- 구현 체크리스트
- 코드 리뷰 결과
- Dev 작업 지시/피드백
- QA 차단 이슈에 대한 수정 계획""",
    },
    {
        "name": "dev",
        "emoji": "⚙️",
        "topic": "⚙️ Dev — 코드 구현, 테스트, 버그 수정, 커밋 가능한 산출물 작성",
        "guide": """⚙️ **Dev 채널**

Dev는 실제 코드를 작성하고 테스트로 검증합니다.

**담당 역할**
- 기능 구현 및 버그 수정
- 로컬 테스트/타입체크/린트 등 기본 검증
- 변경 파일과 테스트 결과를 명확히 보고
- DevLead 리뷰 요청 및 QA 검수 대응
- 코드 작업은 가능하면 worktree/branch로 격리

**이 채널에 올라오는 내용**
- 구현 진행 상황
- 테스트 결과
- 변경 요약
- 리뷰 요청 및 수정 완료 보고""",
    },
    {
        "name": "qa",
        "emoji": "🧪",
        "topic": "🧪 QA — 품질 검수, 재현 절차, 테스트 결과, 릴리스 게이트",
        "guide": """🧪 **QA 채널**

QA는 결과물이 사용자에게 전달 가능한지 검증하는 릴리스 게이트입니다.

**담당 역할**
- 요구사항 기준 검수
- 기능/회귀/엣지케이스 테스트
- 버그 재현 절차와 기대/실제 결과 작성
- 통과(APPROVE) 또는 변경 요청(REQUEST CHANGES) 판단
- 배포 전 최종 품질 리스크 공유

**이 채널에 올라오는 내용**
- 테스트 계획과 결과
- 버그 리포트
- 검수 승인/반려 사유
- 릴리스 준비 상태""",
    },
    {
        "name": "tft-토론",
        "emoji": "🤝",
        "topic": "🤝 TFT 토론 — 역할 간 의사결정, 킥오프, 아키텍처/일정/품질 합의",
        "guide": """🤝 **TFT(Task Force Team) 토론 채널**

복잡한 작업에서 여러 역할의 판단이 필요할 때 사용하는 회의실입니다.

**언제 사용하나**
- 프로젝트 킥오프: CTO + PM + SWA
- 아키텍처 결정: CTO + SWA + DevLead
- 일정/품질 트레이드오프: CTO + PM + DevLead
- 디자인/개발 핸드오프: SWA + DevLead + Dev
- 품질 기준 논의: DevLead + QA + PM

**토론 형식**
📌 토론 주제 / 👥 참석자 / 🎯 목표 / ⏱️ 제한 / ✅ 결론 / 🔜 액션 아이템

CEO가 퍼실리테이션하고, 결론이 나면 Kanban 태스크로 실행 단계에 넘깁니다.""",
    },
    {
        "name": "최종결과",
        "emoji": "✅",
        "topic": "✅ 최종결과 — 사용자에게 전달할 완료 산출물, 검증 결과, 배포/운영 안내",
        "guide": """✅ **최종결과 채널**

완료된 산출물과 사용자에게 전달할 최종 보고가 모이는 채널입니다.

**포함해야 할 내용**
- 최종 결과 요약
- 변경/구현/작성된 산출물 위치
- 테스트 및 검증 결과
- 배포 여부와 접속/사용 방법
- 남은 리스크나 후속 권장 작업

**원칙**
- 사용자가 바로 이해하고 사용할 수 있게 씁니다.
- “완료했다”만 쓰지 말고 무엇으로 검증했는지 반드시 포함합니다.""",
    },
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


def post_channel_guide(channel_id: str, spec: ChannelSpec) -> None:
    request_json(
        "POST",
        f"/channels/{channel_id}/messages",
        {"content": spec["guide"], "allowed_mentions": {"parse": []}},
    )


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

        for spec in CHANNELS:
            name = spec["name"]
            existing = next((c for c in channels if c.get("type") == 0 and c.get("name") == name), None)
            if existing:
                print(f"  Exists: {spec['emoji']} #{name} ({existing.get('id')})")
                continue
            ch = create_text_channel(guild_id, name, spec["topic"], str(category.get("id")))
            post_channel_guide(str(ch.get("id")), spec)
            print(f"  Created: {spec['emoji']} #{name} ({ch.get('id')}) + guide")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace") if exc.fp else ""
        print(f"ERROR: Discord HTTP {exc.code}: {detail}")
        raise SystemExit(1) from exc
