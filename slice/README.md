# Vertical slice: one indicator, one country, end to end

This directory is the depth-first correction to a breadth-first design. It contains exactly one
working path, and it is the thing a reviewer should run first.

Scope: FAOSTAT cereal yield or food supply indicator, Kenya, 2010 to latest available, ingested with
a pinned retrieval date, validated against a pandera schema, transformed into one risk statistic,
rendered as one streamlit page, published as one markdown output with its numbers.

Acceptance: a stranger clones, runs the three commands below, and obtains the published output with
matching figures. No module outside slice/ may be required.

    pip install -r slice/requirements.txt
    python slice/ingest.py --retrieval-date YYYY-MM-DD
    python slice/analyse.py && streamlit run slice/dashboard.py

When this slice passes acceptance, the completion matrix gains its first Implemented row and every
subsequent module is built to the same bar before it is counted.
