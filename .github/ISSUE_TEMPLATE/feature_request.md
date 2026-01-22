name: Feature Request
description: Suggest a new feature for InsightPro
title: "[FEATURE] "
labels: ["enhancement"]

body:
  - type: markdown
    attributes:
      value: "Thank you for suggesting a feature!"

  - type: textarea
    id: problem
    attributes:
      label: Is your feature request related to a problem?
      description: Describe the problem you're trying to solve
      placeholder: "I'm frustrated when..."
    validations:
      required: true

  - type: textarea
    id: solution
    attributes:
      label: Proposed Solution
      description: How should this feature work?
      placeholder: "The feature should allow..."
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternative Solutions
      description: Any other ways to solve this?

  - type: textarea
    id: context
    attributes:
      label: Additional Context
      description: Any other information?

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: I've checked for similar feature requests
          required: true
        - label: This feature would benefit other users
          required: true
