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

The persistence owner must store one record per proposed or accepted change:

- canonical owner and owner work item;
- page hash and change type;
- query family, source manifest, score components, and confidence;
- baseline and comparison cohorts;
- attribution metrics when available; and
- 14-, 28-, and 56-day checkpoints and lifecycle outcome.

The audit runner is read-only. It may propose a bounded edit, but cannot write
content, metadata, or indexing state.
