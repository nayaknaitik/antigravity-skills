# Deployment & Registry Release Specification

## 1. Release Overview
- **Skill Name**: {{ SKILL_NAME }}
- **Target Version**: {{ TARGET_VERSION }}
- **Release Environment**: Global AI Skill Registry

---

## 2. Pre-Deployment Quality Checklist
- [ ] Automated validator returns `valid=True`
- [ ] Automated scorer returns score >= 85
- [ ] All unit tests pass cleanly
- [ ] Security audit completed with 0 high/critical issues

---

## 3. Deployment Steps
1. Tag Git release: `git tag -a v{{ TARGET_VERSION }} -m "Release {{ SKILL_NAME }} v{{ TARGET_VERSION }}"`
2. Push to skill repository main branch.
3. Verify global registry index updates automatically.
