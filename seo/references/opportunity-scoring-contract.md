# SEO opportunity scoring contract

Use this contract to rank existing pages for review. It does not authorize a
content change, predict revenue, or replace the canonical-owner preflight.

```text
ordering score = max(recovery loss, CTR headroom, rank headroom)
                 × conversion weight
                 × evidence confidence
```

- **Recovery loss** is a real, comparable click decline, not a seasonally or event-driven spike.
- **CTR headroom** uses query/device-aware expected CTR where available. A page average-position estimate is a soft ordering signal only.
- **Rank headroom** is the bounded potential for a query already near page one.
- **Conversion weight** reflects consent-respecting attributable business-outcome evidence. Missing conversion data lowers confidence; it does not mean the page has zero value.
- **Evidence confidence** discounts stale, partial, low-volume, or non-comparable inputs.

## Decay guardrail

Do not call a decline decay when the page or query rose around a launch, news
event, or other time-limited spike. Label it `possible-launch-spike`, keep the
evidence, and wait for another comparable window before proposing a
decay-driven edit.

## Audit record

The [measurement contract](measurement-contract.md) owns audit-record timing,
base fields, and checkpoints. For a ranked opportunity, add the ordering-score
components and evidence-confidence value to that record.

The audit runner is read-only. It may propose a bounded edit, but cannot write
content, metadata, or indexing state.
