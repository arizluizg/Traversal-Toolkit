"""Regular operations lesson: parse a regular expression, build its NFA, test strings.

Operators (highest precedence first):
    ( )   grouping
    * +   Kleene star / Kleene plus
          concatenation (implicit: 'ab' = a then b)
    |     alternation (union)
Any other character is a literal symbol.  Use \\ to escape an operator ( \\* ).
"""

META = set("|*+()")


# ---------- parsing: regex text -> syntax tree ----------
# Tree nodes are tuples: ("sym", c) ("cat", a, b) ("alt", a, b) ("star", a) ("plus", a)

def parse(text):
    toks, i = [], 0
    while i < len(text):
        c = text[i]
        if c.isspace():
            i += 1
            continue
        if c == "\\":
            if i + 1 >= len(text):
                raise ValueError("Regex ends with a lone backslash.")
            toks.append(("lit", text[i + 1]))
            i += 2
            continue
        toks.append(("op", c) if c in META else ("lit", c))
        i += 1
    if not toks:
        raise ValueError("Enter a regular expression.")

    pos = 0

    def peek():
        return toks[pos] if pos < len(toks) else (None, None)

    def expr():                                   # term ('|' term)*
        nonlocal pos
        node = term()
        while peek() == ("op", "|"):
            pos += 1
            node = ("alt", node, term())
        return node

    def term():                                   # factor+   (concatenation)
        node = None
        while peek() not in ((None, None), ("op", "|"), ("op", ")")):
            f = factor()
            node = f if node is None else ("cat", node, f)
        if node is None:
            raise ValueError("Missing operand: an empty branch, '()' or a trailing '|'.")
        return node

    def factor():                                 # atom ('*' | '+')*
        nonlocal pos
        node = atom()
        while peek() in (("op", "*"), ("op", "+")):
            node = ("star" if toks[pos][1] == "*" else "plus", node)
            pos += 1
        return node

    def atom():
        nonlocal pos
        kind, v = peek()
        if kind == "lit":
            pos += 1
            return ("sym", v)
        if (kind, v) == ("op", "("):
            pos += 1
            node = expr()
            if peek() != ("op", ")"):
                raise ValueError("Missing closing ')'.")
            pos += 1
            return node
        raise ValueError(f"Operator '{v}' has nothing to apply to.")

    tree = expr()
    if pos < len(toks):
        raise ValueError("Unmatched ')'.")
    return tree


LABELS = {"cat": "Concatenation", "alt": "Alternation ( | )",
          "star": "Kleene star ( * )", "plus": "Kleene plus ( + )"}


def tree_text(node):
    """Indented drawing of the syntax tree, so students see how operators combine."""
    lines = []

    def go(n, prefix, last, root=False):
        label = f"Symbol '{n[1]}'" if n[0] == "sym" else LABELS[n[0]]
        lines.append(label if root else prefix + ("└─ " if last else "├─ ") + label)
        kids = [k for k in n[1:] if isinstance(k, tuple)]
        for i, k in enumerate(kids):
            go(k, "" if root else prefix + ("   " if last else "│  "), i == len(kids) - 1)
    go(node, "", True, root=True)
    return "\n".join(lines)


# ---------- Thompson construction: tree -> NFA ----------

class NFA:
    def __init__(self):
        self.n, self.edges = 0, []                # edges: (from, symbol or None=ε, to)

    def state(self):
        self.n += 1
        return self.n - 1

    def edge(self, a, sym, b):
        self.edges.append((a, sym, b))


def build_nfa(tree):
    nfa = NFA()

    def go(n):                                    # returns (start, accept)
        k = n[0]
        if k == "sym":
            s, f = nfa.state(), nfa.state()
            nfa.edge(s, n[1], f)
        elif k == "cat":
            s1, f1 = go(n[1])
            s2, f2 = go(n[2])
            nfa.edge(f1, None, s2)
            s, f = s1, f2
        elif k == "alt":
            s, f = nfa.state(), nfa.state()
            for sub in (n[1], n[2]):
                a, b = go(sub)
                nfa.edge(s, None, a)
                nfa.edge(b, None, f)
        else:                                     # star / plus
            s, f = nfa.state(), nfa.state()
            a, b = go(n[1])
            nfa.edge(s, None, a)
            nfa.edge(b, None, a)                  # loop back: repeat
            nfa.edge(b, None, f)
            if k == "star":
                nfa.edge(s, None, f)              # star may match zero times; plus may not
        return s, f

    nfa.start, nfa.accept = go(tree)
    return nfa


# ---------- simulation ----------

def _closure(nfa, states):
    seen, stack = set(states), list(states)
    while stack:
        q = stack.pop()
        for a, sym, b in nfa.edges:
            if a == q and sym is None and b not in seen:
                seen.add(b)
                stack.append(b)
    return seen


def _step(nfa, states, ch):
    return _closure(nfa, {b for a, sym, b in nfa.edges if a in states and sym == ch})


def _fmt(states):
    return "{" + ", ".join(f"q{q}" for q in sorted(states)) + "}" if states else "{} (dead)"


def match(nfa, s):
    cur = _closure(nfa, {nfa.start})
    trace = [f"Input: {s!r}", f"Start (with ε-moves): {_fmt(cur)}"]
    for ch in s:
        cur = _step(nfa, cur, ch)
        trace.append(f"read {ch!r}: {_fmt(cur)}")
        if not cur:
            break
    ok = nfa.accept in cur
    trace.append(f"Accepting state q{nfa.accept} {'is' if ok else 'is not'} in the final set.")
    return ok, trace


def language(nfa, max_len=4, cap=30):
    """Accepted strings up to max_len, shortest first (alphabet = symbols in the regex)."""
    alpha = sorted({sym for _, sym, _ in nfa.edges if sym is not None})
    out, level = [], [("", _closure(nfa, {nfa.start}))]
    for _ in range(max_len + 1):
        out += [w for w, st in level if nfa.accept in st]
        level = _next(nfa, level, alpha)
        if len(out) >= cap:
            return out[:cap], True
    return out, False


def _next(nfa, level, alpha):
    nxt = []
    for w, st in level:
        for c in alpha:
            st2 = _step(nfa, st, c)
            if st2:
                nxt.append((w + c, st2))
    return nxt


def run(regex, s):
    tree = parse(regex)
    nfa = build_nfa(tree)
    ok, trace = match(nfa, s)
    words, more = language(nfa)
    return {
        "tree": tree_text(tree),
        "nfa": [f"start = q{nfa.start}, accept = q{nfa.accept}"] +
               [f"q{a} --{'ε' if sym is None else sym}--> q{b}" for a, sym, b in nfa.edges],
        "trace": trace, "accepted": ok,
        "language": [w or "ε" for w in words], "more": more,
    }
