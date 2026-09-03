# SEO operating-audit contract

Use `operating-audit` for a system, skill, evidence-lane, or scheduled
heartbeat review. It is not a page audit and must not invent a public canonical
URL.

## Required checks

1. Name the system owner record and its intended outcome.
2. Compare the scheduled cadence with observed append-only receipts.
3. For a declared local automation, compare its documented configuration with its runtime registration using platform-appropriate locations. A documented schedule without a runtime registration is configuration/runtime drift; do not repair or activate it directly.
4. Record each capability as ready, partial, or unavailable with freshness and a retry condition.
5. Check whether an existing owner record covers every actionable finding.
6. Return one smallest read-only or owner-rail action. Do not create content, submit indexing, or activate automation.

## Required result

```text
mode: operating-audit
system_owner_record:
scope: skill | runtime | automation | evidence lane
scheduled_vs_observed_receipts: expected, observed, gap
runtime_registration: documented state, runtime state
capability_snapshot: source, state, freshness, limitation
evidence_manifest: source, as_of, scope
open_owner_records:
smallest_justified_action:
status: proposed | deferred | blocked-by-evidence | not-needed
blocked_gates:
```

The audit is successful when it makes the current operating state legible and
points to one existing owner. It is not successful merely because a credential
exists or an HTTP endpoint returned 200.
