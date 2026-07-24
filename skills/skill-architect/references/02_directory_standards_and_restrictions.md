# Skill Directory Standards and Storage Restrictions

Every skill generated within the organization MUST strictly follow the 9-directory structure outlined below. No custom top-level folders are permitted without an approved Architectural Decision Record (ADR).

---

## 1. Directory Breakdown

### 1.1 `SKILL.md` (Root Manifest & Instruction Set)
- **Purpose**: The primary entry point and executable instruction manual for the AI Agent.
- **Belongs Inside**: YAML frontmatter (`name`, `description`, `version`, `tags`), trigger rules, workflow state machines, decision logic, input/output specifications, quality gates, and error runbooks.
- **NEVER Store**: Large static datasets, binary files, secret API keys, transient build logs, or unformatted code snippets (>50 lines).

---

### 1.2 `references/` (Knowledge & Domain Rules)
- **Purpose**: Provides deep technical domain context, architectural guidelines, API standards, and detailed decision matrices lazy-loaded by the agent.
- **Belongs Inside**: Markdown (`.md`) files containing syntax specifications, regulatory requirements, framework best practices, data models, and schema references.
- **NEVER Store**: Executable binary code, environment credentials (`.env`), raw build artifacts, user personal data, or duplicate copies of `SKILL.md`.

---

### 1.3 `assets/` (Visual & Static Media Assets)
- **Purpose**: Houses visual diagrams, architecture charts, sample image inputs/outputs, and branding assets referenced in documentation or artifacts.
- **Belongs Inside**: PNG, SVG, JPEG, WebP images, `.mermaid` diagram source files, and visual mockups.
- **NEVER Store**: Executable scripts, sensitive credentials, dynamic source code files (`.py`, `.js`), or un-optimized high-resolution binary files (>10MB).

---

### 1.4 `scripts/` (Automated Tooling & Utilities)
- **Purpose**: Executable scripts used by the skill during generation, linting, validation, quality scoring, or environment manipulation.
- **Belongs Inside**: Python (`.py`), Bash (`.sh`), Node.js (`.js`/`.ts`) scripts, helper CLI utilities, linters, static analyzers, and data conversion scripts.
- **NEVER Store**: Hardcoded passwords/API tokens, compiled binaries without source code, OS-specific raw binaries (`.exe`, `.so`), or non-executable text notes.

---

### 1.5 `templates/` (Reusable Scaffolding Code & Markdown)
- **Purpose**: Production-ready scaffolding templates used by the skill to generate standardized documentation, code, tests, and configurations.
- **Belongs Inside**: Jinja2 (`.j2`), Handlebars (`.hbs`), standard Markdown (`.md`), JSON (`.json`), or boilerplate code templates (`.py.template`, `.ts.template`).
- **NEVER Store**: Fully instantiated concrete projects (those belong in `examples/`), active production secret files, or broken un-parseable syntax templates.

---

### 1.6 `tests/` (Quality Verification & Benchmark Datasets)
- **Purpose**: Automated test suites, evaluation scripts, input/output test fixtures, and prompt benchmark assertions to verify skill accuracy.
- **Belongs Inside**: Test runners (`test_*.py`), golden input/output JSON pairs (`golden_*.json`), test fixtures, edge-case test matrices, and assertion logic.
- **NEVER Store**: Production database dumps containing real customer PII, flaky non-deterministic tests without timeout bounds, or empty placeholder files.

---

### 1.7 `examples/` (Concrete Reference Demonstrations)
- **Purpose**: Golden reference implementations showing human developers and AI agents exactly what a completed, compliant output looks like.
- **Belongs Inside**: Full sample generated skill folders, sample completed architectural documents, sample pull requests, and valid input/output prompt logs.
- **NEVER Store**: Incomplete or non-compliant sample implementations, confidential client code, or un-documented arbitrary code dumps.

---

### 1.8 `metadata/` (Machine-Readable Specifications & Manifests)
- **Purpose**: Machine-readable configuration, schema definitions, dependency locks, and integration manifests for automated orchestrators and CI/CD pipelines.
- **Belongs Inside**: `skill.json` manifests, JSON/YAML schemas (`*_schema.json`), telemetry metrics definitions, dependency manifests (`requirements.txt`, `package.json`).
- **NEVER Store**: Human-targeted guides (those belong in `docs/`), dynamic log outputs, transient cache files (`.pytest_cache`, `__pycache__`), or private SSH keys.

---

### 1.9 `docs/` (Human Engineering & Maintenance Documentation)
- **Purpose**: Operational guides for human developers, skill maintainers, engineering leaders, and auditors.
- **Belongs Inside**: `USER_GUIDE.md`, `MAINTAINER_GUIDE.md`, `CHANGELOG.md`, Architectural Decision Records (`ADR-*.md`), and security audit reports.
- **NEVER Store**: Machine-only config files, raw prompt instruction sets (belonging in `SKILL.md`), or duplicate copies of files in `references/`.

---

## 2. Directory Governance Matrix

| Directory | Primary File Types | Read Target | Executable? | Clean-up Rule |
| :--- | :--- | :--- | :--- | :--- |
| `SKILL.md` | `.md` | Agent System | No | Mandatory Core File |
| `references/` | `.md` | Agent / Human | No | Version Controlled |
| `assets/` | `.svg`, `.png`, `.mermaid` | Human / Artifacts | No | Optimized Binaries Only |
| `scripts/` | `.py`, `.sh` | Agent Terminal | **Yes** | Standard Lint Clean |
| `templates/` | `.j2`, `.template`, `.md` | Agent Engine | No | Strict Syntax Check |
| `tests/` | `.py`, `.json` | CI/CD & Agent | **Yes** | Deterministic Runs |
| `examples/` | `.md`, `.json`, code | Human / Agent | Optional | Compliant Golden Samples |
| `metadata/` | `.json`, `.yaml` | Automation Engine | No | Schema Validated |
| `docs/` | `.md` | Human Engineers | No | Updated on Release |
