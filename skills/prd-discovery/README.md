# Professional Product Discovery & PRD Generator

This skill orchestrates a rigorous, iterative product discovery process. Rather than acting as a chatbot that blindly fills out a PRD template, this skill behaves as a seasoned Product Manager leading a workshop.

## Architecture

- **`skill.yaml`**: The brain of the skill. Defines the state machine, routing, and conversation strategy.
- **`docs/`**: Highly cohesive markdown files loaded lazily depending on the state of discovery.
- **`templates/`**: The final output template for the PRD, loaded only when discovery is 100% complete.

## Workflow
1. **Initial Intake**: Understand the baseline idea.
2. **Discovery Loop**: Iterative questioning and brainstorming to resolve the 50 dimensions of software product development.
3. **Validation**: Checking for contradictions and scope creep.
4. **Review**: Final sign-off on decisions.
5. **PRD Generation**: Outputting the final structured document.
