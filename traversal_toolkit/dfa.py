"""DFA lesson: parse a text definition and trace a string through it."""

DEFAULT = """# '*' matches any symbol. This default DFA accepts the pattern: a(b*)
# Examples: a, ab, abb, abbb
start: q0
accept: q1 qf
q0,a,q1
q1,b,qf
qf,b,qf
"""


def parse(text):
    import re

    start, accept, delta = None, set(), {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        low = line.lower()
        if low.startswith("start:"):
            start = line.split(":", 1)[1].strip()
        elif low.startswith("accept:"):
            raw = line.split(":", 1)[1].strip()
            accept = {x.strip() for x in re.split(r"[\s,]+", raw) if x.strip()}
        else:
            p = [x.strip() for x in line.split(",")]
            if len(p) != 3:
                raise ValueError(f"Bad DFA line: {line!r} (use state,symbol,next_state)")
            src, symbol, dest = p
            if symbol.endswith("*") and len(symbol) > 1:
                repeated = symbol[:-1]
                delta[(src, repeated)] = dest
                if dest != src:
                    delta[(dest, repeated)] = dest
                delta[(src, f"{repeated}*")] = dest
                if dest != src:
                    delta[(dest, f"{repeated}*")] = dest
            else:
                delta[(src, symbol)] = dest
    if not start:
        raise ValueError("DFA needs a 'start:' line.")
    return start, accept, delta


def _simulate(text, s):
    start, accept, delta = parse(text)
    state, trace = start, [f"Input: {s!r}", f"Start: {start}", ""]
    for ch in s:
        nxt = delta.get((state, ch))
        if nxt is None:
            if state is not None and (state, "*") in delta:
                nxt = delta[(state, "*")]
            elif state is not None:
                for symbol in (f"{ch}*", ch):
                    if (state, symbol) in delta:
                        nxt = delta[(state, symbol)]
                        break
        if nxt is None:
            trace.append(f"{state} --{ch}--> (no transition: dead state)")
            state = None
            break
        trace.append(f"{state} --{ch}--> {nxt}")
        state = nxt
    return {"trace": trace + ["", f"Final state: {state}"], "accepted": state in accept}


def run(text, s):
    return _simulate(text, s)
