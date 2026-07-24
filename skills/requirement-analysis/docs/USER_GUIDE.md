# Requirement Analysis Skill User Guide

## 1. Overview
`requirement-analysis` is the **FIRST step** of our organization's AI-assisted SDLC. Its purpose is to transform vague business ideas into measurable, testable, complete, implementation-ready System Requirement Specifications (SRS) for our institutional AI-first quantitative trading platform.

Outputs from this skill serve as direct inputs for the downstream **PRD Design** skill.

---

## 2. Invocation & Workflow

### 2.1 Activating the Skill
Activate `requirement-analysis` whenever a product manager, quant researcher, or trading engineer presents a new feature request or business concept.

### 2.2 Interactive Ambiguity Rejection Loop
1. The skill audits user input using `scripts/ambiguity_checker.py`.
2. If vague terms like *"fast"*, *"real-time"*, *"scalable"*, or *"user-friendly"* appear without numerical thresholds, the skill **REJECTS** the requirement and asks targeted clarifying questions.
3. Once all metrics are quantified (e.g. `< 50 microseconds at p99`, `> 100,000 msg/sec`), the skill generates:
   - Functional Requirements (`FR-XXX`)
   - Non-Functional Requirements (`NFR-XXX`)
   - BDD Acceptance Criteria in Gherkin syntax (`Given-When-Then`)
   - End-to-End Traceability Matrix (`RTM`)

---

## 3. Automated Validation Commands

```bash
# Run Ambiguity Checker on a requirements document
python3 .antigravity/skills/requirement-analysis/scripts/ambiguity_checker.py \
  --file .antigravity/skills/requirement-analysis/examples/05_risk_engine_requirements.md

# Run Traceability Matrix Validator
python3 .antigravity/skills/requirement-analysis/scripts/traceability_validator.py \
  --file .antigravity/skills/requirement-analysis/examples/05_risk_engine_requirements.md
```
