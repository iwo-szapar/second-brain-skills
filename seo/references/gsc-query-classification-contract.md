# Search query-classification contract

## Purpose

Use local deterministic labels to make query-level search-performance analysis
less noisy. This contract does **not** identify traffic source, prove that a
person or AI system issued a query, or create a new SEO mode.

It applies only to query-level quick wins and page refreshes when source rows
include a query dimension. Page-only totals remain unchanged.

## Local taxonomy

| Label | Handling |
| --- | --- |
| `artefact` | Short conversational reply; exclude from query opportunity scoring. |
| `pivot` | Short contextual follow-up; exclude from query opportunity scoring. |
| `tracker_probe` | Rank-tracker-style location probe; exclude from query opportunity scoring. |
| `agent_harness` | Prompt-shaped agent instruction; exclude from query opportunity scoring. |
| `pasted_string` | Likely pasted list or structured string; exclude from query opportunity scoring. |
| `conversational_candidate` | Natural-language question; retain as a separate answer-block diagnostic cohort. |
| `ordinary_or_unclassified` | Everything else; retain in ordinary organic analysis. |

The first five labels are deterministic exclusions. `conversational_candidate`
is a query-shape label, not an AI-surface classification.

## Decision rules

1. Run the classifier locally before computing query-level CTR, rank, or answer-block candidates. Never replace page-level totals with filtered totals.
2. Exclude deterministic non-search classes from query-level scores and show their counts separately in the evidence manifest.
3. A conversational candidate may nominate an answer-block refresh only when the existing canonical owner serves the query, normal performance supports review, and the value rationale remains relevant.
4. A label never establishes query origin, user intent, conversion quality, or a need for a new URL. Run the usual owner, work-item, content-plan, and cannibalization checks.
5. A generative-search report can map pages to AI surfaces only when its export is supplied. Its absence is `unavailable`, not a negative match.

## Provenance and privacy

Record classifier name and version, total query rows, per-label rows, excluded
rows, and candidate rows in the evidence manifest. Do not send query text to a
third-party classifier by default.

An externally hosted model is allowed only as an explicitly approved additive
provider. Record its name and version, data handling, confidence threshold,
row coverage, and failures. Its result remains probabilistic and cannot
override local exclusions, first-party evidence, canonical ownership, or
content approval.

## Tests

Maintain deterministic fixtures for every local label plus these boundaries:

- short replies and agent prompts never inflate query-level CTR opportunity;
- a natural-language question is not reported as confirmed AI-surface traffic;
- ordinary keyword searches remain eligible for ordinary analysis; and
- classifier unavailability or unknown rows do not become zero demand or a negative generative-search match.
