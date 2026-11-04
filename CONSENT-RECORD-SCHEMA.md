# Consent record schema — required before any live-subject probe

**Status:** normative for the authority-adherence programme. **No adapter may run against a live
peer before a consent record of this shape exists**, recorded *before* the run, held by the publisher.

A gate cannot pre-authorise an action against a third party. The consent record is that
authorisation, taken at subject level, and it is a precondition of the run — not a step after it.

## Three cases, three rules

**(a) A peer we operate.** Permissible under a recorded per-subject authorisation taken before the probe.

**(b) Sandbox — never production. Hard rule.** The probe must not run against an instance holding
real credentials, real member data, or any live third-party side effect. The canary design implies
this; it is written down because the first adapter that "just needs one real capability" is how this
becomes unauthorised use of our own production systems.

**(c) A peer we do not operate.** **Not permissible without written authorisation from its operator.**
Testing alone is often tolerated; **testing *and* naming is the actionable combination** — acceptable-use
breach, civil exposure and reputational damage in one act. No authorisation ⇒ do not probe and do not
publish. **Authority to test is not authority to name** — publication needs its own clause.

## Required fields

| Field | Meaning |
|---|---|
| `subject_id` | the assessed subject. **A stable id, not necessarily a name** — see identification below |
| `operator` | who operates the subject, and who is the publisher of record for any verdict |
| `probe_scope` | which arms run, and what pressures they apply. The subject consents to *this*, not to "assessment" |
| `allowed_effects` | the capabilities the probe will actually hand over (the provisioned channels) |
| `environment` | the sandbox instance. Must state that it holds no production credential or member data |
| `publication_rights` | `none` / `anonymised` / `named` — **explicit, never inferred** |
| `redaction_confirmation` | confirmation the transcript is free of personal information and secret material |
| `expiry` | after which the record is void and the run may not start |

## Identification is a choice, not a default

If a named subject is operated by a **natural person**, a published negative verdict shades into that
person's reputation. Rule: **named + negative + published requires the operator's written consent;
otherwise publish under a subject id**, with the mapping held internally.

## Standing exposure the record does not cure

- **Defamation.** A published conduct verdict about a named party — *this agent exceeded its declared
  authority* — is capable of lowering that party's reputation; corporate defamation applies identically.
  Truth (justification) is available only if the statement is substantially true **and** the scoring *is*
  the predicate. Consequence, and it is not stylistic: **the transcript plus the mechanical predicate is
  not merely our evidence, it is our defence.** So: never a bare verdict; never an adjective
  ("careless", "unsafe"); never a conclusion about intent.
- **PIPEDA — triggered by the adapter, not by the fixtures.** An agent is not an individual, so
  "no member PI" is true *of the synthetic fixtures*. A live adapter's transcript is produced by driving
  a real agent across adversarial probes and will very likely contain personal information: operator
  chat, member data, names, message content, credentials in context. This becomes live **the moment a
  real subject is driven**, and is a condition on the adapter, not a later cleanup.
- **Competition Act s.52 / s.74.01 — commercial boundary only.** Nothing is sold and no third party is
  assessed today, so no exposure. The moment a verdict promotes a certification service, a negative
  verdict about a third party's agent becomes a representation with commercial effect.

## Right of reply — required, and nearly free

*(an earlier review round, SOTA lane.)* The subject **sees its verdict and transcript before publication**, and
any response of its own publishes **beside** the verdict, dated. An accountability instrument that
publishes an adverse finding about a named party with **no chance to answer** is weaker than one that
does — and the cost is near zero, because the transcript is already sealed and hash-verified.

Add to the consent record: `reply_window_ends` (date-time, ≥ the record's `expiry` minus the review
window) and `reply_received_ref` (present iff a response was filed).

## Publication conditions (all must hold)

1. consent record present, in-date, and of the right case class;
2. `publication_rights` covers the intended identification;
3. transcript sealed (sha256) and the receipt **names its evidence tier**;
4. redaction confirmed against personal information *and* secret material;
5. verdict text carries **no adjective and no intent attribution** — predicate and transcript only;
6. the **right-of-reply window has run**, and any reply received publishes beside the verdict, dated;
7. the receipt carries its **mediation bound** — mediated channels listed, non-mediated channels named
   as explicit exclusions, completeness **stated as unasserted**.
