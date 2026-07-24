# Code Review Checklist & Template

## Pull Request: {{ PR_TITLE }} (#{{ PR_ID }})

### 1. Code Quality & Formatting
- [ ] Code adheres to Python PEP 8 / TypeScript standard rules
- [ ] Functions are modular with single responsibility
- [ ] Zero commented-out dead code or debug print statements

### 2. Defensive Programming & Error Handling
- [ ] All filesystem/network operations wrapped in try-except blocks
- [ ] Input parameters validated before execution
- [ ] Error messages are clear and actionable

### 3. Verification & Test Coverage
- [ ] New logic accompanied by unit tests
- [ ] Existing test suite passes without regressions
