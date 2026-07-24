# User Guide: System Architecture Skill

## 1. Overview
The `system-architecture` skill is an AI-first software architecture skill tailored for quantitative trading platforms, high-performance distributed systems, and AI agent architectures. It transforms high-level product requirements into production-ready High-Level Design (HLD), Low-Level Design (LLD), and Architecture Decision Records (ADRs).

---

## 2. Activation Triggers
Activate this skill when:
- Designing a new system, service, module, or trading subsystem.
- Creating High-Level Design (HLD) or Low-Level Design (LLD) specifications.
- Evaluating architectural trade-offs, technology stack choices, or system boundaries.
- Formulating Architecture Decision Records (ADRs).

### Example Prompts:
- *"Generate a High-Level Design for a real-time risk management engine."*
- *"Design a low-level state machine and package structure for our Order Management System (OMS)."*
- *"Create an architecture trade-off analysis comparing Kafka vs Shared Memory for tick distribution."*

---

## 3. Standard Design Outputs Generated
When activated, this skill automatically generates:
1. **Business & Domain Analysis**: Bounded context map, domain entities, ubiquitous language.
2. **High-Level Design (HLD)**: C4 diagrams (Context, Container), technology stack evaluation, scalability/reliability strategies.
3. **Low-Level Design (LLD)**: Package structure, class/struct definitions, sequence diagrams, database schema, error handling, testing strategy.
4. **Architectural Review**: SOLID, KISS, YAGNI, and security verification.
