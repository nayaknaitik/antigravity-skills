# Architecture Specification Document (ASD)

## 1. Executive Summary
Overview of system architecture, technology choices, and design rationale.

---

## 2. High-Level Architecture Diagram
```mermaid
graph TD
    A[Client / AI Agent] -->|Activates| B(SKILL.md)
    B -->|Lazy Loads| C[references/]
    B -->|Executes| D[scripts/]
    B -->|Fills Scaffolding| E[templates/]
    D -->|Validates| F[tests/]
    D -->|Scores| G[Quality Gate Engine]
```

---

## 3. Data & Directory Contracts
Detailed layout of directory schemas, file interfaces, and API contracts.

---

## 4. Key Architectural Decisions (ADRs)
- **ADR-0001**: 9-Directory Mandatory Structure.
- **ADR-0002**: SemVer 2.0.0 for Skill Evolution.
