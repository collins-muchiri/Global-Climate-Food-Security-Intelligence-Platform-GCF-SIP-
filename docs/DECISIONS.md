# DECISIONS.md

Zero-Red Mandate decisions (mission rule 11.6).

## D-G1 (2026-10-25) CI matrix pinned to Python 3.11 only

pydantic ^1.10 and langchain 0.0.208 (declared pins) do not support Python 3.12+.
Widening the matrix would require the pydantic-v2/langchain modernisation - an
API-breaking, feature-scale change outside a reliability pass (rule 11.1).
The constraint is now VISIBLE (matrix comment + this file) and tracked in the
modernisation issue instead of silently limiting the project.

## D-G2 (2026-10-25) pandas floor raised ^1.5 -> ^2.1.1

pandera (validation schemas, now a declared test dependency) requires pandas
>=2.1.1; pandas 1.5.3 is from 2022. Source scan for pandas-2-removed APIs
(DataFrame.append, iteritems, .ix): only list.append hits (not the removed
DataFrame API). Suite green on pandas 2.x after the bump.

## D-G3 (2026-10-25) Poetry packaging declares the real src/ layout

`pip install -e .` NEVER worked: Poetry searched for a `gcf-sip` package and
died with ModuleOrPackageNotFoundError. CI masked this by installing only
pytest. Fix matches reality (every module imports `src.*`): `packages =
[{include = "src"}]`. Restructuring to a proper `gcf_sip` namespace is the
right long-term shape and is tracked in the modernisation issue - it renames
every import in the codebase, which is a refactor, not a repair.

## D-G4 (2026-10-25) Pipeline scripts fail loud on missing/invalid input

bronze/silver/gold/governance previously logged (or printed) and exited 0 when
inputs were missing or schema-invalid: a stage could "succeed" having produced
nothing, starving downstream stages silently. All four now exit non-zero. The
e2e test asserts both directions (full run green; missing input red).
