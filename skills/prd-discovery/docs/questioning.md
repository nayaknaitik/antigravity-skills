# Questioning Strategy

**Goal**: Extract missing decisions efficiently without overwhelming the user.

**Actions**:
- **Identify Missing Knowledge**: Ask yourself, "What specific decision is blocking me from writing a complete PRD?"
- **Group Questions**: Never ask 10 random questions. Group 2-3 related questions (e.g., Auth & Roles together, or Scale & Performance together).
- **Explain the WHY**: Prefix questions with context. (e.g., "To ensure we choose the right database architecture, I need to know...")
- **Detect Contradictions**: If an answer conflicts with a previous goal (e.g., "We need 10ms latency but want to use a slow third-party API"), flag it immediately and ask for resolution.
- **Avoid Duplication**: Never ask for something the user has already implicitly or explicitly stated.
