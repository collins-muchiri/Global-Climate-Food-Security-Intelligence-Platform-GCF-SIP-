# Completion matrix

Derived from the repository tree on 24 October 2026 by inspecting which module directories contain
implementation code and which contain only placeholders. Verify each row before publishing; a matrix
that overstates is worse than no matrix.

| Module | Status | Evidence | Note |
|---|---|---|---|
| Ingestion, FAOSTAT | TO VERIFY | directory contents | |
| Ingestion, climate APIs | TO VERIFY | directory contents | |
| Validation and schema registry | Implemented in part | pandera schemas present | state coverage |
| Risk assessment | TO VERIFY | | |
| Scenario modelling | TO VERIFY | | |
| Dashboards | TO VERIFY | streamlit modules present | name which run |
| API layer | TO VERIFY | | |
| Infrastructure, docker compose | Present | compose file | untested end to end |

Rule adopted: a module is Implemented only when a stranger can run it from its README section and
see documented output. Everything else is Partial or Planned. Nineteen placeholder directories are
removed by this release unless a module is Planned with a named owner and date.
