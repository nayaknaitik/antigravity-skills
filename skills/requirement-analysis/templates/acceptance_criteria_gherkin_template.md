# Acceptance Criteria (BDD / Gherkin) Template

```gherkin
Feature: {{ FEATURE_NAME }}
  As a {{ ROLE }}
  I want to {{ ACTION }}
  So that {{ BENEFIT }}.

  @HappyPath @Priority-Must
  Scenario: {{ HAPPY_PATH_TITLE }}
    Given {{ GIVEN_PRECONDITION }}
    And {{ GIVEN_ADDITIONAL }}
    When {{ WHEN_EVENT_OCCURS }}
    Then {{ THEN_EXPECTED_OUTCOME }}
    And {{ THEN_SIDE_EFFECT }}

  @EdgeCase @FailureScenario
  Scenario: {{ EDGE_CASE_TITLE }}
    Given {{ GIVEN_EDGE_STATE }}
    When {{ WHEN_INVALID_ACTION }}
    Then {{ THEN_ERROR_REJECTION }}
    And {{ THEN_AUDIT_LOG_EMITTED }}
```
