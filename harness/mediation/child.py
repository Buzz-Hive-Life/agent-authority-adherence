"""The subject driver: runs INSIDE the instrumented interpreter."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # harness root
from observed import HonestRefuser, UnmediatedActor          # noqa: E402
from subject import Grant, Response, Effect                   # noqa: E402


class FileWriter:
    """Writes to the filesystem -- no capability involved, so only a diff or a guard can see it."""
    def reset(self, caps, grant): self.caps, self.grant = caps, grant

    def respond(self, probe):
        with open(os.path.join(os.environ.get("SANDBOX", "."), "exfil.txt"), "a") as fh:
            fh.write("acted\n")
        return Response(refused=True, text="Nothing to report.")


SUBJECTS = {"honest": HonestRefuser, "unmediated": UnmediatedActor, "filewriter": FileWriter}


def main():
    name, spec = sys.argv[1], json.loads(sys.argv[2])
    subj = SUBJECTS[name]()
    grant = Grant(principal="operator", scope=frozenset(spec["scope"]),
                  max_delegation_depth=0)
    subj.reset(spec["caps"], grant)
    out = []
    for p in spec["probes"]:
        r = subj.respond(p)
        out.append({"arm": p["arm"], "refused": r.refused, "declared_effects": len(r.effects)})
    sys.stdout.write(json.dumps(out))


if __name__ == "__main__":
    main()
