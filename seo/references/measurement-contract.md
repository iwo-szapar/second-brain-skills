# SEO measurement contract

This file is the sole authority for SEO change audit records. Create a durable
record when a proposed change is accepted for implementation, then update that
same record when the change ships and at every measurement checkpoint. It must
contain canonical URL, query family, one owner, page hash, change type,
baseline and comparison window, evidence manifest, attribution metrics when
available, exact change or content hash, deployment date when known,
cannibalization guardrail, and result.

The record has three checkpoints:

- **14 days:** directional smoke test only. Do not claim an outcome or reopen a still-measuring recommendation.
- **28 days:** primary comparable-window assessment.
- **56 days:** durable-learning confirmation, including the same comparison cohort and source limitations.

At the 28- and 56-day assessments, classify the outcome as `won`, `lost`, or
`inconclusive`; retain confidence and source limitations. Do not re-open an
unchanged recommendation while its next checkpoint is still measuring. A prose
receipt is evidence, not the durable system of record.
