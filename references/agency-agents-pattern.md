# Agency-Agents Hierarchical Pattern

## Org structure
CEO
├─ CTO
├─ PM
├─ SWA
├─ DevLead
├─ Dev
└─ QA

## Core ideas
- Connection-based communication: each agent only talks to explicitly connected agents.
- SOUL.md defines each agent's identity, personality, decision framework, and communication style.
- Use a shared kanban board to route work down the org chart.

## Typical connection map
- CEO ↔ CTO, PM
- CTO ↔ CEO, SWA, DevLead
- PM ↔ CEO, DevLead, QA
- SWA ↔ CTO, DevLead
- DevLead ↔ CTO, SWA, PM, Dev, QA
- Dev ↔ DevLead, QA
- QA ↔ DevLead, Dev, PM

## Kanban assignee chain
- CEO -> DevLead
- CTO -> SWA
- SWA -> DevLead
- DevLead -> Dev
- PM / Dev / QA can execute directly

## Why it matters
This pattern prevents noise, keeps responsibilities clear, and makes TFT-style discussion easier to manage.
