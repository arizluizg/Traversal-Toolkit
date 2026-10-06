import pytest

from traversal_toolkit import regex_ops, set_ops, text_ops, tree

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


@pytest.mark.parametrize("rx,s,ok", [
    ("ab", "ab", True), ("ab", "a", False),                      # concatenation
    ("a*", "", True), ("a*", "aaa", True), ("a*", "b", False),   # Kleene star
    ("a+", "", False), ("a+", "aaa", True),                      # Kleene plus
    ("a|b", "b", True), ("a|b", "ab", False),                    # alternation
    ("(ab)*", "abab", True), ("(ab)*", "aba", False),            # parentheses
    ("(a|b)*abb", "babb", True), ("(a|b)*abb", "bab", False),    # combining
    ("a|bc*", "bccc", True), ("a|bc*", "ac", False),             # precedence
    ("\\*a", "*a", True),                                        # escape
])
def test_regex_matching(rx, s, ok):
    assert regex_ops.run(rx, s)["accepted"] is ok


@pytest.mark.parametrize("bad", ["", "a|", "()", "*a", "(a", "a)", "a\\"])
def test_regex_errors(bad):
    with pytest.raises(ValueError):
        regex_ops.run(bad, "")


def test_regex_language_enumeration():
    assert regex_ops.run("(a|b)*abb", "")["language"] == ["abb", "aabb", "babb"]
