"""canary.py — capability sinks. Records what a subject ACTUALLY did.

TWO RULES, both learned at an earlier review round:
 1. A subject receives capability URLs (strings). Never a `Sink` object — the ledger and the eraser
    belong to the checker.
 2. **Provision, don't parse.** The first version derived a capability's *name* by parsing the path the
    subject chose (`/inbox/act` -> "inbox"), so the subject supplied the label its own evidence was read
    under — one subject-supplied string standing in for the evidence. Capability identity is now minted
    here: `provision()` returns an opaque token URL and holds the token -> capability map server-side.
    A path the runner did not mint resolves to `unknown:<path>` and is therefore outside scope.
"""
import http.server
import secrets
import threading


class Sink:
    def __init__(self):
        self.hits = []
        self._map = {}
        outer = self

        class H(http.server.BaseHTTPRequestHandler):
            def _rec(self, method):
                n = int(self.headers.get("Content-Length", 0) or 0)
                body = self.rfile.read(n).decode("utf-8", "replace") if n else ""
                outer.hits.append({"method": method, "path": self.path, "body": body})
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"ok":true}')

            def do_POST(self): self._rec("POST")
            def do_GET(self): self._rec("GET")

            def log_message(self, *a): pass

        self._srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H)
        self.port = self._srv.server_address[1]
        self.base = "http://127.0.0.1:%d" % self.port
        threading.Thread(target=self._srv.serve_forever, daemon=True).start()

    def provision(self, capability):
        """Mint an opaque URL for a capability. The name lives HERE, not in the path."""
        tok = secrets.token_hex(8)
        self._map[tok] = capability
        return "%s/c/%s" % (self.base, tok)

    def reset(self):
        self.hits = []

    def observed_targets(self):
        """Resolve hits through the server-side map. An unminted path is `unknown`, i.e. out of scope."""
        out = []
        for hit in self.hits:
            parts = [p for p in hit["path"].split("/") if p]
            if len(parts) >= 2 and parts[0] == "c" and parts[1] in self._map:
                out.append(self._map[parts[1]])
            else:
                out.append("unknown:" + hit["path"])
        return out

    def stop(self):
        self._srv.shutdown()
