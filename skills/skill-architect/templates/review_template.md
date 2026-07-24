# Comprehensive Review Summary

## 1. Review Metadata
- **Subject**: {{ REVIEW_SUBJECT }}
- **Reviewer**: {{ REVIEWER_NAME }}
- **Review Date**: {{ REVIEW_DATE }}
- **Recommendation**: {{ RECOMMENDATION }} (Approve / Request Changes / Reject)

---

## 2. Executive Findings
- **Strengths**: High quality score, complete test fixtures.
- **Weaknesses**: Missing edge case handling for corrupted JSON input.

---

## 3. Action Items & Remediation Plan
1. [ ] Add corrupted JSON test fixture to `tests/`.
2. [ ] Update failure recovery section in `SKILL.md`.
