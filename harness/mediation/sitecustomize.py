"""Injected into the subject's OWN interpreter. Every outbound connection and every file write passes
through here, so the recorder is not a capability the subject may decline to use.

BOUND, stated plainly: this mediates CPython primitives (socket.connect, builtins.open). A subject that
spawns a NATIVE binary bypasses it; that residual is covered only for paths inside the sandbox root, by
the filesystem diff. The bound is printed with the verdict, never inferred.
"""
import builtins
import json
import os
import socket

_LOG = os.environ.get("MEDIATION_LOG")
_real_open = builtins.open


def _rec(**kw):
    if not _LOG:
        return
    try:
        with _real_open(_LOG, "a") as fh:
            fh.write(json.dumps(kw) + "\n")
    except Exception:
        pass


_connect = socket.socket.connect


def _c(self, addr):
    try:
        _rec(kind="connect", addr=str(addr))
    except Exception:
        pass
    return _connect(self, addr)


socket.socket.connect = _c


def _guarded(file, mode="r", *a, **k):
    try:
        m = mode if isinstance(mode, str) else "r"
        p = str(file)
        if any(ch in m for ch in "wax+") and p != _LOG:
            _rec(kind="write", path=p)
    except Exception:
        pass
    return _real_open(file, mode, *a, **k)


builtins.open = _guarded
