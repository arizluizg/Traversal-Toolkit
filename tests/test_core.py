import pytest

from traversal_toolkit import dfa, set_ops, string_extra, text_ops, tree

PRE, INO, POST = ["A", "B", "D", "E", "C", "F"], ["D", "B", "E", "A", "F", "C"], ["D", "E", "B", "F", "C", "A"]


def test_build_from_pre_in():
    r = tree.build(PRE, INO, [])
    assert tree.postorder(r) == POST and tree.height(r) == 3


def test_build_from_post_in():
    assert tree.preorder(tree.build([], INO, POST)) == PRE


def test_mismatched_traversals_rejected():
    with pytest.raises(ValueError):
        tree.build(PRE, INO, list(reversed(POST)))


def test_needs_inorder():
    with pytest.raises(ValueError):
        tree.build(PRE, [], POST)


def test_string_ops():
    rows = dict(text_ops.string_ops("ABC", "XY"))
    assert rows["Concatenation (A + B)"] == "ABCXY" and rows["Reverse of A"] == "CBA"


def test_set_ops():
    rows = dict(set_ops.set_ops(["A", "B"], ["B", "C"]))
    assert rows["Intersection (A ∩ B)"] == "{B}" and rows["Symmetric difference (A Δ B)"] == "{A, C}"


def test_dfa_default_ab_star_pattern():
    assert dfa.run(dfa.DEFAULT, "a")["accepted"] is True
    assert dfa.run(dfa.DEFAULT, "ab")["accepted"] is True
    assert dfa.run(dfa.DEFAULT, "abbb")["accepted"] is True
    assert dfa.run(dfa.DEFAULT, "b")["accepted"] is False


def test_dfa_ab_star_pattern():
    text = """start: q0
accept: q1 qf
q0,a,q1
q1,b*,qf
"""
    assert dfa.run(text, "a")["accepted"] is True
    assert dfa.run(text, "ab")["accepted"] is True
    assert dfa.run(text, "abbb")["accepted"] is True
    assert dfa.run(text, "b")["accepted"] is False


def test_accept_states_allow_space_or_comma_separators():
    parsed = dfa.run(
        """start: q0
accept: q1 qf
q0,a,q1
q1,b,qf
qf,b,qf
""",
        "ab",
    )
    assert parsed["accepted"] is True
    parsed = dfa.run(
        """start: q0
accept: q1,qf
q0,a,q1
q1,b,qf
qf,b,qf
""",
        "ab",
    )
    assert parsed["accepted"] is True


def test_dfa_transition_can_use_symbol_star_notation():
    parsed = dfa.run(
        """start: q0
accept: q1 qf
q0,a,q1
q1,b*,qf
qf,b*,qf
""",
        "abbb",
    )
    assert parsed["accepted"] is True
    parsed = dfa.run(
        """start: q0
accept: q1 qf
q0,a,q1
q1,b*,qf
qf,b*,qf
""",
        "b",
    )
    assert parsed["accepted"] is False


def test_literal_pattern_input_is_not_specialized():
    text = """start: q0
accept: q1 qf
q0,a,q1
q1,b*,qf
qf,b*,qf
"""
    assert dfa.run(text, "a(b*)")["accepted"] is False
    assert dfa.run(text, "ab*")["accepted"] is False
    assert dfa.run(text, "b")["accepted"] is False

    alt_result = dfa.run(
        """start: q0
accept: q0 q1
q0,a,q1
q0,b,q1
""",
        "a|b",
    )
    assert alt_result["accepted"] is False


def test_string_extra_ops():
    rows = dict(string_extra.string_extra_ops("race car", "ABC"))
    assert rows["Prefix of A"] == "rac"
    assert rows["Suffix of A"] == "car"
    assert rows["Reverse of A"] == "rac ecar"
    assert rows["A is a palindrome"] is True
    assert rows["Reverse of B"] == "CBA"
    assert rows["B is a palindrome"] is False


def test_index_renders_sidebar_and_tabs():
    from pathlib import Path

    from app import app

    root = Path(__file__).resolve().parents[1]
    assert (root / "templates" / "sidebar.html").exists()
    assert (root / "templates" / "toolkit" / "tree.html").exists()
    assert (root / "templates" / "toolkit" / "text.html").exists()
    assert (root / "templates" / "toolkit" / "set.html").exists()
    assert (root / "templates" / "toolkit" / "dfa.html").exists()
    assert (root / "static" / "tree.js").exists()
    assert (root / "static" / "text.js").exists()
    assert (root / "static" / "set.js").exists()
    assert (root / "static" / "dfa.js").exists()

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'data-page="tree"' in html
    assert 'data-page="text"' in html
    assert 'data-page="set"' in html
    assert 'data-page="dfa"' in html
    assert 'tree.js' in html
    assert 'text.js' in html
    assert 'set.js' in html
    assert 'dfa.js' in html
    assert "Traversal Toolkit" in html


def test_dfa_request_does_not_require_tree_inputs():
    from app import app

    client = app.test_client()
    response = client.post(
        "/api/analyze",
        json={
            "dfa": "start: q0\naccept: q0\nq0,*,q0",
            "dfa_source": "custom",
            "dfa_custom": "aa",
        },
    )

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["dfa"]["accepted"] is True
