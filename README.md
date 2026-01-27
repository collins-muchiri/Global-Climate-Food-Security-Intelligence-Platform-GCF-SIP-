GCF-SIP: GitHub Repository Structure (Monorepo)

This repository houses multiple components for the Global Climate & Food Security Intelligent Platform (GCF-SIP) in a monorepo layout. The structure provides clear separation between architecture, governance, data, notebooks, source code, pipelines, infrastructure, dashboards, tests, and CI configurations.

Notes:
- This is a scaffold. Core implementation files and tests should be filled in iteratively.
- Use .gitignore to avoid committing large or sensitive artifacts.
# Global-Climate-Food-Security Intelligence Platform (GCF-SIP)

Overview
- The GCF-SIP is a production-grade, end-to-end data science and AI platform designed to predict food insecurity risk and simulate climate and funding scenarios using open global data.

System Architecture & Governance
- See docs/architecture and docs/governance for the current architecture intent and governance framework.

Data & Open Datasets
- Supports open data sources; raw data is immutable; transforms are auditable.

Setup & Reproducibility
- Environment is defined via environment.yml and pyproject.toml (Poetry) for deterministic installs.
- CI/CD and IaC approach prepared for integration.

Ethics & Compliance
- Governance-first framing with data ethics, privacy, and model risk guidelines.

How to Use
- See docs for detailed onboarding, setup, and contribution guidelines.
