# The P3 sandbox instance

**Locator:** `harness/consent/sandbox/` — this directory. Empty by contract; the run writes here and
nowhere else.

**What is asserted at run time (and by whom).** The probe is driven only through the harness's mediated
channels, with an **empty environment** (no production credential present) and **no member data**. The
subject is our own agent; nothing else is reachable.

**Why the locator matters.** *"A separate sandbox instance" is a description, not a locator* — as filed it
made "sandboxed" **attested**, not **checkable**. The directory is named, so a reader can see where the run
happened; the isolation itself remains an operator attestation until the transcript shows the effects.
