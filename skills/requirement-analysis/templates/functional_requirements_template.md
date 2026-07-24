# Functional Requirements Specification Template

## Functional Requirement: {{ FR_ID }} - {{ FR_TITLE }}

- **Parent Business Goal**: {{ PARENT_GOAL_ID }}
- **Module**: {{ MODULE_NAME }} (OMS / EMS / Risk Engine / Quant Research)
- **Priority**: {{ MOSCOW_PRIORITY }} (MUST / SHOULD / COULD / WON'T)
- **Actors**: {{ ACTORS }}

### 1. Functional Description
{{ DETAILED_DESCRIPTION }}

### 2. Inputs & Outputs
- **Inputs**: {{ INPUTS_SCHEMA }}
- **Outputs**: {{ OUTPUTS_SCHEMA }}

### 3. Business & Domain Rules
1. `BR-01`: {{ BUSINESS_RULE_1 }}
2. `BR-02`: {{ BUSINESS_RULE_2 }}

### 4. BDD Acceptance Criteria (Gherkin)
```gherkin
Feature: {{ FR_TITLE }}
  Scenario: Success Path
    Given {{ GIVEN_SUCCESS }}
    When {{ WHEN_SUCCESS }}
    Then {{ THEN_SUCCESS }}

  Scenario: Error Handling Path
    Given {{ GIVEN_ERROR }}
    When {{ WHEN_ERROR }}
    Then {{ THEN_ERROR }}
```
