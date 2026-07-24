# System Requirements Document (SRD)

## 1. Project Overview
- **Project Name**: {{ PROJECT_NAME }}
- **Objective**: {{ OBJECTIVE }}

---

## 2. Functional Requirements
| ID | Title | Description | Priority |
| :--- | :--- | :--- | :---: |
| `FR-01` | Skill Generation | Scaffolds 9 standard subdirectories automatically | MUST |
| `FR-02` | Quality Scoring | Calculates 0-100 score across 10 evaluation dimensions | MUST |

---

## 3. Non-Functional Requirements
| ID | Category | Requirement | Target Metric |
| :--- | :--- | :--- | :--- |
| `NFR-01` | Performance | Skill validation execution time | < 2.0 seconds |
| `NFR-02` | Security | Zero hardcoded API keys or secrets | 100% compliance |
