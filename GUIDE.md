# Antigravity Skills Directory Guide

Welcome to the `first-platform` AI skills directory. This folder (`.agents/`) is natively compatible with Google Antigravity. It acts as the central brain and standard operating procedure (SOP) repository for all AI coding agents working on this project.

## Directory Structure

```text
.agents/
├── GUIDE.md                 <-- This file
└── skills/                  <-- All active Antigravity skills
    ├── code-review/
    ├── go-engineering/
    ├── java-engineering/
    ├── production-engineering/
    ├── requirement-analysis/
    ├── rust-engineering/
    ├── skill-architect/
    ├── system-architecture/
    └── trading-platform-uiux/
```

## How It Works

Antigravity agents automatically discover any skill placed inside the `.agents/skills/` directory. Each skill folder must contain a `SKILL.md` file with YAML frontmatter specifying its activation rules and descriptions.

When a user prompts the agent, the AI scans these descriptions and automatically "activates" the relevant skills, inheriting the specific domain knowledge, best practices, layout templates, and validation scripts defined within that folder.

## Active Skills in this Workspace

### Frontend & UI
*   **`trading-platform-uiux`**: Mandatory standard for any UI/UX design, chart layouts, and CSS/Tailwind work on the NexTrade platform. Enforces tabular-nums and specific semantic colors.

### Backend & Systems
*   **`rust-engineering`**: High-performance backend engineering rules using Rust, Tokio, Axum, and SQLx. Enforces lock-free concurrency and strict memory safety.
*   **`system-architecture`**: Generates High-Level Designs (HLD), Low-Level Designs (LLD), and Architecture Decision Records (ADR). Used for scaling from monolithic to distributed architectures.
*   **`code-review`**: Automated codebase reviewer for maintaining architectural and security standards.
*   **`production-engineering`**: DevOps and Site Reliability Engineering guidelines (CI/CD, Kubernetes, Observability).

*(Other legacy language skills like `go-engineering` and `java-engineering` are also available for polyglot microservice expansion).*

## Creating New Skills
To define a new skill for your project, simply create a new folder under `.agents/skills/new-skill-name/` and place a `SKILL.md` inside it. You can also ask the agent to use the `skill-architect` skill to scaffold one for you.
