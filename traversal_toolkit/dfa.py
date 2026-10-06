"""DFA lesson: parse a text definition and trace a string through it."""

DEFAULT = """# '*' matches any symbol. Replace with the DFA from your class.
# Default: accepts strings of EVEN length.
start: q0
accept: q0
q0,*,q1
q1,*,q0
"""


def parse(text):
    start, accept, delta = None, set(), {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        low = line.lower()
        if low.startswith("start:"):
            start = line.split(":", 1)[1].strip()
        elif low.startswith("accept:"):
            accept = {x.strip() for x in line.split(":", 1)[1].split(",")}
        else:
            p = [x.strip() for x in line.split(",")]
            if len(p) != 3:
                raise ValueError(f"Bad DFA line: {line!r} (use state,symbol,next_state)")
            delta[(p[0], p[1])] = p[2]
    if not start:
        raise ValueError("DFA needs a 'start:' line.")
    return start, accept, delta


def run(text, s):
    start, accept, delta = parse(text)
    state, trace = start, [f"Input: {s!r}", f"Start: {start}", ""]
    for ch in s:
        nxt = delta.get((state, ch)) or delta.get((state, "*"))
        if nxt is None:
            trace.append(f"{state} --{ch}--> (no transition: dead state)")
            state = None
            break
        trace.append(f"{state} --{ch}--> {nxt}")
        state = nxt
    return {"trace": trace + ["", f"Final state: {state}"], "accepted": state in accept}
