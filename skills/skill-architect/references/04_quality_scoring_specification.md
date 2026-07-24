# Automated Quality Review & Scoring Specification

## 1. Overview
The Quality Review Process evaluates an AI Skill across 10 evaluation dimensions. The overall **Quality Score** ranges from **0 to 100 points**. Skills must score **85 or higher** to pass quality gate validation and be released into production.

---

## 2. Evaluation Matrix (10 Dimensions)

| ID | Evaluation Dimension | Max Points | Verification Criteria |
| :--- | :--- | :---: | :--- |
| **D1** | **Directory & Structure Completeness** | 10 | All 9 directories (`references/`, `assets/`, `scripts/`, `templates/`, `tests/`, `examples/`, `metadata/`, `docs/`) exist and contain valid files. No forbidden files present. |
| **D2** | **Frontmatter & Metadata Integrity** | 10 | `SKILL.md` contains valid YAML frontmatter with `name`, `description`, `version`, `author`, and `tags`. `metadata/skill.json` matches frontmatter. |
| **D3** | **Activation & Trigger Precision** | 10 | `SKILL.md` defines clear positive triggers, negative constraints (what NOT to trigger on), and disambiguation rules. |
| **D4** | **Input/Output Schema Definition** | 10 | Inputs and outputs are strictly typed with standard JSON Schemas or explicit Markdown tables containing validation rules. |
| **D5** | **Workflow State Machine & Reasoning Strategy** | 10 | `SKILL.md` outlines step-by-step state transitions, chain-of-thought directives, and defensive decision trees. |
| **D6** | **Quality Gates & Failure Handling** | 10 | Includes pre-execution and post-execution checks, edge-case tables, and explicit recovery runbooks for failed states. |
| **D7** | **Template Scaffolding Coverage** | 10 | `templates/` contains production-grade boilerplate for code, tests, documentation, and reviews. |
| **D8** | **Test Suite & Verification Logic** | 10 | `tests/` contains automated test scripts (`test_*.py`) and golden input/output datasets (`golden_*.json`). |
| **D9** | **Golden Examples & Demonstrations** | 10 | `examples/` contains at least one fully compliant, realistic reference implementation. |
| **D10** | **Human & Machine Documentation** | 10 | `docs/` contains `USER_GUIDE.md`, `MAINTAINER_GUIDE.md`, `CHANGELOG.md`, and Architectural Decision Records (`ADR-*.md`). |

---

## 3. Score Breakdown & Grade Classification

$$\text{Total Quality Score} = \sum_{i=1}^{10} \text{Points}(D_i)$$

| Quality Score | Grade | Classification | Release Status | Action Required |
| :---: | :---: | :--- | :---: | :--- |
| **95 - 100** | **A+** | Exemplary Production Skill | **Approved** | Immediate release to global registry. |
| **85 - 94** | **A** | Production Grade | **Approved** | Approved for release; address minor recommendations. |
| **70 - 84** | **B** | Needs Improvement | **Blocked** | Requires revision of weak prompts, missing tests, or templates. |
| **50 - 69** | **C** | Non-Compliant Draft | **Blocked** | Fails structural or schema completeness rules. |
| **0 - 49** | **F** | Invalid / Critical Fail | **Rejected** | Critical missing components (e.g. missing `SKILL.md` or scripts). |

---

## 4. Automated Scoring Formula Implementation

The Python evaluation engine located in `scripts/quality_scorer.py` evaluates skills programmatically using the following rules:

1. **D1 Structure Check (-10 if missing folders)**:
   - Evaluates existence of all 9 subdirectories and `SKILL.md`.
2. **D2 Metadata Check (-10 if frontmatter invalid)**:
   - Parses YAML frontmatter and compares version string against `metadata/skill.json`.
3. **D3 Activation Check (-10 if triggers missing or vague)**:
   - Scans `SKILL.md` for "Activation rules", "Trigger phrases", and "Negative triggers".
4. **D4 Schema Check (-10 if typed schemas missing)**:
   - Checks presence of typed input/output tables or JSON schemas.
5. **D5 Workflow Check (-10 if workflow unstructured)**:
   - Checks for step-by-step workflow stages and explicit decision logic.
6. **D6 Quality Gates Check (-10 if checks/fallbacks absent)**:
   - Verifies presence of pre-flight, post-flight, and failure runbooks.
7. **D7 Templates Check (-10 if standard templates missing)**:
   - Verifies presence of required `.template` or `.md` files in `templates/`.
8. **D8 Tests Check (-10 if no test runner or fixtures)**:
   - Verifies presence of executable Python tests in `tests/`.
9. **D9 Examples Check (-10 if golden examples missing)**:
   - Verifies presence of realistic input/output samples in `examples/`.
10. **D10 Docs Check (-10 if user/maintainer guide missing)**:
   - Verifies presence of user guide, maintainer guide, and changelog in `docs/`.
