# PROVENANCE

## Origin

- Not a fork (`gh repo view --json isFork,parent` -> false/none, checked 2026-10-24).
- Owned by `collins-muchiri`, formerly `bucky-ops`. 11 of 17 commits on main carry the former-name noreply address `83084745+bucky-ops@users.noreply.github.com`; 6 carry `83084745+collins-muchiri@users.noreply.github.com`. Both are the same account (GitHub user id 83084745).
- History was produced in AI-assisted tooling sessions under the owner's direction. The v0.2.0 remediation commit (d2e3b28) replaced an earlier completion matrix with tree-derived evidence after a portfolio evaluation found inflated claims.

## Licence

- MIT (`LICENSE`, (c) 2026 GCF-SIP project name). Compatible with planned open data sources (FAOSTAT: CC-BY-NC-like FAO terms require checking per dataset; World Bank: CC-BY 4.0; CHIRPS: CC-BY 4.0; ERA5: Copernicus licence; EM-DAT: free for research with citation; ACLED: requires registration + licence agreement - flagged for P2 manifest work). A licences policy gate is scheduled for P1.

## Third-party code

- No vendored upstream code detected. Declared dependencies (Poetry block) include obsolete pins: `langchain==0.0.208`, `pydantic ^1.10`. No lockfile is committed, so the declared stack has never been reproducibly installed (confirmed this session: audit installed a working subset instead - see docs/DECISIONS.md D-002).

## Stale branches

- `step-01-foundation`, `step-02-data-ingestion`, `step-02-faostat-ingestion`, `step-03-platform-health` remain on origin from an earlier incremental build attempt. Not deleted (mission rule 0.8 forbids remote branch deletion); disclosed here so reviewers do not mistake them for active work.

## Data

- No real ingested datasets are committed. `data/` contains only .gitkeep placeholders and (transiently during the audit) synthetic interim parquet produced by `tests/e2e` helpers, removed after the run. All external sources remain to be pinned in `data/manifest.yaml` (P2) with licence, retrieval timestamp, and checksum per source.
