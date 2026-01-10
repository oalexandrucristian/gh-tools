# Workflow Inspector – PR Gate for `.github/workflows`

## Context
This PR introduces a **Workflow Inspector** executed via GitHub Actions, aimed at improving safety, visibility, and maintainability of GitHub Actions workflows in a monorepo setup.

Given the current context:
- a large number of workflows,
- several workflows calling reusable workflows from external organizations,
- increased risk of regressions or unsafe configuration changes,

this solution provides a **lightweight, non-intrusive guardrail** focused exclusively on workflow changes.

---

## What this does
The workflow runs a small Python script that inspects files under `.github/workflows/**` and:

- inventories existing workflows
- shows **which GitHub event** each workflow runs on (`pull_request`, `push`, `schedule`, etc.)
- detects usage of **external reusable workflows**
- checks for the presence of key best-practice elements:
  - explicit `permissions`
  - `concurrency` (best-effort, mainly for deploy/release workflows)
- outputs a clear, readable report in logs and Job Summary

At this stage, the workflow is **informational only** and does not block PRs.

---

## When it runs
The workflow is triggered automatically on pull requests that modify:

```yaml
.github/workflows/**
scripts/workflow_inspector.py
