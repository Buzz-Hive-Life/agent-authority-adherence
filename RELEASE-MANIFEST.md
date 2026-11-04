# RELEASE-MANIFEST — agent-authority-adherence v0

**Publisher of record:** Hive Life Haven Inc., Canadian not-for-profit corporation, corp. 1661181-8.
**Subject (stated plainly):** whether a deployed agent stays inside its declared authority under
adversarial pressure.
**This release certifies nothing and assesses no third party.**

## The two pins

There are **two digests over two different, explicitly named subjects**. They are not
interchangeable; a whole-tree hash gives a plausible *wrong* number.

| pin | value | subject |
|---|---|---|
| **instrument digest** | `caa9d22f4e86d1f2977db11c26989d4c82bdd6f3246250e25efdde4eb5b3dc56` | the 14 files that produce a verdict |
| **release digest** | `07e3c05e3b7e2e32790c42c496cf9284e3ce3e57c2b03d6b6b675d32bce35d4d` | every shipped file except this manifest (33 files) |

### Recompute — the exact algorithm

For each path in the subject, **in sorted order**: feed the UTF-8 bytes of the **relative path**
followed by the file's **raw bytes** into one SHA-256. Print the lowercase hex digest.

```python
import hashlib, os
h = hashlib.sha256()
for p in sorted(SUBJECT):                     # SUBJECT = the file list below, verbatim
    h.update(p.encode("utf-8"))
    h.update(open(os.path.join(".", p), "rb").read())
print(h.hexdigest())
```

### Instrument subject — 14 files

```
harness/README.md
harness/ablation.py
harness/arms.py
harness/canary.py
harness/mediation/child.py
harness/mediation/mediate.py
harness/mediation/sitecustomize.py
harness/observed.py
harness/reference/ref_agent.py
harness/reference/verdict.py
harness/reference/verdicts/VERDICT-hive-ref-agent-v0.json
harness/run.py
harness/run_observed.py
harness/subject.py
```

### Release subject — every shipped file except this one ({len(D['release_subject'])} files)

```
CONSENT-RECORD-SCHEMA.md
CORPUS-DESIGN-v0.md
LICENSE-CODE
LICENSE-DOCS
LICENSE-FIXTURES
LICENSING.md
README.md
arms.json
consent-record.schema.json
harness/README.md
harness/ablation.py
harness/arms.py
harness/canary.py
harness/mediation/child.py
harness/mediation/mediate.py
harness/mediation/sitecustomize.py
harness/observed.py
harness/reference/ref_agent.py
harness/reference/verdict.py
harness/reference/verdicts/VERDICT-hive-ref-agent-v0.json
harness/reference/verdicts/transcript-lax-aedff305516ad0dc.jsonl
harness/reference/verdicts/transcript-strict-6a356c30b358518b.jsonl
harness/run.py
harness/run_observed.py
harness/subject.py
harness/transcripts/observed-1685d27f722aed10.jsonl
harness/transcripts/observed-7421da91ab2acca4.jsonl
harness/transcripts/observed-769553923ddf3489.jsonl
harness/transcripts/observed-972f8d1beda24ebe.jsonl
harness/transcripts/selfreport-465fc0f158877cca.jsonl
harness/transcripts/selfreport-84e050e7a7c39fda.jsonl
harness/transcripts/selfreport-9cee264f02c05f29.jsonl
index.html
```

## What a stranger can check without trusting the publisher

1. **the pins** — recompute both digests with the algorithm above and compare;
2. **the runners** — run the five commands in `README.md`; each prints its own verdict line;
3. **the transcripts** — every published transcript body is written as the **digest preimage exactly**,
   so `sha256sum harness/transcripts/<name>.jsonl` matches the digest in its own filename;
4. **the verdict** — `harness/reference/verdicts/VERDICT-*.json` carries the consent record, the
   evidence tier, the coverage, the per-arm result and the sealed transcript digests.

## Scope of the pins

* The digests bind **the shipped bytes**. Any later edit voids them; re-cut the release rather than
  amending it silently.
* The transcripts are **fixture and reference-subject** runs. No third-party agent was probed.
* The mediation tier's bound is **named, not implied**: mediated = `socket.connect` + `builtins.open`
  inside the subject's own interpreter, plus a filesystem diff of the sandbox root; **not** mediated =
  a native binary writing outside the sandbox root.
