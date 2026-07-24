# Antigravity, Gemini & Claude Skill Architecture Standards

## Executive Summary
This reference document establishes the architectural synthesis of agent skill design across Google Antigravity, Google Gemini, and Anthropic Claude ecosystems. It bridges prompt engineering, tool orchestration, and enterprise Software Development Lifecycle (SDLC) standards into a unified model for AI Skills.

---

## 1. Multi-Platform Skill Synthesis

### 1.1 Antigravity Skill Paradigm
- **Frontmatter**: YAML metadata header containing `name` and `description` used for implicit skill routing and agent activation.
- **Context Management**: Dynamic document inclusion using standard Markdown links to local `references/*.md` files. This keeps the primary `SKILL.md` concise while lazy-loading detailed domain rules.
- **Tool Exposing**: Native integration with terminal execution, file system modification, subagent orchestration (`invoke_subagent`), background process monitoring, and Model Context Protocol (MCP) servers.

### 1.2 Gemini System & Skill Patterns
- **Structured Reasoning**: Multi-stage chain-of-thought instructions requiring explicit hypotheses before code mutation.
- **Context Windows**: High-capacity context utilization leveraging strict hierarchical document structure (H1 -> H2 -> H3) for precise semantic retrieval.
- **Parametric Constraints**: Strict typed inputs/outputs to eliminate hallucination in system calls and file edits.

### 1.3 Claude Agent & Tool Guidelines
- **Role & Boundary Specification**: Explicit definition of agent capabilities, forbidden actions (negative constraints), and failure fallbacks.
- **State Machine Workflow**: Explicit step-by-step state transitions (e.g., `INIT -> RESEARCH -> PLAN -> IMPLEMENT -> VERIFY -> HANDOFF`).
- **Defensive Prompting**: Pre-flight verification gates prior to executing write operations or shell commands.

---

## 2. Core Architectural Principles for AI Skills

1. **Determinism over Ambiguity**:
   Skills must define exact inputs, explicit validation logic, clear quality gates, and deterministic output schemas.
2. **Modular File Decomposition**:
   A skill is not a single giant prompt. It is a structured repository containing instructions (`SKILL.md`), reference manuals (`references/`), automation tooling (`scripts/`), reusable scaffolding (`templates/`), test suites (`tests/`), concrete examples (`examples/`), machine metadata (`metadata/`), and human documentation (`docs/`).
3. **Lazy-Loaded Context**:
   High-density domain knowledge must reside in `references/` files and be read by the agent only when activated or when specific sub-paths are triggered.
4. **Automated Quality Gates**:
   Every skill must be programmatically verifiable. Un-verified skill outputs or broken schemas are considered build failures.
5. **Zero-Lock-in Portability**:
   Skill definitions must rely on standard Markdown, JSON Schemas, Python scripts, and standard CLI conventions so they can execute cleanly across Antigravity CLI, IDE, or automated CI/CD pipelines.

---

## 3. Tool Interaction & MCP Integration Standards

- **Static Reference vs Dynamic MCP**:
  - Use `references/` for static domain rules, coding standards, and internal organization schemas.
  - Use `MCP (Model Context Protocol)` servers for live database lookups, real-time API integrations, and interactive external environments.
- **Command Execution Safety**:
  - Always validate target paths before executing filesystem or shell commands.
  - Never execute un-scoped destructive shell commands (e.g., raw `rm -rf *` without absolute path validation).
