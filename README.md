# Hermes Agent × Discord 멀티 에이전트 팀 셋업 가이드

## 조직 구조 (v1.4.0 — agency-agents 기반)

```
           CEO (퍼실리테이터 + 전략)
          /   \
        CTO    PM
         |      |
        SWA     |
         \     /
       Dev Lead
        /    \
      Dev    QA
```

7개 에이전트가 계층적 연결(Connections) 기반으로 소통합니다. CEO는 퍼실리테이터로서 TFT를 구성하고, 토론을 주도하며, 팀을 동적으로 관리합니다. **TFT는 선택이 아닌 필수** — 모든 중요 결정은 TFT를 통해서만 이루어집니다.

## 에이전트 역할

| 에이전트 | 역할 | 연결 | 기본 할당 |
|----------|------|------|-----------|
| **CEO** | 전략, 퍼실리테이션, TFT 구성/해체, 팀 동적 관리 | CTO, PM (전체 채널 접근) | DevLead |
| **CTO** | 기술 전략, 아키텍처 결정, 기술 트레이드오프 분석 | CEO, SWA, DevLead | SWA |
| **PM** | 일정, 리소스, 위험 관리, 진행 추적 | CEO, DevLead, QA | 직접 |
| **SWA** | 시스템 아키텍처 설계, 인터페이스 정의 | CTO, DevLead | DevLead |
| **DevLead** | 개발 총괄, 코드 리뷰, 품질 기준 | CTO, SWA, PM, Dev, QA | Dev |
| **Dev** | 코드 구현, TDD, 테스트 | DevLead, QA | 직접 |
| **QA** | 품질 검수, 버그 리포트, 릴리스 게이트 | DevLead, Dev, PM | 직접 |

## Discord 채널 구조

```
📁 AI 에이전트 팀
  # ceo-요청     — 사용자 → CEO 요청 채널
  # 작업현황     — 진행 상황 공유 (PM, DevLead, QA 접근)
  # cto          — CTO 전용
  # pm           — PM 전용
  # swa          — SWA 전용
  # devlead      — DevLead 전용
  # dev          — Dev 전용
  # qa           — QA 전용
  # tft-토론     — TFT 토론/회의 (모든 에이전트 접근)
  # 최종결과     — 완성된 결과물 게시

📁 아카이브 (v1)
  # researcher   — (v1 아카이브)
  # developer    — (v1 아카이브)
  # designer     — (v1 아카이브)
  # reviewer     — (v1 아카이브)
```

## TFT (Task Force Team) 프로토콜

### 구성 조건
- **모든 프로젝트 시작 시 (킥오프)**: CTO + PM + SWA (TFT는 선택이 아닌 필수)
- 아키텍처 결정 (CTO + SWA + DevLead)
- 기술 vs 일정 트레이드오프 (CTO + PM + DevLead)
- 디자인-개발 핸드오프 (SWA + DevLead + Dev)
- 품질 기준 논의 (DevLead + QA + PM)
- 요구사항 명확화 필요시

### 진행 방식
1. CEO가 #tft-토론에 주제와 참석자 명시
2. 각 참석자가 관점과 근거 제시
3. CEO가 퍼실리테이션하며 합의점 도출
4. 결론과 액션 아이템 정리
5. 결론에 따라 Kanban 태스크 생성/수정

### 해체 조건
- 결론 도출 → 실행 단계 전환
- 참석자 합의
- CEO의 충분한 정보 판단

### TFT 참여 의무
- **CTO**: 모든 킥오프 TFT와 기술 결정 TFT에 필수 참석 (TFT는 선택이 아닌 필수)
- **PM**: 모든 킥오프 TFT와 우선순위/일정 TFT에 필수 참석 (TFT는 선택이 아닌 필수)

## 사용법

### 원클릭 셋업
```bash
chmod +x hermes-discord-team-setup.sh
./hermes-discord-team-setup.sh
```

