# Contributing to GCF-SIP

This project follows a production-grade, governance-first development process with a strict branch-per-step workflow. All contributions should pass through review on the designated Step branches before merging into main.

1) Branching model
- main: production-ready
- step-01-foundation: Step 1 foundation
- step-02-ingestion: Step 2 data ingestion
- step-03-platform-health: Step 3 platform health and tests
- Additional steps will follow step-n naming (Step 4, Step 5, etc.)

2) Commit discipline
- Use semantic commits: feat, fix, chore, docs, test, refactor, build
- Do not commit secrets or credentials
- Ensure changes are isolated to a single logical concern per commit

3) Environment & tests
- Use Conda: conda env create -f environment.yml; activate via conda activate gcf-sip-env
- Install in editable mode: pip install -e .
- Run tests: pytest -q

4) Governance & PRs
- Governance artifacts must live under docs/governance
- PRs must include scope, risks, data ethics considerations, and validation plan
- Reviewer sign-off is required before merging into main

5) Quality & compliance
- No silent failures; log clearly and surface actionable errors
- Deterministic behavior and reproducibility are required
- Data handling must be config-driven; avoid hard-coded secrets

Thank you for helping build a robust, auditable data platform.
