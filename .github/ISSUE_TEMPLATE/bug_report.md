name: Bug Report
description: Report a bug in InsightPro
title: "[BUG] "
labels: ["bug"]

body:
  - type: markdown
    attributes:
      value: |
        Thank you for reporting a bug! Please provide the following information:

  - type: input
    id: version
    attributes:
      label: InsightPro Version
      description: What version are you using?
      placeholder: "2.1"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: What happened?
      placeholder: "I clicked on... and got..."
    validations:
      required: true

  - type: textarea
    id: reproduction
    attributes:
      label: Steps to Reproduce
      description: How can we reproduce the issue?
      placeholder: |
        1. Click on...
        2. Upload...
        3. See error
    validations:
      required: true

  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
      description: What should have happened?
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Error Logs
      description: Paste any error messages or logs
      render: python

  - type: input
    id: os
    attributes:
      label: Operating System
      description: What OS are you using?
      placeholder: "Windows 11, macOS 13, Ubuntu 22.04"
    validations:
      required: true

  - type: dropdown
    id: python-version
    attributes:
      label: Python Version
      options:
        - "3.8"
        - "3.9"
        - "3.10"
        - "3.11"
        - "3.12"
        - "Not sure"
    validations:
      required: true
