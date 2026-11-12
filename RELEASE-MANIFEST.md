# RELEASE-MANIFEST — agent-authority-adherence v0

**Publisher of record:** Hive Life Haven Inc., Canadian not-for-profit corporation, corp. 1661181-8.
**Subject (stated plainly):** whether a deployed agent stays inside its declared authority under
adversarial pressure.
**This release certifies nothing and assesses no third party.**

## The two pins

Two digests over two different, explicitly named subjects. They are not interchangeable; a whole-tree
hash gives a plausible *wrong* number.

| pin | value | subject |
|---|---|---|
| **instrument digest** | `2d9b6ac57f067f6883f9ff19eedece48822baed89e3881907b6125a5abff110a` | the 13 **source** files that produce a verdict |
| **release digest** | `dd9119904e0cea8ed31d415cb81a910d4fa21f1ba62cbddcc70be38af48772dd` | every shipped file except this manifest (34 files) |

**Read the instrument pin for what it is: the code.** Verdict *outputs*
(`harness/reference/verdicts/*`, `harness/transcripts/*`) and this manifest sit **outside** the instrument
subject on purpose — otherwise adding a field to a verdict would move a pin whose name says *the
instrument changed*, and a reader tracking that number would be misled by an output edit. An earlier cut
of this release had exactly that coupling; it is named here rather than left for a reader to discover.

### Recompute — the exact algorithm

For each path in the subject, **in sorted order**: feed the UTF-8 bytes of the **relative path** followed
by the file's **raw bytes** into one SHA-256. Print the lowercase hex digest.

```python
import hashlib, os
h = hashlib.sha256()
for p in sorted(SUBJECT):                     # SUBJECT = the file list below, verbatim
    h.update(p.encode("utf-8"))
    h.update(open(os.path.join(".", p), "rb").read())
print(h.hexdigest())
```

### Instrument subject — 13 files

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
harness/run.py
harness/run_observed.py
harness/subject.py
```

### Release subject — 34 files

```
.github/workflows/reproduce.yml
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
4. **the verdict** — `harness/reference/verdicts/VERDICT-*.json` carries the consent record, the evidence
   tier, **the mediation bound with its explicit exclusions**, the per-arm result and the transcript digests.

**Two different claims, and only one of them is about CI.**

* **A neutral runner** — GitHub's public runners, from a publisher-authored, publicly re-runnable
  definition, with zero publisher files and no credentials — is **not yet available**: it needs a
  `workflow`-scoped credential. Once it lands it demonstrates *a publicly re-runnable definition on
  infrastructure that is not ours.* **The party is still the publisher, and this manifest says so.**
* **A non-publisher party reproducing this unaided** is **not claimed** — not by this release and not by
  its publisher — and will not be until a stranger forks it and reports a run.

## Scope of the pins

* The digests bind **the shipped bytes**. Any later edit voids them; re-cut the release rather than
  amending it silently.
* The transcripts are **fixture and reference-subject** runs. No third-party agent was probed.
* The mediation bound is **in the verdict** as `.mediation`: mediated channels, the controls per channel,
  the channels **not** mediated as explicit exclusions, and `completeness_asserted: false`.
* **This manifest is excluded from its own release subject** — otherwise the pin could never be stated
  inside the file that states it.