### 사전 요구사항
1. Hermes Agent v0.14+ 설치
2. Discord Bot Token (Developer Portal)
3. Discord 서버 관리자 권한
4. LLM API 키 (OpenAI, OpenRouter, GLM 등)
5. 봇이 Discord 서버에 이미 초대되어 있어야 함

### Discord 봇 권한 (permissions=311385246800)
- VIEW_CHANNEL
- MANAGE_CHANNELS
- SEND_MESSAGES
- READ_MESSAGE_HISTORY
- ADD_REACTIONS
- EMBED_LINKS
- ATTACH_FILES
- USE_APPLICATION_COMMANDS
- CREATE_PUBLIC_THREADS
- SEND_MESSAGES_IN_THREADS

### Privileged Gateway Intents (필수)
- Message Content Intent: ON
- Server Members Intent: ON

## 작업 흐름 예시

```
사용자: "로그인 기능을 만들어줘"
  ↓
CEO: 요청 분석 → 태스크 그래프 작성
  ├→ CTO: 기술 스택 결정 (OAuth2 vs JWT)
  │   └→ TFT: CTO+SWA+DevLead 토론 → JWT 채택
  ├→ SWA: 아키텍처 설계 (API 스펙, 데이터 모델)
  ├→ PM: 일정 수립 (마일스톤, 마감일)
  ├→ DevLead: 구현 계획 → Dev에게 할당
  │   ├→ Dev: 코드 구현 + 테스트
  │   └→ QA: 품질 검수 → 버그 리포트
  │       └→ Dev: 버그 수정
  └→ CEO: 최종 검수 → 사용자에게 결과 보고
```

## 변경 이력

### v1.4.0
- **CEO 워커 룰**: 간단한 작업(단일 함수, 설정 변경, 30분 이내)은 CEO가 직접 수행, 복잡한 작업만 팀에 위임. Core Rule #1 수정, TFT 구성 조건에 간단한 작업 예외 추가
- **Discord 자동 구독**: dispatcher가 태스크를 spawn할 때 `kanban_notify_subs`에 assignee 채널 구독 자동 등록. CEO config에 `kanban.notify_channels` (profile→channel_id 매핑) 설정
- **gateway/run.py Patch C**: `_tick_once_for_board` spawn 후 auto-subscribe 코드 삽입 (`_kanban_notify_channels` 캐싱, `add_notify_sub` 자동 호출)
- **HERMES_HOME 경로 호환**: 프로필 스코프(`~/.hermes/profiles/ceo`)와 루트(`~/.hermes`) 모두에서 config.yaml 탐색
- **Worktree workspace**: 보드 `default_workdir` 설정, 코드 작업 태스크에 `--workspace worktree --branch <이름>` 지원. CEO Core Rule #10 + Workspace 전략 섹션 추가

### v1.3.0
- **SQLite WAL 경쟁 패치**: `kanban_db.py`의 `release_stale_claims`에 트랜지언트 disk I/O 에러 핸들링 추가, `gateway/run.py`의 dispatcher가 WAL 경쟁 시 보드를 비활성화하지 않고 재시도하도록 변경 (`_consecutive_db_errors` 카운터 도입)
- **WAL 체크포인트 자동화**: `~/.hermes/scripts/kanban-wal-checkpoint.sh` 스크립트 생성, 5분마다 시스템 크론으로 실행하여 WAL 파일 증가 방지
- **TFT 필수 명시**: CEO SOUL.md에 "TFT는 선택이 아닌 필수" 코어 룰 추가, CTO/PM SOUL.md에 "TFT 참여 의무" 섹션 강화
- **Cron 프롬프트 업데이트**: morning-standup 및 stale-task-alert가 7역할 구조(CEO, CTO, PM, SWA, DevLead, Dev, QA)와 TFT 토론 상태를 반영하도록 업데이트
- **패치 대상 파일**: `hermes_cli/kanban_db.py`, `gateway/run.py`

### v1.2.0
- 초기 7역할 에이전트 팀 구조
- Agency-Agents connections 방식 채널 매핑
- Kanban 보드 자동 초기화
- 데일리 스탠드업 및 정체 태스크 알림 cron
